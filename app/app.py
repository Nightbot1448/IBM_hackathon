import os
import jsons
import geopandas
from shapely.geometry import Point
from flask import Flask, render_template, request

HERE_API_KEY = os.getenv('HERE_API_KEY')

app = Flask(__name__, static_folder="./../static/", template_folder="./../template/")

geodata = geopandas.read_file('static/states.json')

@app.route('/')
def map_func():
    return render_template('map.html', apikey=HERE_API_KEY)


@app.route('/tapped', methods=['POST'])
def func1():
    data = request.get_json()
    print(data)
    tap = Point(float(data.get('lng')), float(data.get('lat')))
    resp = geodata[['NAME', 'STATE']][geodata.geometry.map(tap.within)]
    return resp.iloc[0].to_dict()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
