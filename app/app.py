import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from flask import Flask, render_template, request, redirect


HERE_API_KEY = os.getenv('HERE_API_KEY')

app = Flask(__name__, static_folder="./../static/", template_folder="./../template/")

geodata = gpd.read_file('static/states.json').set_index('STATE')
stat = pd.read_csv('static/data.csv', index_col='Code')
merged = stat.merge(geodata, left_index=True, right_index=True, how='outer').drop(columns=['NAME'])

@app.route('/')
def map_func():
    return render_template('map.html', apikey=HERE_API_KEY)


@app.route('/tapped', methods=['POST'])
def func1():
    data = request.get_json()
    #print(data)
    tap = Point(float(data.get('lng')), float(data.get('lat')))
    mask = merged.geometry.map(tap.within)    
    #print(resp)
    if mask.any():
        resp = merged[mask].iloc[0, merged.columns != 'geometry']
        resp['clust'] = int(resp['clust'])
        return render_template('test.html', state_data=resp.to_dict())
    else:
        return 'Not a State'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
