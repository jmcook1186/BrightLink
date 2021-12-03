from ImageAnalysis import *


savepath = "/home/joe/Code/BrightLink/"
coords = [[1.3985, 51.3836],\
         [1.3766, 51.3836],\
         [1.3766, 51.3899],\
         [1.3985, 51.3899]]

##analysisType = "ALBEDO" #or "NVDI"

startDate = "2021-06-01"
endDate = "2021-08-31"

score_type = "mean"
ndvi_threshold = 0.5
platform = 'MODIS'

if platform == 'SENTINEL2':
    filepath = "/home/joe/Code/jmcook1186.github.io/Data/BrightLinkData/SentinelData.json"
elif platform == 'LANDSAT':
    filepath = "/home/joe/Code/jmcook1186.github.io/Data/BrightLinkData/LandsatData.json"
elif platform == 'MODIS':
    filepath = "/home/joe/Code/jmcook1186.github.io/Data/BrightLinkData/ModisData.json"



collection, area = setupGEE(coords, platform, startDate, endDate)
ndvi_score = runAnalysis(collection, platform, score_type, savepath, area, plot=True)
update_json(filepath, ndvi_score)
commit_and_push(filepath, "update json page according to outcome of S2 ndvi app")