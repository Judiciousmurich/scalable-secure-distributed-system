import multiprocessing
import time

def process_task(task):
    """Generic task processing function"""
    try:
        task_type = task.get('type')
        data = task.get('data', [])

        if task_type == 'compute':
            return sum(data)
        elif task_type == 'sort':
            return sorted(data)
        elif task_type == 'multiply':
            return [x * 2 for x in data]
        elif task_type == 'sleep':
            # Simulate long-running task
            time.sleep(task.get('duration', 1))
            return f"Slept for {task.get('duration', 1)} seconds"
        else:
            return f"Unsupported task type: {task_type}"
    except Exception as e:
        return f"Task processing error: {str(e)}"

def parallel_task_execution(tasks, max_workers=None):
    """Execute multiple tasks in parallel"""
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=max_workers) as pool:
        results = pool.map(process_task, tasks)
    
    return results