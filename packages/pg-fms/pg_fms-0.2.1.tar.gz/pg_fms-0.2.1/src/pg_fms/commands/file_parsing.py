import csv
import json
import xml.etree.ElementTree as ET
import yaml
import re
from typing import Any, Optional
from pg_fms.data_structures import (
    TrieNode,
    LinkedList,
    Queue,
)


def read_text_file(file_path: str) -> Optional[str]:
    """Read a text file and return its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except IOError:
        print(f"Error: Unable to read file - {file_path}")
    except UnicodeDecodeError:
        print(f"Error: File encoding is not UTF-8 - {file_path}")
    return None


def write_text_file(file_path: str, content: str) -> bool:
    """Write content to a text file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return True
    except IOError:
        print(f"Error: Unable to write to file - {file_path}")
    return False


def read_csv(file_path: str) -> Optional[LinkedList]:
    """Read a CSV file and return its content as a linked list."""
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            linked_list = LinkedList()
            for row in reader:
                linked_list.append(row)
            return linked_list
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except csv.Error as e:
        print(f"Error: CSV parsing failed - {file_path} - {str(e)}")
    return None


def write_csv(file_path: str, data: LinkedList) -> bool:
    """Write a linked list to a CSV file."""
    if data.head is None:
        print("Error: No data to write")
        return False
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.head.item.keys())
            writer.writeheader()
            current = data.head
            while current:
                writer.writerow(current.item)
                current = current.next
        return True
    except IOError:
        print(f"Error: Unable to write to file - {file_path}")
    return False


def read_json(file_path: str) -> Optional[Any]:
    """Read a JSON file and return its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format - {file_path}")
    return None


def write_json(file_path: str, data: Any) -> bool:
    """Write data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    except IOError:
        print(f"Error: Unable to write to file - {file_path}")
    except TypeError:
        print(f"Error: Data is not JSON serializable - {file_path}")
    return False


def read_xml(file_path: str) -> Optional[TrieNode]:
    """Read an XML file and return its content as a trie."""
    try:
        root = ET.parse(file_path).getroot()
        trie = TrieNode()

        def build_trie(element, path):
            current_path = f"{path}/{element.tag}"
            trie.insert(current_path)
            for child in element:
                build_trie(child, current_path)

        build_trie(root, "")
        return trie
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except ET.ParseError:
        print(f"Error: Invalid XML format - {file_path}")
    return None


def write_xml(file_path: str, root: ET.Element) -> bool:
    """Write an XML element to a file."""
    try:
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="unicode", xml_declaration=True)
        return True
    except IOError:
        print(f"Error: Unable to write to file - {file_path}")
    except TypeError:
        print(f"Error: Invalid XML element - {file_path}")
    return False


def read_yaml(file_path: str) -> Optional[Any]:
    """Read a YAML file and return its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format - {file_path} - {str(e)}")
    return None


def write_yaml(file_path: str, data: Any) -> bool:
    """Write data to a YAML file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False)
        return True
    except IOError:
        print(f"Error: Unable to write to file - {file_path}")
    return False


def search_text(file_path: str, pattern: str) -> Optional[Queue]:
    """Search for a pattern in a text file and return the matches as a queue."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            matches = Queue()
            for match in re.findall(pattern, file.read()):
                matches.enqueue(match)
            return matches
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except re.error:
        print(f"Error: Invalid regex pattern - {pattern}")
    return None


def replace_text(file_path: str, search: str, replace: str) -> bool:
    """Replace a pattern in a text file with a replacement string."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        modified_content = content.replace(search, replace)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        return True
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except IOError:
        print(f"Error: Unable to read or write file - {file_path}")
    return False


def count_lines(file_path: str) -> Optional[int]:
    """Count the number of lines in a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except IOError:
        print(f"Error: Unable to read file - {file_path}")
    return None


def count_words(file_path: str) -> Optional[int]:
    """Count the number of words in a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return len(file.read().split())
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except IOError:
        print(f"Error: Unable to read file - {file_path}")
    return None


def extract_emails(file_path: str) -> Optional[Queue]:
    """Extract email addresses from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = Queue()
        for email in re.findall(email_pattern, content):
            emails.enqueue(email)
        return emails
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except IOError:
        print(f"Error: Unable to read file - {file_path}")
    return None


def extract_urls(file_path: str) -> Optional[Queue]:
    """Extract URLs from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        urls = Queue()
        for url in re.findall(url_pattern, content):
            urls.enqueue(url)
        return urls
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except IOError:
        print(f"Error: Unable to read file - {file_path}")
    return None
