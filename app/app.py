from flask import Flask, render_template
app = Flask(__name__, static_folder="./../static/", template_folder="./../template/")

@app.route('/')
def index():
    return 'Привет'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)