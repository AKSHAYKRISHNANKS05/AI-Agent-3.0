
import re
from agent_router import select_tool, execute_tool
from browser_automation import search_web

def plan_task(command):
    """
    Break a simple combined instruction into smaller tasks.
    """

    command = command.strip()

    if not command:
        return []

    # Split commands containing 'and then' or 'then'
    parts = re.split(
        r"\s+and\s+then\s+|\s+then\s+",
        command,
        flags=re.IGNORECASE
    )

    # Split simple combined commands using 'and'
    tasks = []

    for part in parts:
        sub_tasks = re.split(
            r"\s+and\s+(?=(?:open|show|tell|create|search|read|list|write|append|display|find|give|get)\b)",
            part,
            flags=re.IGNORECASE
        )

        tasks.extend(sub_tasks)

    return [task.strip() for task in tasks if task.strip()]


def browser_search(query):
    """
    Search the web using Playwright and return formatted results.
    """

    results = search_web(query)

    if not results:
        return "No search results found."

    output = []

    for number, item in enumerate(results, start=1):
        output.append(
            f"{number}. {item['title']}\n"
            f"Link: {item['link']}"
        )

    return "\n\n".join(output)


def run_task(command):
    """
    Plan a command and execute its individual tasks.
    """

    tasks = plan_task(command)

    if not tasks:
        return ["Please enter a command."]

    results = []


    for task in tasks:
        print(f"\nProcessing: {task}")

        # Recognise explicit browser-search commands
        if task.lower().startswith("browser search "):
            query = task[len("browser search "):].strip()

            result = browser_search(query)

            results.append({
                "task": task,
                "result": result
            })

            continue

        selected = select_tool(task)


        print("Selected tool:", selected["tool"])

        result = execute_tool(selected)

        results.append({
            "task": task,
            "result": result
        })

    return results


# Run this test only when agent.py is executed directly

if __name__ == "__main__":
    command = "Browser search Python tutorials and then tell me the time"

    results = run_task(command)

    print("\nFinal Results:")

    for item in results:
        print(f"\nTask: {item['task']}")
        print(f"Result:\n{item['result']}")
