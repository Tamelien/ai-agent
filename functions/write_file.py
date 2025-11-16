import os
from google.genai import types

def write_file(working_directory, file_path, content):

    base_path = os.path.abspath(working_directory)   
    target_path = os.path.abspath(os.path.join(base_path, file_path))     
 
    if not (target_path.startswith(base_path + os.sep) and target_path != base_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))

        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content argument to a file at the specified file path, constrained to the working directory."\
                "If the file path does not exist, it is created automatically. "\
                "If the file already exists, its contents are overwritten with the value of the content argument.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory."
            ),

            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)