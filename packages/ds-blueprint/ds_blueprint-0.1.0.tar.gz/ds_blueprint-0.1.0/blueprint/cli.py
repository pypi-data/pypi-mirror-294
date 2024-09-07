import os
import click
import subprocess
from importlib import resources

def get_template_content(template_name):
    try:
        # Assuming 'templates' is a directory inside your 'blueprint' package
        with resources.open_text('blueprint.templates', template_name) as file:
            return file.read()
    except FileNotFoundError:
        click.echo(f"Warning: Template '{template_name}' not found.")
        return ""


@click.group()
def cli():
    """Blueprint CLI tool for project creation."""
    pass

@cli.command()
@click.argument('name')
@click.option('--blueprint', default='default', help='Blueprint to use for project creation')
def draft(name, blueprint):
    """Create a new project with the given NAME using the specified or default blueprint."""
    if blueprint == 'default':
        create_default_blueprint(name)
    else:
        # TODO: Implement custom blueprint logic
        click.echo(f"Custom blueprint '{blueprint}' not implemented yet.")
        return

    click.echo(f"Project {name} created successfully using the {blueprint} blueprint!")

def create_default_blueprint(name):
    """Create the default project structure."""
    # Create directories
    directories = [
        f"{name}/conf",
        f"{name}/conf/local",
        f"{name}/conf/base",
        f"{name}/src",
        f"{name}/notebooks",
        f"{name}/data/01_bronze",
        f"{name}/data/02_silver",
        f"{name}/data/03_gold",
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create .gitkeep files in all directories
        open(os.path.join(directory, ".gitkeep"), "w").close()

    # Create .gitignore
    gitignore_content = get_template_content('gitignore_template.txt')
    with open(f"{name}/.gitignore", "w") as f:
        f.write(gitignore_content)

    # Create README.md
    readme_content = get_template_content('README_template.md')
    with open(f"{name}/README.md", "w") as f:
        f.write(readme_content)

    # Create logger.yml
    logger_content = get_template_content('logger.yml')
    with open(f"{name}/conf/base/logger.yml", "w") as f:
        f.write(logger_content)

    # Create credentials.yml
    credentials_path = os.path.join(name, "conf", "local", "credentials.yml")
    with open(credentials_path, "w") as f:
        f.write("# Add your credentials here\n")

    # Create environment.yml
    environment_content = get_template_content('environment.yml')
    with open(os.path.join(name, "conf", "base", "environment.yml"), "w") as f:
        f.write(environment_content)

@cli.command()
@click.argument('project_path')
@click.option('--package', default='blueprint-environments', help='Package to add to dependencies')
def configure(project_path, package):
    """Configure the project by installing Poetry and adding a specified package."""
    click.echo(f"Configuring project in {project_path}")

    # Change to the project directory
    os.chdir(project_path)

    # Initialize Poetry project
    click.echo("Initializing Poetry project...")
    try:
        subprocess.run(["poetry", "init", "--no-interaction"], check=True)
        click.echo("Poetry project initialized.")
    except subprocess.CalledProcessError:
        click.echo("Failed to initialize Poetry project.")
        return

    # Add the specified package
    click.echo(f"Adding package {package} to dependencies...")
    try:
        subprocess.run(["poetry", "add", package], check=True)
        click.echo(f"Package {package} added successfully.")
    except subprocess.CalledProcessError:
        click.echo(f"Failed to add package {package}.")
        return

    click.echo("Project configuration completed successfully!")


if __name__ == '__main__':
    cli()
