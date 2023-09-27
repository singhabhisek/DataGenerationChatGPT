import os
import string
import subprocess
import random
import openai
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import shutil

# Set the OpenAI API key
openai.api_key = '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'

app = Flask(__name__)
CORS(app)

# Example usage
source_folder = '.'  # Replace with the actual source folder path
destination_folder = 'static/download/'  # Replace with the actual destination folder path
file_name = 'sample.py'  # Replace with the actual file name


def copy_file_if_exists(source_folder, destination_folder, file_name):
    """Copy a file if it exists from the source folder to the destination folder."""
    source_path = os.path.join(source_folder, file_name)

    # Check if the file exists in the source folder
    if os.path.exists(source_path):
        destination_path = os.path.join(destination_folder, file_name)

        # Copy the file to the destination folder
        shutil.move(source_path, destination_path)
        print(f'File {file_name} copied successfully to {destination_path}')
    else:
        print(f'File {file_name} does not exist in {source_folder}')


# Endpoint to create a new guide
@app.route('/datarequest', methods=["POST"])
def datarequest():
    try:
        script_path1 = 'chatgpt_wrapper.py'
        argument1 = request.json['content']
        randomString = str(generate_random_filename())
        argOutputResult = "output_" + randomString + ".txt"
        argInterimPythonProgram = "script_to_exec_" + randomString + ".py"
        Request_From = request.headers['Request-From']
    except KeyError:
        return jsonify({'error': 'Input data not provided or invalid format'}), 400

    # Run the script and handle the output
    stdout, stderr = run_script(script_path, argument1, argOutputResult, argInterimPythonProgram)
    input_text = stdout + stderr
    file_path = argOutputResult

    # Copy the output file to the destination folder
    copy_file_if_exists(source_folder, destination_folder, file_path)

    # Return the response based on the request origin
    file_path = os.path.join("static", "download", file_path)
    try:
        with open(file_path, 'r') as file:
            data = file.read()
        response_data = data
        if Request_From == 'web':
            return jsonify({'response': response_data, 'filename': os.path.basename(file_path), 'scriptname': os.path.basename(argInterimPythonProgram)})
        else:
            return response_data
    except FileNotFoundError:
        return jsonify({"error": "File not found", "status_code": "404"}), 404


# Serve the generated data file from the 'static/downloads' folder
@app.route('/download/<filename>', methods=["GET", "POST"])
def download(filename):
    return send_file(os.getcwd() +"\\static\\download\\" + filename , as_attachment=True)


def generate_random_filename():
    """Generate a random filename of length 5."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(5))


def run_script(script_path, argContent, argOutputFile, argInterimPythonProgram):
    """Run a script using subprocess and return the stdout and stderr."""
    try:
        result = subprocess.run(['python', script_path, argContent, argOutputFile, argInterimPythonProgram], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return None, str(e)
