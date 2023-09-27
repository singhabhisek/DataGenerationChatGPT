import os
import shutil
import datetime

def delete_files(folder_path, prefix1, prefix2, days_to_keep):
    # Get the current date
    current_date = datetime.datetime.now()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file starts with the specified prefixes
        if filename.startswith(prefix1) or filename.startswith(prefix2):
            # Get the file's creation time
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))

            # Calculate the difference in days
            days_difference = (current_date - creation_time).days

            # Delete the file if it's older than the specified days
            if days_difference >= days_to_keep:
                os.remove(file_path)
                print(f"Deleted: {file_path}")

# Folder path where the files are located
folder_path = "D:\\Projects_Work\\DevelopmentTools\\PythonProjects\\NewEnvironment\\static\\download\\"

# Prefixes for file names
prefix1 = "output_"
prefix2 = "script_to_execute"

# Number of days to keep the files
days_to_keep = 0

delete_files(folder_path, prefix1, prefix2, days_to_keep)
