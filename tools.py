
import webbrowser
import os
from datetime import datetime
from urllib.parse import quote_plus


# Workspace location
WORKSPACE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "agent_workspace"
)


def get_date():
    return datetime.now().strftime("%A, %d-%m-%Y")


def get_time():
    return datetime.now().strftime("%I:%M:%S %p")


def open_website(url):
    if not url.startswith(("https://", "http://")):
        return "Please provide a valid website URL."

    webbrowser.open(url)
    return f"Requested browser opening for {url}"


def create_folder(folder_name):
    os.makedirs(WORKSPACE, exist_ok=True)

    if (
        not folder_name
        or folder_name in (".", "..")
        or os.path.basename(folder_name) != folder_name
    ):
        return "Invalid folder name."

    folder_path = os.path.join(WORKSPACE, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    return f"Folder '{folder_name}' created successfully."


def google_search(query):
    if not query.strip():
        return "Please provide something to search."

    search_url = "https://www.google.com/search?q=" + quote_plus(query)
    webbrowser.open(search_url)

    return f"Requested Google search for: {query}"


def list_folders():
    os.makedirs(WORKSPACE, exist_ok=True)

    folders = [
        name for name in os.listdir(WORKSPACE)
        if os.path.isdir(os.path.join(WORKSPACE, name))
    ]

    if not folders:
        return "No folders found in agent_workspace."

    return "Folders in agent_workspace:\n" + "\n".join(
        f"- {name}" for name in sorted(folders)
    )


def create_file(filename):
    os.makedirs(WORKSPACE, exist_ok=True)

    if (
        not filename
        or filename in (".", "..")
        or "/" in filename
        or "\\" in filename
        or ":" in filename
        or os.path.basename(filename) != filename
    ):
        return "Invalid filename. Please provide a simple filename."

    file_path = os.path.join(WORKSPACE, filename)

    try:
        with open(file_path, "x", encoding="utf-8"):
            pass
    except FileExistsError:
        return f"File '{filename}' already exists."

    return f"File '{filename}' created successfully."


def read_file(filename):
    if (
        not filename
        or filename in (".", "..")
        or "/" in filename
        or "\\" in filename
        or ":" in filename
        or os.path.basename(filename) != filename
    ):
        return "Invalid filename."

    file_path = os.path.join(WORKSPACE, filename)

    if not os.path.isfile(file_path):
        return f"File '{filename}' does not exist."

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read() or "The file is empty."

    except UnicodeError:
        return "This is not a supported UTF-8 text file."

    except OSError as error:
        return f"Unable to read file: {error}"


def append_file(filename, content):
    if (
        not filename
        or filename in (".", "..")
        or "/" in filename
        or "\\" in filename
        or ":" in filename
        or os.path.basename(filename) != filename
    ):
        return "Invalid filename."

    file_path = os.path.join(WORKSPACE, filename)

    if not os.path.isfile(file_path):
        return f"File '{filename}' does not exist."

    if not content.strip():
        return "Please provide some text to write."

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            existing_content = file.read()

        with open(file_path, "a", encoding="utf-8") as file:
            if existing_content and not existing_content.endswith("\n"):
                file.write("\n")

            file.write(content + "\n")

        return f"Text added successfully to '{filename}'."

    except OSError as error:
        return f"Unable to write to file: {error}"


def list_files():
    os.makedirs(WORKSPACE, exist_ok=True)

    files = [
        name for name in os.listdir(WORKSPACE)
        if os.path.isfile(os.path.join(WORKSPACE, name))
    ]

    if not files:
        return "No files found in agent_workspace."

    return "Files in agent_workspace:\n" + "\n".join(
        f"- {name}" for name in sorted(files)
    )


def delete_file(filename):
    filename = filename.strip()

    if (
        not filename
        or filename in (".", "..")
        or "/" in filename
        or "\\" in filename
        or ":" in filename
        or os.path.basename(filename) != filename
    ):
        return "Invalid filename. Only files inside agent_workspace can be deleted."

    file_path = os.path.join(WORKSPACE, filename)

    if not os.path.isfile(file_path):
        return f"File '{filename}' does not exist."

    try:
        os.remove(file_path)
        return f"File '{filename}' deleted successfully."

    except OSError as error:
        return f"Unable to delete file: {error}"
