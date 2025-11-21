import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    working_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_path, file_path))

    # Path Traversal Validation (Security Check)
    if not target_path.startswith(working_path):
        return f'Cannot execute "{file_path}" as it is outside the permitted working directory.'
        
    # Check if the file exists and is a file
    if not os.path.exists(target_path):
        return f'ERROR: File "{file_path}" does not exist.'
    
    # Check if the file has a .py extension
    if not file_path.endswith('.py'):
        return f'ERROR: File "{file_path}" is not a Python file.'
    
    # Run the Python file
    try:
        command =["python", target_path]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,  # Prevent long-running scripts
            cwd=working_path,
        )
    
        # --- 2. Fallback and Standard Output Formatting ---
        # If no unit test pattern was found, format the standard output/error/exit code
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)