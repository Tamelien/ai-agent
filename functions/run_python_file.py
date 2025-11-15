import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):

    base_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_path, file_path))

    if not target_path.startswith(base_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'

    if not (target_path.endswith(".py") and os.path.isfile(target_path)):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cmd = ["python", target_path] + list(args)
        result = subprocess.run(cmd,
                                cwd=base_path,
                                capture_output=True,
                                text=True,
                                timeout=30,
                                check=False,)
        
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        
        if not stdout and not stderr:
            return "No output produced."

        output = [f"STDOUT: {stdout}", f"STDERR: {stderr}"]

        if result.returncode:
            output.append(f"Process exited with code {result.returncode}")
        
        return output
        

    except Exception as e:
        return f"Error: executing Python file: {e}"