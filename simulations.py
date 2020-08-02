import matlab.engine
import numpy as np
import scipy.io
import cv2
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # This import has side effects required for the kwarg projection='3d' in the call to fig.add_subplot
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os
import utils
import heatmap as htmap


#------------------------------------</ per MSEC Simulation >------------------=----------------------------------------
def simulateRealTimeVideoWithGazeLocation(video_location, gazes, start, end, stepSize = 1):
    vidcap = cv2.VideoCapture(video_location)
    xs, ys, pupilSizes = gazes
    for i in range(start, end, stepSize):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, i)
        success, image = vidcap.read()
        image = cv2.resize(image, (1280, 720))
        x = int(xs[i])
        y = int(ys[i])-183
        cv2.circle(image, (x,y), 20, (255, 0, 0), -1)
        image = cv2.resize(image, (800, 600))
        cv2.imshow("showRealTimeVideoWithGazeLocation", image)
        cv2.waitKey(1)

def simulateFrameByFrameVideoWithGazeLocations(framesPath, gazes, start, end, waitKeySpeed = 1):
    frame_index = 1
    xs, ys, pupilSizes = gazes
    for i in range(start, end):
        image = cv2.imread(framesPath+"/"+str(i)+".jpg")
        for j in range(int((i)*33.333333333333333333333),int((i+1)*33.333333333333333333333)):
            x = int(xs[j])
            y = int(ys[j])-183
            cv2.circle(image,(x,y), 20, (255,0,0), -1)
        frame_index = frame_index + 1
        image = cv2.resize(image, (800, 600))
        cv2.imshow("showFrameByFrameVideoWithGazeLocations",image)
        cv2.waitKey(waitKeySpeed)

#------------------------------------</ per Fixation Simulation >-------------------------------------------------------
def simulateRealTimeVideoWithFixationLocation(video_location, fixations, start, end, stepSize = 1):
    vidcap = cv2.VideoCapture(video_location)
    starts, ends, xs, ys, pupilSizes = fixations
    for i in range(len(xs)):
        s = int(starts[i])
        e = int(ends[i])
        x = int(xs[i])
        y = int(ys[i])-183
        if s < start:
            continue
        if e > end:
            break
        for j in range(s, e, stepSize):
            vidcap.set(cv2.CAP_PROP_POS_MSEC, j)
            success, image = vidcap.read()
            image = cv2.resize(image, (1280, 720))
            cv2.circle(image, (x,y), 20, (255, 0, 0), -1)
            image = cv2.resize(image, (800, 600))
            cv2.imshow("showRealTimeVideoWithFixationLocation", image)
            cv2.waitKey(1)

def simulateFrameByFrameVideoWithFixationsLocations(video_location, fixations, start, end, stepSize, waitKeySpeed = 1):
    vidcap = cv2.VideoCapture(video_location)
    per = 33.33333333333333333333
    starts, ends, xs, ys, pupilSizes = fixations
    start = int(start*per)
    end = int(end*per)
    for i in range(len(xs)):
        s = int(starts[i])
        e = int(ends[i])
        x = int(xs[i])
        y = int(ys[i])-183
        if s < start:
            continue
        if e > end:
            break
        for j in range(s, e, stepSize):
            vidcap.set(cv2.CAP_PROP_POS_MSEC, j)
            success, image = vidcap.read()
            image = cv2.resize(image, (1280, 720))
            cv2.circle(image, (x,y), 20, (255, 0, 0), -1)
            image = cv2.resize(image, (800, 600))
            cv2.imshow("showRealTimeVideoWithFixationLocation", image)
            cv2.waitKey(waitKeySpeed)

def digitFormat(num):
    if num < 10:
        return '0000'+str(num)
    elif num < 100:
        return '000' + str(num)
    elif num < 1000:
        return '00' + str(num)
    elif num < 10000:
        return '0' + str(num)
    else:
        return str(num)

def fixationGray(video_location, fixations, start, end, stepSize, waitKeySpeed = 1):
    vidcap = cv2.VideoCapture(video_location)
    per = 33.33333333333333333333
    starts, ends, xs, ys, pupilSizes = fixations
    lenOfTimeline = int(per*(end - start))
    print(lenOfTimeline)

    timeline = []
    for i in range(lenOfTimeline):
        timeline.append([-1, -1, -1])


    start = int(start*per)
    end = int(end*per)


    for i in range(len(xs)):
        s = int(starts[i])
        e = int(ends[i])
        x = int(xs[i])
        y = int(ys[i])-183
        ps = int(pupilSizes[i])



        if s < start:
            continue
        if e > end:
            break

        for j in range(s, e, stepSize):
            timeline[j][0] = x
            timeline[j][1] = y
            timeline[j][2] = ps
    '''
    for i in range(1, end - start + 1):
        a = int((i-1)*per)
        b = int(i*per)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, b)
        success, image = vidcap.read()
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (1280, 720))
        for j in range(a, b):
            if timeline[j][2] > -1:
                cv2.circle(image, (timeline[j][0],timeline[j][1]), 20, (255, 0, 0), -1)

        cv2.imwrite("bimokh/"+digitFormat(i+1)+".png", image)
        #image = cv2.resize(image, (800, 600))
        #cv2.imshow("showRealTimeVideoWithFixationLocation", image)
        #cv2.waitKey(waitKeySpeed)
    '''
    return timeline






#------------------------------------</ Heatmap >-----------------------------------------------------------------------
def showHeatmapFrameByFrameVideoWithGazeLocations(framesPath, gazes, start, end, waitKeySpeed = 1):
    frame_index = 1
    xs, ys, pupilSizes = gazes
    for i in range(start, end):
        heat_points = []
        heat_img = htmap.Image.open(framesPath+"/"+str(i)+".jpg")
        for j in range(int((i)*33.333333333333333333333),int((i+1)*33.333333333333333333333)):
            x = int(xs[j])
            y = int(ys[j])-183
            heat_points.append((x, y))
        frame_index = frame_index + 1
        heatmapper = htmap.Heatmapper()
        heatmap = heatmapper.heatmap_on_img(heat_points, heat_img)
        heatmap.save('hello.png')
        image = cv2.imread("hello.png")
        image = cv2.resize(image, (800, 600))
        cv2.imshow("showFrameByFrameVideoWithGazeLocations",image)
        cv2.waitKey(waitKeySpeed)
        #os.remove("hello.png")

def showHeatmapSingleFrameVideoWithGazeLocations(imagePath, gazes, start, end, showEnabled = True, saveEnabled = False, saveName = 'test.png' , waitKeySpeed = 1):
    frame_index = 1
    xs, ys, pupilSizes = gazes
    heat_img = htmap.Image.open(imagePath)
    heat_points = []
    for i in range(start, end):
        for j in range(int((i)*33.333333333333333333333),int((i+1)*33.333333333333333333333)):
            x = int(xs[j])
            y = int(ys[j])-183
            heat_points.append((x, y))
        frame_index = frame_index + 1
    heatmapper = htmap.Heatmapper()
    heatmap = heatmapper.heatmap_on_img(heat_points, heat_img)
    heatmap.save('hello.png')
    image = cv2.imread("hello.png")
    if showEnabled:
        image = cv2.resize(image, (800, 600))
        cv2.imshow("showFrameByFrameVideoWithGazeLocations",image)
        cv2.waitKey(0)
    if saveEnabled:
        cv2.imwrite(saveName, image)

# use for questuon
def showHeatmap(imagePath, fixation, showEnabled = True, saveEnabled = False, saveName = 'test.png', x_bias = 0, y_bias = 0):
    starts, ends, xs, ys, pupilSizes = fixation
    image = cv2.imread(imagePath)
    heat_points = []
    for i in range(len(starts)):
        x = int(xs[i])
        y = int(ys[i])
        cv2.circle(image, (x+x_bias,y + y_bias), 10, (255, 0, 0), -1)
    if showEnabled:
        image = cv2.resize(image, (800, 600))
        cv2.imshow("heatmap",image)
        cv2.waitKey(0)
    if saveEnabled:
        cv2.imwrite(saveName, image)
        #os.remove("hello.png")

def showHeatmapRealtime(imagePath, fixation):
    starts, ends, xs, ys, pupilSizes = fixation
    heat_img = htmap.Image.open(imagePath)
    heat_points = []
    for i in range(len(starts)):
        x = int(xs[i])
        y = int(ys[i])

        heat_points.append((x, y))
        heatmapper = htmap.Heatmapper()
        heatmap = heatmapper.heatmap_on_img([(x, y)], heat_img)
        heatmap.save('hello.png')
        image = cv2.imread("hello.png")
        image = cv2.resize(image, (800, 600))
        cv2.imshow("heatmap",image)
        cv2.waitKey(0)


#------------------------------------</ non-Categorized >---------------------------------------------------------------
def simulateCenterTest(centerTestGazes, stepSize):
    xs, ys, pupilSizes = centerTestGazes
    for i in range(0, len(xs), stepSize):
        image = cv2.imread("center_test.jpg")
        x = int(xs[i])
        y = int(ys[i])
        cv2.circle(image,(x,y), 20, (255,0,0), -1)
        image = cv2.resize(image, (800, 600))
        cv2.imshow("CENTER TEST",image)
        print(str(i) + ": ("+str(x)+", "+str(y)+")")
        cv2.waitKey(33)

def Test():
    import EYEData
    data_path = "sample_data"
    filePrefixName = "11p_karimi"
    data = EYEData(data_path, filePrefixName)
    gazes = data.getMultimediaGazes()
    fixations = data.getMultimediaFixations()

    '''
    video_location = 'E:/Thesis/Video Files/Ch11/P/CH11_P_NQ_02.mkv'
    simulateRealTimeVideoWithGazeLocation(video_location, gazes, 0 , len(gazes[0]), 100)
    '''

    '''
    frames__path = "C:/Users/K Hun/Desktop/temp/Shabani/main_frames"
    simulateFrameByFrameVideoWithGazeLocations(frames__path, gazes, 0, 10241)
    '''

    '''
    video_location = 'E:/Thesis/Video Files/Ch11/P/CH11_P_NQ_02.mkv'
    simulateRealTimeVideoWithFixationLocation(video_location, fixations, 0 , len(gazes[0]), 100)
    '''

    '''
    video_location = 'E:/Thesis/Video Files/Ch11/P/CH11_P_NQ_02.mkv'
    simulateFrameByFrameVideoWithFixationsLocations(video_location, fixations, 3149 , 3392, 100)
    '''

    '''
    frames__path = "C:/Users/K Hun/Desktop/temp/Shabani/main_frames"
    sim.showHeatmapFrameByFrameVideoWithGazeLocations(frames__path, gazes, 3979, 4082)
    '''

    '''
    image__path = "C:/Users/K Hun/Desktop/temp/Shabani/main_frames/4082.jpg"
    sim.showHeatmapSingleFrameVideoWithGazeLocations(image__path, gazes, 3979, 4082)
    '''

    '''
    simulateCenterTest(data.getCenterTestGazes(), 1)
    '''


