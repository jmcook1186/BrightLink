from ImageAnalysis import *

filepath = "/home/joe/Code/jmcook1186.github.io/Data/example.json"
savepath = "/home/joe/Code/Brightlink/"
coords = [[1.3985, 51.3836],\
         [1.3766, 51.3836],\
         [1.3766, 51.3899],\
         [1.3985, 51.3899]]

ndvi_threshold = 0.5

collection, area = setupGEE(coords)
ndvi_score = runAnalysis(collection, savepath, area, False)
update_json(filepath, ndvi_score)
#commit_and_push(filepath, "update NFT metadata according to outcome of S2 ndvi app")