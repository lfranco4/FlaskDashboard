import paramiko
from flask import Flask, render_template, request

app = Flask(__name__)

ssh_client = None
ssh_channel = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global ssh_client, ssh_channel
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        "remote_host",
        username="user",
        key_filename="/path/to/key",
        passphrase="passphrase")

    # Create interactive shell
    ssh_channel = ssh_client.invoke_shell()
    ssh_channel.send("cd /remote/path\n")
    import time; time.sleep(1)
    ssh_channel.send("./start_app\n")

    # Small delay and fetch initial output
    import time; time.sleep(1)
    output = ssh_channel.recv(4096).decode()
    options = parse_options_from_output(output)
    return render_template("options.html", output=output, options=options)

@app.route("/send", methods=["POST"])
def send():
    global ssh_channel
    user_input = request.form["selection"]
    ssh_channel.send(user_input + "\n")
    import time; time.sleep(1)
    output = ssh_channel.recv(4096).decode()
    options = parse_options_from_output(output)
    return render_template("options.html", output=output, options=options)

@app.route("/exit", methods=["POST"])
def exit():
    global ssh_client, ssh_channel
    if ssh_channel:
        ssh_channel.close()
    if ssh_client:
        ssh_client.close()
    ssh_channel = None
    ssh_client = None
    return "<p>SSH session closed.</p>"

# Example parser
def parse_options_from_output(output):
    # Example: looks for lines starting with numbers or letters
    import re
    lines = output.strip().splitlines()
    options = [line.strip() for line in lines if re.match(r"^\s*\d+\.\s|\s*[a-zA-Z]\)", line)]
    return options
