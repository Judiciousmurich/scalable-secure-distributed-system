import os
import sys

# Add the project root directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.utils.logger import setup_logging, log_info, log_error

# Set up a logger specifically for task management
logger = setup_logging("task_manager")

def handle_client_task(conn, addr):
    """
    Handles tasks assigned by the client.

    Parameters:
        conn: The socket connection to the client.
        addr: The address of the connected client.
    """
    log_info(logger, f"Handling tasks for client {addr}.")
    conn.sendall(b"Welcome! Send a task or type 'exit' to disconnect.\n")
    
    while True:
        try:
            # Receive task from the client
            task = conn.recv(1024).decode().strip()
            if not task:
                break  # If the client disconnects unexpectedly
            
            log_info(logger, f"Received task from {addr}: {task}")
            
            if task.lower() == "exit":
                conn.sendall(b"Goodbye!\n")
                log_info(logger, f"Client {addr} requested disconnection.")
                break
            
            # Process the task (in this example, just echoing it back)
            result = f"Task '{task}' completed successfully.\n"
            conn.sendall(result.encode())
            log_info(logger, f"Task from {addr} processed: {task}")
        
        except Exception as e:
            log_error(logger, f"Error while handling task for {addr}", e)
            conn.sendall(b"An error occurred while processing your task.\n")
            break

    # Close the connection
    conn.close()
    log_info(logger, f"Connection with client {addr} closed.")
