from flask import Flask, render_template, request

app = Flask(__name__)

# Simulated shell state
fake_shell = {
    "state": "start"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    fake_shell["state"] = "main_menu"
    output = "Welcome to the test app!\nChoose an option:\n1. Option A\n2. Option B"
    options = parse_options_from_output(output)
    return render_template("options.html", output=output, options=options)

@app.route("/send", methods=["POST"])
def send():
    selection = request.form["selection"]

    # Simulated responses
    if fake_shell["state"] == "main_menu":
        if selection == "1.":
            output = "You chose A.\nNext:\na) Sub A1\nb) Sub A2\nc) Sub A3\nd) Sub A4\ne) Sub A5\nf) Sub A6\ng) Sub A7"
            fake_shell["state"] = "sub_menu_a"
        elif selection == "2.":
            output = "You chose B.\nNext:\na) Sub B1\nb) Sub B2\nc) Sub B3\nd) Sub B4\ne) Sub B5\nf) Sub B6\ng) Sub B7"
            fake_shell["state"] = "sub_menu_b"
        else:
            output = "Invalid selection.\n1. Option A\n2. Option B"
    elif fake_shell["state"] in ["sub_menu_a", "sub_menu_b"]:
        output = f"You selected {selection}. Thank you!\nChoose again:\n1. Option A\n2. Option B"
        fake_shell["state"] = "main_menu"
    else:
        output = "Unknown state. Resetting."
        fake_shell["state"] = "main_menu"

    options = parse_options_from_output(output)
    return render_template("options.html", output=output, options=options)

@app.route("/exit", methods=["POST"])
def exit():
    fake_shell["state"] = "start"
    return "<p>Session closed.</p>"

def parse_options_from_output(output):
    import re
    lines = output.strip().splitlines()
    return [line.strip() for line in lines if re.match(r"^\s*[\d]+\.\s|\s*[a-zA-Z]\)", line)]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
