import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    
    base_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_path, directory))

    if not (target_path.startswith(base_path + os.sep) or target_path == base_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory'

    try:            
        list_dir = os.listdir(target_path)  
        
        content_dir = ""
        for item in list_dir:
            full_path = os.path.abspath(os.path.join(target_path, item))
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path)
            content_dir += f"- {item}: file_size={size} bytes, is_dir={is_dir}\n"
    
        return content_dir
    
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    
