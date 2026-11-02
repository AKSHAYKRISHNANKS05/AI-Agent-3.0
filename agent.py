
import re
from agent_router import select_tool, execute_tool
from browser_automation import search_web


def plan_task(command):
    """Break a simple combined instruction into smaller tasks."""

    command = command.strip()

    if not command:
        return []

    parts = re.split(
        r"\s+and\s+then\s+|\s+then\s+",
        command,
        flags=re.IGNORECASE
    )

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
    """Search the web using Playwright and return formatted results."""

    if not query.strip():
        return "Please provide something to search for."

    try:
        results = search_web(query)

        if not results:
            return "No search results found."

        output = []

        for number, item in enumerate(results, start=1):
            output.append(
                f"{number}. {item.get('title', 'Untitled')}\n"
                f"Link: {item.get('link', 'No link available')}"
            )

        return "\n\n".join(output)

    except Exception as error:
        print(f"Browser search error: {error}")
        return "Unable to complete the browser search. Please try again."


def run_task(command, streamlit_mode=False):
    """Plan a command and execute its individual tasks."""

    tasks = plan_task(command)

    if not tasks:
        return {
            "results": [],
            "pending_action": None,
            "remaining_tasks": []
        }

    results = []

    for index, task in enumerate(tasks):

        print(f"\nProcessing: {task}")

        try:

            if task.lower().startswith("browser search "):
                query = task[len("browser search "):].strip()
                result = browser_search(query)

            else:
                selected = select_tool(task)

                print("Selected tool:", selected["tool"])

                if streamlit_mode:
                    result = execute_tool(selected, confirmed=False)
                else:
                    result = execute_tool(selected)

            if (
                isinstance(result, dict)
                and result.get("confirmation_required")
            ):
                return {
                    "results": results,
                    "pending_action": result,
                    "remaining_tasks": tasks[index + 1:]
                }

            results.append({
                "task": task,
                "result": result
            })

        except Exception as error:

            print(f"Task execution error: {error}")

            results.append({
                "task": task,
                "result": (
                    "Unable to complete this task. "
                    "Please check the request and try again."
                )
            })

    return {
        "results": results,
        "pending_action": None,
        "remaining_tasks": []
    }


def approve_pending_action(pending_action):
    """Execute an action after the user approves it."""

    try:
        return execute_tool(
            {
                "tool": pending_action["tool"],
                "argument": pending_action["argument"]
            },
            confirmed=True
        )

    except Exception as error:
        print(f"Approved action error: {error}")
        return "Unable to complete the approved action. Please try again."


# Run this test only when agent.py is executed directly

if __name__ == "__main__":

    command = "Browser search Python tutorials and then tell me the time"

    result = run_task(command)

    print("\nFinal Results:")

    for item in result["results"]:
        print(f"\nTask: {item['task']}")
        print(f"Result:\n{item['result']}")
