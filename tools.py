
import webbrowser
import os
from datetime import datetime


# Tool 1: Get current date
def get_date():
    return datetime.now().strftime("%A, %d-%m-%Y")


# Tool 2: Get current time
def get_time():
    return datetime.now().strftime("%I:%M:%S %p")


# Tool 3: Open a website
def open_website(url):
    if not url.startswith(("https://", "http://")):
        return "Please provide a valid website URL."

    webbrowser.open(url)
    return f"Requested browser opening for {url}"


# Tool 4: Create a folder
def create_folder(folder_name):
    base_folder = os.path.join(
        os.path.dirname(__file__),
        "agent_workspace"
    )

    os.makedirs(base_folder, exist_ok=True)

    # Allow only a simple folder name inside agent_workspace
    if not folder_name or folder_name in (".", ".."):
        return "Invalid folder name."

    if os.path.basename(folder_name) != folder_name:
        return "Please provide a folder name, not a path."

    folder_path = os.path.join(base_folder, folder_name)

    os.makedirs(folder_path, exist_ok=True)

    return f"Folder '{folder_name}' created successfully."


from urllib.parse import quote_plus


def google_search(query):
    if not query.strip():
        return "Please provide something to search."

    search_url = "https://www.google.com/search?q=" + quote_plus(query)

    webbrowser.open(search_url)

    return f"Requested Google search for: {query}"


def list_folders():
    base_folder = os.path.join(
        os.path.dirname(__file__),
        "agent_workspace"
    )

    os.makedirs(base_folder, exist_ok=True)

    folders = [
        name
        for name in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, name))
    ]

    if not folders:
        return "No folders found in agent_workspace."

    return "Folders in agent_workspace:\n" + "\n".join(
        f"- {name}" for name in sorted(folders)
    )


def create_file(filename):
    base_folder = os.path.join(
        os.path.dirname(__file__),
        "agent_workspace"
    )

    os.makedirs(base_folder, exist_ok=True)

    # Allow only simple filenames, not paths
    if (
        not filename
        or filename in (".", "..")
        or "/" in filename
        or "\\" in filename
        or ":" in filename
        or os.path.basename(filename) != filename
    ):
        return "Invalid filename. Please provide a simple filename."

    file_path = os.path.join(base_folder, filename)

    # Prevent overwriting existing files
    try:
        with open(file_path, "x", encoding="utf-8") as file:
            pass
    except FileExistsError:
        return f"File '{filename}' already exists."

    return f"File '{filename}' created successfully."


def read_file(filename):
    base_folder = os.path.join(
        os.path.dirname(__file__),
        "agent_workspace"
    )

    # Prevent accessing files outside the workspace
    if (
        not filename
        or filename in (".", "..")
        or "/" in filename
        or "\\" in filename
        or ":" in filename
    ):
        return "Invalid filename."

    file_path = os.path.join(base_folder, filename)

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
    base_folder = os.path.join(
        os.path.dirname(__file__),
        "agent_workspace"
    )

    # Allow only simple filenames
    if (
        not filename
        or filename in (".", "..")
        or "/" in filename
        or "\\" in filename
        or ":" in filename
        or os.path.basename(filename) != filename
    ):
        return "Invalid filename."

    file_path = os.path.join(base_folder, filename)

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
    base_folder = os.path.join(
        os.path.dirname(__file__),
        "agent_workspace"
    )

    os.makedirs(base_folder, exist_ok=True)

    files = [
        name
        for name in os.listdir(base_folder)
        if os.path.isfile(os.path.join(base_folder, name))
    ]

    if not files:
        return "No files found in agent_workspace."

    return "Files in agent_workspace:\n" + "\n".join(
        f"- {name}" for name in sorted(files)
    )

