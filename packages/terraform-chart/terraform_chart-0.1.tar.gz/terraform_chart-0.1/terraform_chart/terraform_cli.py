import click
import subprocess
import sys
import pkg_resources  # For finding files within the package

@click.group()
def cli():
    """CLI tool for Terraform module scaffolding."""
    pass

@click.command()
@click.argument('module_name')
def create(module_name):
    """Create a Terraform module structure."""
    execute_script('create', module_name)

@click.command()
def list_modules():
    """List all Terraform modules in the repository."""
    execute_script('list')

@click.command()
@click.argument('module_name')
def delete(module_name):
    """Delete a Terraform module locally."""
    execute_script('delete', module_name)

@click.command()
@click.argument('module_name')
def pull(module_name):
    """Pull a Terraform module from the repository."""
    execute_script('pull', module_name)

def execute_script(command, module_name=None):
    """Helper function to execute the terraform.sh script with given arguments."""
    # Path to the terraform.sh script within the package
    try:
        script_path = pkg_resources.resource_filename(__name__, 'terraform.sh')
    except Exception as e:
        click.echo(f"Error locating the script: {e}", err=True)
        sys.exit(1)

    # Prepare the command
    cmd = ['bash', script_path, command]
    if module_name:
        cmd.append(module_name)

    try:
        # Use bufsize=1 for line-buffered output (stdout and stderr)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )

        # Print stdout and stderr in real-time
        for line in process.stdout:
            click.echo(line.strip(), nl=True)
            sys.stdout.flush()  # Ensure the line is printed immediately

        for line in process.stderr:
            click.echo(f"Error: {line.strip()}", err=True, nl=True)
            sys.stdout.flush()  # Ensure the error is printed immediately

        process.wait()  # Ensure the process has finished

        # If the process failed, exit with the error code
        if process.returncode != 0:
            sys.exit(process.returncode)

    except OSError as e:
        click.echo(f"OS Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected Error: {e}", err=True)
        sys.exit(1)

cli.add_command(create)
cli.add_command(list_modules, name='list')
cli.add_command(delete)
cli.add_command(pull)

if __name__ == '__main__':
    cli()