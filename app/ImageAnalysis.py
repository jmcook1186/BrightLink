import ee
import numpy as np
import json
import os
from github import Github
from git import Repo
from dotenv import load_dotenv

load_dotenv()

def setupGEE(coords, platform, startDate, endDate):

    # init the ee object
    ee.Initialize()
    
    area = ee.Geometry.Polygon([coords],None,False)

    # select platform
    if platform =='SENTINEL2':
        platformPath = "COPERNICUS/S2"
        BandLong = 'B8'
        BandShort = 'B4'
    
    elif platform == 'LANDSAT':
        platformPath = "LANDSAT/LC08/C01/T1_TOA"
        BandLong = 'B5'
        BandShort = 'B4'
    
    elif platform == 'MODIS':
        platformPath = "MODIS/MOD09GA_006_NDVI"
        BandLong = None
        BandShort = None
    else:
        raise ValueError("please select a valid platform from: MODIS, SENTINEL2, LANDSAT")

    # define the image
    if (platform == "SENTINEL2") or (platform == "LANDSAT"):

        collection = ee.ImageCollection(platformPath).filterBounds(area)\
                                            .filterDate(startDate, endDate)\
                                            .select([BandLong, BandShort])
    
    elif platform == "MODIS":
        collection = ee.ImageCollection(platformPath)\
                  .filter(ee.Filter.date(startDate, endDate))

        
    print(" number of image: ",collection.size().getInfo())
    if collection.size().getInfo() == 0:
        raise ValueError("There are no valid images for this area/date combination")

    return collection, area


def albedo_LANDSAT():
    return

def albedo_Sentinel():
    return

# perform any calculation on the image collection here
def ndvi_S2(img):
    ndvi = ee.Image(img.normalizedDifference(['B8', 'B4'])).rename(["ndvi"])
    return ndvi

def ndvi_LANDSAT(img):
    ndvi = ee.Image(img.normalizedDifference(['B5','B4'])).rename(['ndvi'])
    return ndvi

# export the latitude, longitude and array
def LatLonImg(img, area):

    img = img.addBands(ee.Image.pixelLonLat())

    img = img.reduceRegion(reducer=ee.Reducer.toList(),\
                                        geometry=area,\
                                        maxPixels=1e13,\
                                        scale=10);

    data = np.array((ee.Array(img.get("result")).getInfo()))
    lats = np.array((ee.Array(img.get("latitude")).getInfo()))
    lons = np.array((ee.Array(img.get("longitude")).getInfo()))
    return lats, lons, data


# covert the lat, lon and array into an image
def toImage(lats,lons,data):

    # get the unique coordinates
    uniqueLats = np.unique(lats)
    uniqueLons = np.unique(lons)

    # get number of columns and rows from coordinates
    ncols = len(uniqueLons)
    nrows = len(uniqueLats)

    # determine pixelsizes
    ys = uniqueLats[1] - uniqueLats[0]
    xs = uniqueLons[1] - uniqueLons[0]

    # create an array with dimensions of image
    arr = np.zeros([nrows, ncols], np.float32) #-9999

    # fill the array with values
    counter =0
    for y in range(0,len(arr),1):
        for x in range(0,len(arr[0]),1):
            if lats[counter] == uniqueLats[y] and lons[counter] == uniqueLons[x] and counter < len(lats)-1:
                counter+=1
                arr[len(uniqueLats)-1-y,x] = data[counter] # we start from lower left corner
    return arr
    

def runAnalysis(collection, platform, score_type, savepath, area, plot):
    
    # map over the image collection
    if platform == "SENTINEL2":
        myCollection  = collection.map(ndvi_S2)
    elif platform == "LANDSAT":
        myCollection = collection.map(ndvi_LANDSAT)
    elif platform == "MODIS":
        myCollection = collection
    
    # get the median
    result = ee.Image(myCollection.mean()).rename(['result'])
    
    # get the lon, lat and result as 1d array
    lat, lon, data = LatLonImg(result, area)
    
    # 1d to 2d array
    image  = toImage(lat,lon,data)
    if score_type == "count":
        ndvi_score = (np.size(image[image>0.5])/np.size(image))*100
    elif score_type == "median":
        ndvi_score = np.median(image)*100
    elif score_type == "mean":
        ndvi_score = np.mean(image)*100

    print("NDVI score = ",ndvi_score)

    if plot:
        import matplotlib.pyplot as plt
        plt.imshow(image)
        plt.colorbar()
        print("saveing to {}".format(str(savepath+'image_ndvi.jpg')))
        plt.savefig(str(savepath+'/image_ndvi.jpg'))
    
    return ndvi_score



def update_json(file_path, ndvi_score):
    
    with open(str(file_path)) as json_in_file:
        data = json.load(json_in_file)
        data["data"][0]["number"] = str(int(ndvi_score))
    
    with open(str(file_path), 'w') as json_out_file:
        json.dump(data, json_out_file, indent = 4)
    
    return


def commit_and_push(file_path, commit_message):
    """
    requires git personal access token to be provided in .env file
    or set as environment variable in shell
    """

    current_path = os.getcwd()
    path_to_repo = '/home/joe/Code/jmcook1186.github.io'
    os.chdir(path_to_repo)
    
    g= Github(os.environ["GIT_TOKEN"])
    repo = Repo(path_to_repo)
    
    repo.index.add(file_path)
    repo.index.commit(commit_message)
    origin = repo.remote('origin')
    origin.push()

    os.chdir(current_path)

    return


