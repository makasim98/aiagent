import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    cwd = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(cwd, file_path))

    if not abs_file_path.startswith(cwd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        args = ["python3", file_path] + args
        completed_process = subprocess.run(args=args, cwd=cwd, timeout=30, capture_output=True, text=True)

        output = []
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

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
                description="Path to the Python file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the Python file. If nothing no arguments provided, run the file without them",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file."
                ),
            )
        },
        required=["file_path"],
    ),
)