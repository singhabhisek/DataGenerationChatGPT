import os
import subprocess
import sys
import openai

# Set the OpenAI API key
openai.api_key = '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'

# Function to write a reply to a file
def write_reply_to_file(reply, file_path):
    try:
        # Construct the full file path
        file_path = os.path.join("static", "download", file_path)

        # Write the reply to the specified file
        with open(file_path, "w") as file:
            file.write(reply)
            print("Code written to", file_path)

        # Modify the file content by replacing certain strings
        new_sentence = 'import datetime'
        rewrite_file(file_path, new_sentence)
    except IOError as e:
        print("An error occurred while writing to the file:", str(e))

# Function to rewrite a file with new content
def rewrite_file(filename, new_sentence):
    try:
        # Read the existing content of the file
        with open(filename, 'r') as file:
            existing_content = file.read()

        # Replace specific strings in the content
        existing_content = existing_content.replace('static/download/{', '{')
        existing_content = existing_content.replace('download/{', '{')
        existing_content = existing_content.replace('static/download/', '')
        existing_content = existing_content.replace('download/', '')
        existing_content = existing_content.replace('```python', '')
        existing_content = existing_content.replace('```', '')

        # Write the new sentence and the modified content back to the file
        with open(filename, 'w') as file:
            file.write(new_sentence + '\n')
            file.write(existing_content)
    except IOError as e:
        print("An error occurred while rewriting the file:", str(e))

# Function to execute a Python script
def execute_python_script(script_path):
    try:
        # Construct the full script path
        script_path = os.path.join("static", "download", script_path)

        # Execute the Python script
        subprocess.run(["python", script_path])
    except FileNotFoundError:
        print("Error: Python executable not found.")
    except Exception as e:
        print("An error occurred:", str(e))

# Main wrapper function
def wrapper(content, filename, scriptname):
    try:
        filename = filename
        messages = [{"role": "system", "content":
            "You are a python code generation assistant. You don't use datetime, uuid, pandas, numpy libraries. You will use loop logic to generate that number of records. You will "
            "be given a description of the problem.  Write result into a  file named " + filename + " and print name of the file. Respond with only the code without explanation."}]
        message = content

        if message:
            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        reply = chat.choices[0].message.content

        if reply:
            messages.append({"role": "assistant", "content": reply})

        script_to_execute = scriptname
        write_reply_to_file(reply, script_to_execute)
        execute_python_script(script_to_execute)

    except IndexError:
        print("Insufficient arguments. Please provide content, filename, and scriptname.")

# Retrieve arguments and call the main wrapper function
content = sys.argv[1] if len(sys.argv) > 1 else ""
filename = sys.argv[2] if len(sys.argv) > 2 else ""
scriptname = sys.argv[3] if len(sys.argv) > 3 else ""
wrapper(content, filename, scriptname)
