from ImageAnalysis import *


savepath = "/home/joe/Code/BrightLink/"
coords = [[1.3985, 51.3836],\
         [1.3766, 51.3836],\
         [1.3766, 51.3899],\
         [1.3985, 51.3899]]

ndvi_threshold = 0.5
platform = 'LANDSAT'

if platform == 'SENTINEL2':
    filepath = "/home/joe/Code/jmcook1186.github.io/Data/SentinelData.json"
elif platform == 'LANDSAT':
    filepath = "/home/joe/Code/jmcook1186.github.io/Data/LandsatData.json"

collection, area = setupGEE(coords, platform)
ndvi_score = runAnalysis(collection, platform, savepath, area, plot=True)
update_json(filepath, ndvi_score)
#commit_and_push(filepath, "update NFT metadata according to outcome of S2 ndvi app")