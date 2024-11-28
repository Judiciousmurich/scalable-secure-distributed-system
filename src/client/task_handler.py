def create_task(task_type, message=None):
    if task_type == "PING":
        return "PING"
    elif task_type == "ECHO" and message:
        return f"ECHO:{message}"
    else:
        raise ValueError("Invalid task type.")
