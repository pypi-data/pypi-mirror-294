import os
from datetime import datetime, timedelta
from typing import List, Optional
from pg_fms.utils import CliError, CliWarning
from pg_fms.data_structures import (
    TrieNode,
    LinkedList,
    Queue,
    PriorityQueue,
)


def filter_by_type(directory: str, file_type: str) -> List[str]:
    """Filter files by type."""
    try:
        trie = TrieNode()
        for f in os.listdir(directory):
            if f.endswith(file_type):
                trie.insert(f)
        return trie.get_all_words()
    except FileNotFoundError as e:
        raise CliError(f"Directory not found: {directory}") from e
    except PermissionError as e:
        raise CliError(f"Permission denied: {directory}") from e


def filter_by_size(directory: str, min_size: int, max_size: int) -> List[str]:
    """Filter files by size."""
    try:
        pq = PriorityQueue()
        for f in os.listdir(directory):
            size = os.path.getsize(os.path.join(directory, f))
            if min_size <= size <= max_size:
                pq.enqueue((-size, f))  # Negative size for max-heap behavior
        return [f for _, f in pq.to_sorted_list()]
    except FileNotFoundError as e:
        raise CliError(f"Directory not found: {directory}") from e
    except PermissionError as e:
        raise CliError(f"Permission denied: {directory}") from e


def filter_by_date_modified(directory: str, days: int) -> List[str]:
    """Filter files by date modified."""
    try:
        cutoff = datetime.now() - timedelta(days=days)
        queue = Queue()
        for f in os.listdir(directory):
            mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(directory, f)))
            if mtime > cutoff:
                queue.enqueue((mtime, f))
        return [f for _, f in sorted(queue.to_list(), reverse=True)]
    except FileNotFoundError as e:
        raise CliError(f"Directory not found: {directory}") from e
    except PermissionError as e:
        raise CliError(f"Permission denied: {directory}") from e


def batch_filter_by_type(directory: str, file_type: str) -> List[str]:
    """Filter files by type."""
    return filter_by_type(directory, file_type)


def batch_filter_by_size(directory: str, min_size: int, max_size: int) -> List[str]:
    """Filter files by size."""
    return filter_by_size(directory, min_size, max_size)


def batch_filter_by_date_modified(directory: str, days: int) -> List[str]:
    """Filter files by date modified."""
    return filter_by_date_modified(directory, days)


def batch_operation(
    operation: str, source_files: List[str], destination: Optional[str] = None
) -> List[str]:
    """Batch operation on files."""
    operations = {
        "filter_by_type": batch_filter_by_type,
        "filter_by_size": lambda s, d: batch_filter_by_size(
            s, int(d.split(",")[0]), int(d.split(",")[1])
        ),
        "filter_by_date_modified": lambda s, d: batch_filter_by_date_modified(
            s, int(d)
        ),
    }

    if operation not in operations:
        raise CliError(f"Unknown operation: {operation}")

    results = LinkedList()
    for file in source_files:
        try:
            result = operations[operation](file, destination)
            for item in result:
                results.append(item)
        except CliError as e:
            raise CliError(f"Error processing {file}: {str(e)}") from e
        except Exception as e:
            raise CliError(f"Unexpected error processing {file}: {str(e)}") from e

    if results.is_empty():
        raise CliWarning("No files match the specified criteria.")

    return results.to_list()
