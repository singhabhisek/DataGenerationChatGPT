import os
import string
import subprocess
from random import random

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def generate_random_filename():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(10))


def generate_file(input_text, filename):
    file_content = f"This is the content of the file generated with input: {input_text}"
    with open(filename, 'w') as file:
        file.write(file_content)


@app.route('/process', methods=['POST'])
def process():
    script_path = 'chatgpt_wrapper.py'
    argument1 = request.form['input_text']
    argument2 = "mydataset1.txt"
    argument3 = "script_to_exec.py"

    # input_text = wrapper(request.form['input_text'])
    # You can invoke your Python program here with input_text
    # For simplicity, we'll echo the input_text as the response
    stdout, stderr = run_script(script_path, argument1, argument2, argument3)
    input_text = stdout + stderr
    file_path = argument2

    try:
        file_path = os.path.join("static", "download", file_path)
        script_path = os.path.join("static", "download", argument3)
        with open(file_path, 'r') as file:
            response = file.read()
    except FileNotFoundError:
        response = "File not generated"

    # response = f"Received input: {input_text}"
    # return render_template('index.html', response=response)
    return jsonify({'response': response, 'filename': file_path, 'scriptname': script_path})


if __name__ == '__main__':
    app.run(debug=True)


def run_script(script_path, arg1, arg2, arg3):
    try:
        result = subprocess.run(['python', script_path, arg1, arg2, arg3], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return None, str(e)


def wrapper(inputval):
    return "welcome: " + inputval
