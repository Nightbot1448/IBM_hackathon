from flask import Flask, render_template, request
import os

HERE_API_KEY = os.getenv('HERE_API_KEY')

app = Flask(__name__, static_folder="./../static/", template_folder="./../template/")


@app.route('/')
def map_func():
    return render_template('map.html', apikey=HERE_API_KEY)


@app.route('/tapped', methods=['POST'])
def func1():
    data = request.get_json()
    print(data)
    return '123'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
