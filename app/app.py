import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from flask import Flask, render_template, request, redirect
import requests


HERE_API_KEY = os.getenv('HERE_API_KEY')
WATSON_API_KEY = os.getenv('WATSON_API_KEY')

app = Flask(__name__, static_folder="./../static/",
            template_folder="./../template/")

geodata = gpd.read_file('static/states.json').set_index('STATE')
stat = pd.read_csv('static/data.csv', index_col='Code')
merged = stat.merge(geodata, left_index=True, right_index=True,
                    how='outer').drop(columns=['NAME'])


@app.route('/')
def map_func():
    return render_template('map.html', apikey=HERE_API_KEY)


@app.route('/tapped', methods=['POST'])
def func1():
    data = request.get_json()
    # print(data)
    tap = Point(float(data.get('lng')), float(data.get('lat')))
    mask = merged.geometry.map(tap.within)
    # print(resp)
    if mask.any():
        resp = merged[mask].iloc[0, merged.columns != 'geometry']
        resp['clust'] = int(resp['clust'])
        return render_template('test.html', state_data=resp.to_dict())
    else:
        return 'Not a State'


@app.route('/submitted', methods=['POST'])
def func2():
    data = request.get_json()
    # print(data)
    token_response = requests.post('https://iam.eu-de.bluemix.net/identity/token', data={
                                "apikey": WATSON_API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    #print(token_response.json())
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + mltoken}

    payload_scoring = {
        "input_data": [
            {
                "fields":
                    ['Clear_Days', 'mPS(20m)', 'Petroleum-Fired(%)', 'Natural_Gas-Fired(%)',
                    'Coal-Fired(%)', 'Nuclear(%)', 'Renewables(%)'],
                "values": [
                    list(map(float, data))
                        ]
            }
        ]
    }
    print(list(map(float, data)))
    response_scoring = requests.post('https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/d4e33a8e-ca69-48d2-b8b9-b0be8791e3d8/predictions?version=2020-11-13',
                                    json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    scoring = response_scoring.json()
    scoring['predictions'][0]['values'][0][1][0] = scoring['predictions'][0]['values'][0][1][0].__round__(3)
    print(scoring['predictions'][0]['values'][0][1][0])
    clust = int(scoring['predictions'][0]['values'][0][0])
    print('clust:', clust)
    res = {
        'Clear_Days': int(data[0]),
        'mPS(20m)': float(data[1]),
        'clust': clust,
        'probability': scoring['predictions'][0]['values'][0][1][clust].__round__(3)
    }
    print(res)
    return render_template('model_result.html', response_scoring=res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
