import click
from pg_fms.commands import file_operations, file_filtering
from pg_fms.utils import CliError, CliWarning, CliInfo, CliExceptionGroup
import functools
import sys
import os


def handle_cli_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CliError as e:
            click.echo(click.style(f"Error: {str(e)}", fg="red", bold=True), err=True)
            sys.exit(1)
        except CliWarning as e:
            click.echo(click.style(f"Warning: {str(e)}", fg="yellow"), err=True)
        except CliInfo as e:
            click.echo(click.style(f"Info: {str(e)}", fg="cyan"))
        except CliExceptionGroup as e:
            click.echo(
                click.style("Multiple issues occurred:", fg="red", bold=True), err=True
            )
            exceptions = e.exceptions if hasattr(e, "exceptions") else [e]
            for exc in (
                exceptions if isinstance(exceptions, (list, tuple)) else [exceptions]
            ):
                if isinstance(exc, CliError):
                    click.echo(click.style(f"  Error: {str(exc)}", fg="red"), err=True)
                elif isinstance(exc, CliWarning):
                    click.echo(
                        click.style(f"  Warning: {str(exc)}", fg="yellow"), err=True
                    )
                elif isinstance(exc, CliInfo):
                    click.echo(click.style(f"  Info: {str(exc)}", fg="cyan"))
            if any(
                isinstance(exc, CliError)
                for exc in (
                    exceptions
                    if isinstance(exceptions, (list, tuple))
                    else [exceptions]
                )
            ):
                sys.exit(1)
        except click.ClickException as e:
            click.echo(e.format_message(), err=True)
            sys.exit(e.exit_code)
        except Exception as e:  # pylint: disable=broad-except
            click.echo(
                click.style(f"Unexpected error: {str(e)}", fg="red", bold=True),
                err=True,
            )
            sys.exit(1)

    return wrapper


@click.group()
@click.version_option(version="0.1.8", prog_name="pg-fms")
def cli():
    """PG-FMS: The Purple Geckos File Management System

    A CLI tool for efficient file management operations."""
    click.echo(
        click.style(
            "PG-FMS: The Purple Geckos File Management System", fg="green", bold=True
        )
    )


@cli.command("move-file")
@click.argument("source")
@click.argument("destination")
@handle_cli_exception
def move_file_cmd(source, destination):
    """Move a file from SOURCE to DESTINATION."""
    file_operations.move_file(source, destination)
    click.echo(f"Moved file from {source} to {destination}")


@cli.command("copy-file")
@click.argument("source")
@click.argument("destination")
@handle_cli_exception
def copy_file_cmd(source, destination):
    """Copy a file from SOURCE to DESTINATION."""
    file_operations.copy_file(source, destination)
    click.echo(f"Copied file from {source} to {destination}")


@cli.command("filter-files")
@click.option("--type", default=None, help="File type to filter by")
@click.option(
    "--size", nargs=2, type=int, help="File size range to filter by (min max)"
)
@click.option(
    "--date-modified",
    type=int,
    help="Number of days since modification to filter by",
)
@handle_cli_exception
def filter_files_cmd(file_type, size, date_modified):
    """Filter files based on type, size, or modification date."""
    if file_type:
        files = file_filtering.filter_by_type(".", file_type)
    elif size:
        files = file_filtering.filter_by_size(".", size[0], size[1])
    elif date_modified:
        files = file_filtering.filter_by_date_modified(".", date_modified)
    else:
        files = []
    click.echo(f"Filtered files: {files}")


@cli.command("rename-file")
@click.argument("source")
@click.argument("new_name")
@handle_cli_exception
def rename_file_cmd(source, new_name):
    """Rename a file from SOURCE to NEW_NAME."""
    file_operations.rename_file(source, new_name)
    click.echo(f"Renamed file from {source} to {new_name}")


@cli.command("delete-file")
@click.argument("file_path")
@click.option("--force", is_flag=True, help="Force deletion without confirmation")
@handle_cli_exception
def delete_file_cmd(file_path, force):
    """Delete a file at FILE_PATH."""
    if not force and not click.confirm(f"Are you sure you want to delete {file_path}?"):
        return
    file_operations.delete_file(file_path)
    click.echo(f"Deleted file: {file_path}")


@cli.command("list-files")
@click.argument("directory", default=".")
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date"]),
    default="name",
    help="Sort files by name, size, or date",
)
@handle_cli_exception
def list_files_cmd(directory, sort):
    """List files in the specified DIRECTORY."""
    files = file_operations.list_files(directory)
    # Implement sorting based on the 'sort' option
    if sort == "size":
        files.sort(key=lambda f: os.path.getsize(os.path.join(directory, f)))
    elif sort == "date":
        files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    for file in files:
        click.echo(file)


@cli.command("search-files")
@click.argument("pattern")
@click.option("--directory", default=".", help="Directory to search in")
@handle_cli_exception
def search_files_cmd(pattern, directory):
    """Search for files matching PATTERN in the specified DIRECTORY."""
    files = file_operations.search_files(directory, pattern)
    click.echo(f"Files matching '{pattern}':")
    for file in files:
        click.echo(file)


@cli.command("batch-operation")
@click.argument("operation", type=click.Choice(["move", "copy", "delete"]))
@click.argument("source_files", nargs=-1)
@click.option("--destination", help="Destination directory for move or copy operations")
@handle_cli_exception
def batch_operation_cmd(operation, source_files, destination):
    """Perform OPERATION on multiple SOURCE_FILES."""
    for file in source_files:
        if operation == "move":
            file_operations.move_file(file, destination)
        elif operation == "copy":
            file_operations.copy_file(file, destination)
        elif operation == "delete":
            file_operations.delete_file(file)
    click.echo(f"Batch {operation} operation completed on {len(source_files)} files")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
