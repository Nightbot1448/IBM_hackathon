from flask import Flask, render_template
import os

HERE_API_KEY = os.getenv('HERE_API_KEY')

app = Flask(__name__, static_folder="./../static/", template_folder="./../template/")

@app.route('/')
def map_func():
	return render_template('map.html',apikey=HERE_API_KEY)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
