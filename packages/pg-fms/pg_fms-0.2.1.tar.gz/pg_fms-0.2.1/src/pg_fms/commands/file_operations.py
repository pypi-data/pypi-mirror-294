import os
import shutil
import fnmatch
from typing import List, Optional, Callable
from pg_fms.data_structures import (
    TrieNode,
    LinkedList,
    Stack,
    Queue,
)


def safe_operation(func: Callable) -> Callable:
    """Safe operation decorator."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(f"Error: File or directory not found - {args[0]}")
        except PermissionError:
            print(f"Error: Permission denied - {args[0]}")
        except IsADirectoryError:
            print(f"Error: Expected file, found directory - {args[0]}")
        except NotADirectoryError:
            print(f"Error: Expected directory, found file - {args[0]}")
        except shutil.Error as e:
            print(f"Error: Operation failed - {str(e)}")
        except OSError as e:
            print(f"Error: OS error occurred - {str(e)}")

    return wrapper


@safe_operation
def move_file(source: str, destination: str) -> None:
    """Move a file to a destination."""
    if not os.path.exists(source):
        raise FileNotFoundError(source)
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(source))
    shutil.move(source, destination)


@safe_operation
def copy_file(source: str, destination: str) -> None:
    """Copy a file to a destination."""
    if not os.path.exists(source):
        raise FileNotFoundError(source)
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(source))
    shutil.copy2(source, destination)


@safe_operation
def rename_file(source: str, new_name: str) -> None:
    """Rename a file."""
    if not os.path.exists(source):
        raise FileNotFoundError(source)
    new_path = os.path.join(os.path.dirname(source), new_name)
    os.rename(source, new_path)


@safe_operation
def delete_file(file_path: str) -> None:
    """Delete a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
    else:
        os.remove(file_path)


@safe_operation
def create_file(file_path: str) -> None:
    """Create a file."""
    if os.path.exists(file_path):
        print(f"Warning: File already exists - {file_path}")
        return
    with open(file_path, "w", encoding="utf-8") as file:
        pass


@safe_operation
def read_file(file_path: str) -> Optional[str]:
    """Read a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


@safe_operation
def list_files(directory: str) -> Optional[List[str]]:
    """List all files in a directory."""
    if not os.path.exists(directory):
        raise FileNotFoundError(directory)
    if not os.path.isdir(directory):
        raise NotADirectoryError(directory)
    trie = TrieNode()
    for file in os.listdir(directory):
        trie.insert(file)
    return trie.get_all_words()


@safe_operation
def search_files(directory: str, pattern: str) -> Optional[List[str]]:
    """Search for files in a directory."""
    if not os.path.exists(directory):
        raise FileNotFoundError(directory)
    if not os.path.isdir(directory):
        raise NotADirectoryError(directory)
    matches = Queue()
    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.enqueue(os.path.join(root, filename))
    return matches.to_list()


def batch_operation(
    operation: str, source_files: List[str], destination: Optional[str] = None
) -> None:
    """Batch operation."""
    operations = {
        "move": move_file,
        "copy": copy_file,
        "delete": delete_file,
        "rename": rename_file,
        "create": create_file,
        "read": lambda s, _: print(read_file(s) or ""),
        "list": lambda s, _: print("\n".join(list_files(s) or [])),
        "search": lambda s, d: print("\n".join(search_files(s, d) or [])),
    }

    if operation not in operations:
        print(f"Error: Unknown operation - {operation}")
        return

    queue = Queue()
    for file in source_files:
        queue.enqueue((file, destination))

    while not queue.is_empty():
        file, dest = queue.dequeue()
        operations[operation](file, dest)


def batch_move(source_files: List[str], destination: str) -> None:
    """Move files to a destination."""
    if not os.path.exists(destination):
        print(f"Error: Destination directory not found - {destination}")
        return
    batch_operation("move", source_files, destination)


def batch_copy(source_files: List[str], destination: str) -> None:
    """Copy files to a destination."""
    if not os.path.exists(destination):
        print(f"Error: Destination directory not found - {destination}")
        return
    batch_operation("copy", source_files, destination)


def batch_delete(source_files: List[str]) -> None:
    """Delete files."""
    stack = Stack()
    for file in source_files:
        stack.push(file)
    while not stack.is_empty():
        batch_operation("delete", [stack.pop()])


def batch_rename(source_files: List[str], new_name: str) -> None:
    """Rename files."""
    if len(source_files) > 1:
        print("Error: Can only rename one file at a time")
        return
    batch_operation("rename", source_files, new_name)


def batch_create(source_files: List[str]) -> None:
    """Create files."""
    batch_operation("create", source_files)


def batch_read(source_files: List[str]) -> None:
    """Read files."""
    linked_list = LinkedList()
    for file in source_files:
        linked_list.append(file)
    current = linked_list.head
    while current:
        batch_operation("read", [current.data])
        current = current.next


def batch_list(source_files: List[str]) -> None:
    """List files."""
    batch_operation("list", source_files)


def batch_search(source_files: List[str], pattern: str) -> None:
    """Search for files."""
    batch_operation("search", source_files, pattern)
