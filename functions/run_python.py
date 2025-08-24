import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_abspath = os.path.abspath(working_directory)

        if not full_path.startswith(working_abspath):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # Check if the file path exists
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not full_path.endswith('.py'):
            f'Error: "{file_path}" is not a Python file.'
        #Use the subprocess.run function to execute the Python file and get back a "completed_process" object. Make sure to:
        #Set a timeout of 30 seconds to prevent infinite execution
        #Capture both stdout and stderr
        #Set the working directory properly
        #Pass along the additional args if provided
        completed_process = subprocess.run(['python', full_path] + args, check=True, timeout=30, capture_output=True, text=True, cwd=working_directory)

        # Return a string with the output formatted to include:
        # The stdout prefixed with STDOUT:, and stderr prefixed with STDERR:. The "completed_process" object has a stdout and stderr attribute.
        # If the process exits with a non-zero code, include "Process exited with code X"
        # If no output is produced, return "No output produced."
        output = []
        if completed_process.stdout:
            output.append(f'STDOUT: {completed_process.stdout.strip()}')
        if completed_process.stderr:
            output.append(f'STDERR: {completed_process.stderr.strip()}')
        if completed_process.returncode != 0:
            output.append(f'Process exited with code {completed_process.returncode}')
        
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f'Error: {str(e)}'
    
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