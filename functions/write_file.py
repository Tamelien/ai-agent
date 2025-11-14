import os

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