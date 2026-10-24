
import json
import os

MEMORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "agent_memory.json"
)


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_memory(key, value):
    memory = load_memory()

    memory[key] = value

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)

    return f"Remembered: {key} = {value}"


def delete_memory(key):
    memory = load_memory()

    if key not in memory:
        return f"No saved memory found for: {key}"

    del memory[key]

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)

    return f"Deleted saved memory: {key}"
