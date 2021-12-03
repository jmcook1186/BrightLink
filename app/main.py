from matplotlib.pyplot import get
from ImageAnalysis import *
import threading
import asyncio
from flask import Flask, jsonify, request


print(f"In flask global level: {threading.current_thread().name}")
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    print(f"Inside flask function: {threading.current_thread().name}")
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    x1  = request.args.get('x1')
    y1  = request.args.get('y1')
    x2  = request.args.get('x2')
    y2  = request.args.get('y2')
    x3  = request.args.get('x3')
    y3  = request.args.get('y3')
    x4  = request.args.get('x4')
    y4  = request.args.get('y4')
    start_date = request.args.get('start')
    end_date =request.args.get('end')
    result = loop.run_until_complete(run_analysis(x1,y1,x2,y2,x3,y3,x4,y4,start_date,end_date))
    return jsonify({"result": result})


async def run_analysis(x1,y1,x2,y2,x3,y3,x4,y4, start, end):
    
    coords = [[float(x1), float(y1)],\
            [float(x2), float(y2)],\
            [float(x3), float(y3)],\
            [float(x4), float(y4)]]

    score_type = "mean"
    ndvi_threshold = 0.5
    filepath = "/home/joe/Code/jmcook1186.github.io/Data/BrightLinkData/LandsatData.json"
    scores = []

    for platform in ['MODIS','SENTINEL2','LANDSAT']:
    
        collection, area = setupGEE(coords, platform, start, end)
        ndvi_score = runAnalysis(collection, platform, score_type, filepath, area, plot=False)
        scores.append(ndvi_score)


    result = np.mean(scores)

    update_json(filepath, result)
    commit_and_push(filepath, "update json page according to outcome of S2 ndvi app")
    
    return result

