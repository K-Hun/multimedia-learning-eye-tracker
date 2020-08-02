import matlab.engine
import numpy as np
import scipy.io
import cv2
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import \
    Axes3D  # This import has side effects required for the kwarg projection='3d' in the call to fig.add_subplot
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
from heapq import nlargest





def loadCSV(path):
    csv_file = open(path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    return csv_reader


def msToTimeStrFormat(ms):
    return str(timedelta(seconds=int(ms / 1000)))


def timeSubtraction(t1, t2):
    FMT = '%Y-%m-%d %H:%M:%S:%f'
    seconds = (datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)).seconds
    microseconds = (datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)).microseconds
    ms = (seconds*1000000 + microseconds)/1000
    return int(seconds*1000)

def getInterval(originTime, startTime, endTime):
    FMT = '%H:%M:%S'
    start = timeSubtraction(originTime, startTime)
    end = timeSubtraction(originTime, endTime)
    return [start, end]


def skip(startTime, csvReader):
    for j in range(0, startTime):
        next(csvReader)

# like: listOfNumbers = [1, 2, 3, 4, -1, 0.0, 0, 5], nanVlues= [-1, 0.0, 0], returns [1, 2, 3, 4, 5]
def removeNans(listOfNumbers, nanValues):
    cleanlist = []
    flag = True
    for element in listOfNumbers:
        flag = True
        for nan in nanValues:
            if element == nan:
                flag = False
                break
        if flag:
            cleanlist.append(element)
    return cleanlist

def averageList(listOfNumbers):
    if len(listOfNumbers) < 1:
        return 0.0
    else:
        return float(sum(listOfNumbers))/float(len(listOfNumbers))

def kMaxList(listOfnumbers, k):
    return nlargest(k, listOfnumbers)

def kMaxList(listOfnumbers, k):
    return nlargest(k, listOfnumbers)

def jointList(seperatedLists):
    joinedlist = []
    for sepList in seperatedLists:
        joinedlist = joinedlist + sepList

    return joinedlist

def extractFrames(video_location, start, end, saveLocation):
    vidcap = cv2.VideoCapture(video_location)
    per = 33.3333333333333333333333333333333333333333
    for i in range(start, end):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, int(i * per))
        success, image = vidcap.read()
        image = cv2.resize(image, (1280, 720))
        cv2.imwrite(saveLocation + "\\" + str(i) + ".jpg", image)

def isInPolygon(polygon, point):
    import matplotlib.path as mplPath
    crd = np.array(polygon)# poly
    bbPath = mplPath.Path(crd)
    pnts = [point] # points on edges
    r = 0.001 # accuracy
    isIn = [ bbPath.contains_point(pnt,radius=r) or bbPath.contains_point(pnt,radius=-r) for pnt in pnts]
    return isIn[0]


def lineChart(xlabel, ylabel,xarrays, yarray):
    import matplotlib.pyplot as plt
    plt.plot(yarray, 'o-')
    plt.xticks(xarrays)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

# duration: time slice in ms, numberOfFrames: total number of frames, return [[start1, end1, 'null'], [start2, end2, 'null'], ...]
# 'null' is the description of the block, it's not necessary at this time!
def getTimeSliceBlocksWithNumberOfFrames(duration, numberOfFrames):
    blocks = []
    secPerBlock = duration
    step = secPerBlock*30
    for i in range(0,numberOfFrames, step):
        if (i+step) < (numberOfFrames - 1):
            blocks.append([i, i + step,1, "null"])
        else:
            blocks.append([i, numberOfFrames,1, "null"])
    return blocks

def getTimeSliceBlocksWithNumberOfFramesWindowed(windowSize, overlap, numberOfFrames):
    blocks = []
    secPerBlock = windowSize
    step = secPerBlock*30
    gap = overlap*30
    start = 0
    end = step
    blocks.append([start, end, 1, "null"])
    while(end < numberOfFrames):
        start = start + gap
        end = end + gap
        if end > numberOfFrames:
            break
        blocks.append([start, end, 1, "null"])

    if blocks[len(blocks)-1][1] < numberOfFrames:
        blocks.append([end, numberOfFrames, 1, "null"])
    return blocks

def movingAverage(signal):
    N = 3
    cumsum, moving_aves = [0], []
    for o, x in enumerate(signal, 1):
        cumsum.append(cumsum[o-1] + x)
        if o>=N:
            moving_ave = (cumsum[o] - cumsum[o-N])/N
            #can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    return moving_aves

def interpZeros(signal):
    signal = np.array(signal)
    y = np.array(signal)
    if y[0] <= 0:
        y[0] = 1
    if y[len(y)-1] <= 0:
        y[len(y)-1] = 1
    x = np.arange(len(y))
    idx = np.where(y>0)        #or np.nonzero(y) -- thanks DanielF
    f = interp1d(x[idx],signal[idx])
    ynew = f(x)
    return ynew.tolist()
