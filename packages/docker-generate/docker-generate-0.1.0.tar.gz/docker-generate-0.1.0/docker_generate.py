import os
import click
import subprocess
from src.file_selector import create_file_selector_app
from src.llm import choose_llm, get_extra_info, send_to_llm
from src.utils import extract_code, get_files_in_directory, read_file_content


def get_valid_filename(initial_name="dockerfile"):
    if not os.path.exists(initial_name):
        return initial_name

    click.echo(click.style(f"'{initial_name}' already exists.", fg="yellow"))
    new_name = click.prompt("Enter a new filename (or press Enter to overwrite)", default="", show_default=False)

    if new_name:
        return get_valid_filename(new_name)
    else:
        return initial_name


def get_tree_output(depth=1):
    try:
        # Check if .gitignore exists
        gitignore_path = os.path.join(os.getcwd(), '.gitignore')
        if os.path.exists(gitignore_path):
            # Read .gitignore and prepare patterns
            with open(gitignore_path, 'r') as f:
                ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            # Construct the tree command with ignore patterns
            ignore_args = sum([['-I', pattern] for pattern in ignore_patterns], [])
            cmd = ['tree', '-L', str(depth)] + ignore_args
        else:
            cmd = ['tree', '-L', str(depth)]

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        click.echo(click.style("Warning: 'tree' command not found. Project structure will not be included.", fg="yellow"))
        return ""
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error running tree command: {e}", fg="red"))
        return ""


@click.command()
def main():
    click.clear()
    click.echo(click.style("Welcome to the LLM Dockerfile Generator!", fg="blue", bold=True))

    selected_llm = choose_llm()
    click.echo(click.style(f"Selected LLM: {selected_llm}", fg="blue"))

    # Get files in the current directory
    files = get_files_in_directory()

    # Let the user select files
    selected_files = create_file_selector_app(files)

    if not selected_files:
        click.echo(click.style("ERROR: No files selected. Exiting.", fg="red"))
        return

    click.clear()

    # Display summary:
    click.echo(click.style("Selected files:", fg="bright_white"))
    for file in selected_files:
        click.echo(click.style(f"- {file}", fg="white"))
    click.echo(click.style("Selected Model:", fg="bright_white"))
    click.echo(click.style(f"- {selected_llm}", fg="white"))

    # Get project structure
    click.echo()
    tree_depth = click.prompt(click.style("Show the LLM the projects structure with a depth of: (0 for no None)", fg="blue"), default=3, type=int)
    tree_output = ""
    if tree_depth > 0:
        tree_output = get_tree_output(tree_depth)
    if tree_output != "":
        click.echo(click.style("Project tree:", fg="bright_white"))
        click.echo(tree_output)

    # Extra info ?
    extra_info = get_extra_info()
    if extra_info != "":
        click.echo(click.style("Extra info:", fg="bright_white"))
        click.echo(click.style(f"- {extra_info}", fg="white"))

    # Read content of selected files
    content = "Project Structure:\n" + tree_output + "\n\n"
    for file in selected_files:
        content += f"File: {file}\n"
        content += read_file_content(file)
        content += "\n\n"

    confirmed = click.confirm(
        click.style("\nReady to generate? This will analyze the selected files and create output based on your choices. ", fg="bright_white") +
        click.style("\nProceed?", fg="blue", bold=True),
        default=True
    )
    if not confirmed:
        click.echo(click.style("Generation cancelled by user", fg="yellow"))
        return

    # Send to LLM
    # INFO OpenAI or Anthropic key need to be setted as env var
    dockerfile_content = send_to_llm(content, extra_info, selected_llm)

    if dockerfile_content is None:
        click.echo(click.style("ERROR: LLM did not return anything", fg="red"))
        return

    # Write output to file
    output_file = get_valid_filename()

    with open(output_file, 'w') as file:
        file.write(extract_code(dockerfile_content))

    click.echo(f"\n{dockerfile_content}\n")

    click.echo(click.style(f"Dockerfile has been generated and saved as '{output_file}'", fg="blue"))
    if output_file != "dockerfile":
        click.echo(click.style("Note: A custom filename was used due to a naming conflict.", fg="yellow"))


if __name__ == "__main__":
    main()
