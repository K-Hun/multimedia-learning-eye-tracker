import matlab.engine
import os
import utils
import numpy as np
import scipy.io
import cv2
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # This import has side effects required for the kwarg projection='3d' in the call to fig.add_subplot
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import simulations as sim



class EYEData:

    __path = ""
    __filePrefixName = ""
    __matlabEngine = 0
    __EYE_TRACKER_RECORD_START_TIME = ""

    __MULTIMEDIA_START_TIME = ""
    __MULTIMEDIA_END_TIME = ""

    __CENTER_TEST_START_TIME = ""
    __CENTER_TEST_END_TIME = ""

    __Q_TIMES = []
    __Q_ANS_TIMES = []
    __EXAM_FINISH = ""

    __MATLAB_BASE_TIME = 0
    __BIAS = 999
    matlabEngStarted = False

    answerSheet = []

    diffPupilSize = []
    aveFixationDurations = []
    fixationRate = []
    aveAmplitudes = []
    aveVelocities = []
    blinkRates = []
    aveBlinkLatencies = []
    aveMSAMP = []
    msRate = []
    name = ""
    fig = ''

    def __init__(self, data__path, __filePrefixName):
        self.matlabEngStarted = False
        self.diffPupilSize = []
        self.aveFixationDurations = []
        self.fixationRate = []
        self.aveAmplitudes = []
        self.aveVelocities = []
        self.answerSheet = []
        self.blinkRates = []
        self.aveBlinkLatencies = []
        self.aveMSAMP = []
        self.msRate = []
        fig = ''
        self.__path = data__path
        self.__filePrefixName = __filePrefixName
        self.__initLogConstatns()
        self.__extractAnswerSheet()

        if os.path.exists(self.__path+"/"+self.__filePrefixName+"_gazes.csv") == False:
            self.__startMatlabEng()
            self.__matlabEngine.getGazes(nargout=0)
        else:
            print(self.__filePrefixName+"_gazes.csv"+" is already generated!")

        if os.path.exists(self.__path+"/"+self.__filePrefixName+"_fixations.csv") == False:
            self.__startMatlabEng()
            self.__matlabEngine.getFixations(nargout=0)
        else:
            print(self.__filePrefixName+"_fixations.csv"+" is already generated!")

        if os.path.exists(self.__path+"/"+self.__filePrefixName+"_saccades.csv") == False:
            self.__startMatlabEng()
            self.__matlabEngine.getSaccades(nargout=0)
        else:
            print(self.__filePrefixName+"_saccades.csv"+" is already generated!")

        if os.path.exists(self.__path+"/"+self.__filePrefixName+"_blinks.csv") == False:
            self.__startMatlabEng()
            self.__matlabEngine.getBlinks(nargout=0)
        else:
            print(self.__filePrefixName+"_blinks.csv"+" is already generated!")

        if os.path.exists(self.__path+"/"+self.__filePrefixName+"_microsaccades.csv") == False:
            self.__startMatlabEng()
            self.__matlabEngine.getMicrosaccades(nargout=0)
        else:
            print(self.__filePrefixName+"_microsaccades.csv"+" is already generated!")

        print("init function")

    def __startMatlabEng(self):
        if(self.matlabEngStarted == False):
            self.__matlabEngine = matlab.engine.start_matlab()
            self.__loadMatlabWorkspace()
            self.__matlabEngine.workspace['path'] = self.__path
            self.__matlabEngine.workspace['filePrefixName'] = self.__filePrefixName
            self.__matlabEngine.initEDF(nargout=0)
            self.matlabEngStarted = True

    def __initLogConstatns(self):
        file__path = self.__path + "/" + self.__filePrefixName + ".txt"
        firstLineRead = False
        questionPointer = 1
        self.__Q_TIMES = []
        visited = ""
        for i in range(12):
            self.__Q_TIMES.append([])
            self.__Q_ANS_TIMES.append("")
        with open(file__path , "r") as ins:
            for line in ins:
                if firstLineRead != True:
                    self.__EYE_TRACKER_RECORD_START_TIME = line.replace("\n","")
                    firstLineRead = True

                if line.startswith("MUL_START"):
                    self.__MULTIMEDIA_START_TIME = line.replace("\n","").split(" @ ")[1]

                elif line.startswith("MUL_END"):
                    self.__MULTIMEDIA_END_TIME = line.replace("\n","").split(" @ ")[1]

                elif line.startswith("CENTER_TEST_START"):
                    self.__CENTER_TEST_START_TIME = line.replace("\n","").split(" @ ")[1]

                elif line.startswith("CENTER_TEST_END"):
                    self.__CENTER_TEST_END_TIME = line.replace("\n","").split(" @ ")[1]

                if line.startswith("Q_"):
                    qNumber = int(line.replace("\n","").split("_")[1].split(" @")[0])
                    timeLog = line.replace("\n","").split(" @ ")[1]
                    if visited == qNumber:
                        continue
                    if qNumber == questionPointer:
                        self.__Q_TIMES[questionPointer-1].append(timeLog)
                    else:
                        self.__Q_TIMES[questionPointer-1].append(timeLog)
                        questionPointer = qNumber
                        self.__Q_TIMES[questionPointer-1].append(timeLog)
                    visited = qNumber

                if line.startswith("QS_FINISH_"):
                    self.__Q_TIMES[questionPointer-1].append(line.replace("\n","").split(" @ ")[1])
                    self.__EXAM_FINISH = line.replace("\n","").split(" @ ")[1]

                if line.startswith("QANS"):
                    qNumber = int(line.replace("\n","").split("QANS_")[1].split("_")[0])
                    self.__Q_ANS_TIMES[qNumber-1] = line.replace("\n","").split(" @ ")[1]


    def __getGazes(self, originTime, startTime, endTime):
        start , end = utils.getInterval(originTime, startTime, endTime)
        csv_reader = utils.loadCSV(self.__path + "/" + self.__filePrefixName + "_gazes.csv")
        start = start + self.__BIAS
        end = end + self.__BIAS
        utils.skip(start,csv_reader)
        xs = []
        ys = []
        pupilSizes = []
        for i in range(end - start):
            row = next(csv_reader)

            x = row[0]
            if x != 'NaN':
                xs.append(float(x))
            else:
                xs.append(-1)

            y = row[1]
            if y != 'NaN':
                ys.append(float(y))
            else:
                ys.append(-1)

            pupilSize = row[2]
            if pupilSize != 'NaN':
                pupilSizes.append(float(pupilSize))
            else:
                pupilSizes.append(-1)
        #MOVING AVERAGE TO REDUCE THE EFFECTS OF OUTLIERS

        pupilSizes = utils.interpZeros(pupilSizes)
        realLen = len(pupilSizes)
        pupilSizes = utils.movingAverage(pupilSizes)
        diffLen = realLen - len(pupilSizes)
        if diffLen > 0:
            for i in range(diffLen):
                pupilSizes.append(-1)
        return [xs, ys, pupilSizes]

    def __getFixations(self, originTime, startTime, endTime):
        start , end = utils.getInterval(originTime, startTime, endTime)
        csv_reader = utils.loadCSV(self.__path + "/" + self.__filePrefixName + "_fixations.csv")
        start = start + self.__BIAS
        end = end + self.__BIAS
        starts = []
        ends = []
        xs = []
        ys = []
        pupilSizes = []
        while True:
            row = next(csv_reader)
            s = float(row[0])
            e = float(row[1])
            if s < start:
                continue
            if e > end:
                break
            starts.append(s - start)
            ends.append(e - start)
            x = row[2]
            if x != 'NaN':
                xs.append(float(x))
            else:
                xs.append(-1)
            y = row[3]
            if y != 'NaN':
                ys.append(float(y))
            else:
                ys.append(-1)
            pupilSize = row[4]
            if pupilSize != 'NaN':
                pupilSizes.append(float(pupilSize))
            else:
                pupilSizes.append(-1)
        return [starts, ends, xs, ys, pupilSizes]

    def __getSaccades(self, originTime, startTime, endTime):
        start , end = utils.getInterval(originTime, startTime, endTime)
        csv_reader = utils.loadCSV(self.__path + "/" + self.__filePrefixName + "_saccades.csv")
        start = start + self.__BIAS
        end = end + self.__BIAS
        starts = []
        ends = []
        xs = []
        ys = []
        xEnds = []
        yEnds = []
        hypots = []
        pvels = []
        while True:
            row = next(csv_reader)
            s = float(row[0])
            e = float(row[1])
            if s < start:
                continue
            if e > end:
                break
            starts.append(s - start)
            ends.append(e - start)
            x = row[2]
            if x != 'NaN':
                xs.append(float(x))
            else:
                xs.append(-1)
            y = row[3]
            if y != 'NaN':
                ys.append(float(y))
            else:
                ys.append(-1)
            xEnd = row[4]
            if xEnd != 'NaN':
                xEnds.append(float(xEnd))
            else:
                xEnds.append(-1)
            yEnd = row[5]
            if yEnd != 'NaN':
                yEnds.append(float(yEnd))
            else:
                ys.append(-1)
            hypot = row[6]
            if hypot != 'NaN':
                hypots.append(float(hypot))
            else:
                hypots.append(-1)
            pvel = row[7]
            if pvel != 'NaN':
                pvels.append(float(pvel))
            else:
                ys.append(-1)
        return [starts, ends, xs, ys, xEnds, yEnds, hypots, pvels]

    def __getMicrosaccades(self, originTime, startTime, endTime):
        start , end = utils.getInterval(originTime, startTime, endTime)
        csv_reader = utils.loadCSV(self.__path + "/" + self.__filePrefixName + "_microsaccades.csv")
        start = start + self.__BIAS
        end = end + self.__BIAS
        starts = []
        ends = []
        vPeaks = []
        amplitudes = []
        while True:
            row = next(csv_reader)
            s = float(row[0])
            e = float(row[1])
            if s < start:
                continue
            if e > end:
                break
            starts.append(s - start)
            ends.append(e - start)
            vPeak = row[2]
            if vPeak != 'NaN':
                vPeaks.append(float(vPeak))
            else:
                vPeaks.append(-1)
            amp = row[3]
            if amp != 'NaN':
                amplitudes.append(float(amp))
            else:
                amplitudes.append(-1)

        return [starts, ends, vPeaks, amplitudes]

    def __getBlinks(self, originTime, startTime, endTime):
        start, end = utils.getInterval(originTime, startTime, endTime)
        csv_reader = utils.loadCSV(self.__path + "/" + self.__filePrefixName + "_blinks.csv")
        start = start + self.__BIAS
        end = end + self.__BIAS
        starts = []
        ends = []
        while True:
            row = next(csv_reader)
            s = float(row[0])
            e = float(row[1])
            if s < start:
                continue
            if e > end:
                break
            starts.append(s - start)
            ends.append(e - start)

        return [starts, ends]

    def __loadMatlabWorkspace(self):
        self.__matlabEngine.createWorkspace(nargout=0)

    def getCenterTestGazes(self):
        return self.__getGazes(self.__EYE_TRACKER_RECORD_START_TIME, self.__CENTER_TEST_START_TIME, self.__CENTER_TEST_END_TIME)

    def getMultimediaGazes(self):
        return self.__getGazes(self.__EYE_TRACKER_RECORD_START_TIME, self.__MULTIMEDIA_START_TIME, self.__MULTIMEDIA_END_TIME)

    def getMultimediaFixations(self):
        return self.__getFixations(self.__EYE_TRACKER_RECORD_START_TIME, self.__MULTIMEDIA_START_TIME, self.__MULTIMEDIA_END_TIME)

    def getMultimediaSaccades(self):
        return self.__getSaccades(self.__EYE_TRACKER_RECORD_START_TIME, self.__MULTIMEDIA_START_TIME, self.__MULTIMEDIA_END_TIME)

    def getMultimediaMicrosaccades(self):
        return self.__getMicrosaccades(self.__EYE_TRACKER_RECORD_START_TIME, self.__MULTIMEDIA_START_TIME, self.__MULTIMEDIA_END_TIME)

    def getMultimediaBlinks(self):
        return self.__getBlinks(self.__EYE_TRACKER_RECORD_START_TIME, self.__MULTIMEDIA_START_TIME, self.__MULTIMEDIA_END_TIME)

    def getCroppedMultimediaPupilSizesPerFrames(self, start, end):
        xs, ys, pupilSizes = self.getMultimediaGazes()
        croppedPupilSizes = []
        for i in range(start, end):
            for j in range(int(i*33.333333333333333333333),int((i+1)*33.333333333333333333333)):
                croppedPupilSizes.append(int(pupilSizes[j]))

        return croppedPupilSizes

    def getCroppedMultimediaFixationsPerFrames(self, start, end):
        per = 33.33333333333333333333
        starts, ends, xs, ys, pupilSizes = self.getMultimediaFixations()
        start = int(start*per)
        end = int(end*per)
        durations = []
        for i in range(len(xs)):
            s = int(starts[i])
            e = int(ends[i])
            duration = int(float(ends[i])-float(starts[i]))
            if s < start:
                continue
            if e > end:
                break
            durations.append(duration)
        return durations

    def getCroppedMultimediaSaccadesPerFrames(self, start, end):
        per = 33.33333333333333333333
        starts, ends, xs, ys, xs2, ys2, ampls, pvles = self.getMultimediaSaccades()
        start = int(start*per)
        end = int(end*per)
        amplitudes = []
        peakVelocities = []
        for i in range(len(xs)):
            s = int(starts[i])
            e = int(ends[i])
            if s < start:
                continue
            if e > end:
                break
            amplitudes.append(float(ampls[i]))
            peakVelocities.append(float(pvles[i]))
        return [amplitudes, peakVelocities]

    def getCroppedMultimediaMicrosaccadesPerFrames(self, start, end):
        per = 33.33333333333333333333
        starts, ends, vPks, ampls = self.getMultimediaMicrosaccades()
        start = int(start*per)
        end = int(end*per)
        amplitudes = []
        vPeaks = []
        for i in range(len(starts)):
            s = int(starts[i])
            e = int(ends[i])
            if s < start:
                continue
            if e > end:
                break
            amplitudes.append(float(ampls[i]))
            vPeaks.append(float(vPks[i]))
        return [vPeaks, amplitudes]

    def getCroppedMultimediaBlinksPerFrames(self, start, end):
        per = 33.33333333333333333333
        starts, ends = self.getMultimediaBlinks()
        start = int(start*per)
        end = int(end*per)
        durations = []
        for i in range(len(starts)):
            s = int(starts[i])
            e = int(ends[i])
            if s < start:
                continue
            if e > end:
                break
            durations.append(int(float(ends[i]) - float(starts[i])))
        return durations

    # returns [ [], [], [], ... ]
    def getQuestionGazes(self, numOfQ):
        gazes = []
        for i in range(0,len(self.__Q_TIMES[numOfQ-1]),2):
            gazes.append(self.__getGazes(self.__EYE_TRACKER_RECORD_START_TIME, self.__Q_TIMES[numOfQ-1][i], self.__Q_TIMES[numOfQ-1][i+1]))
        return gazes

    # returns [ [], [], [], ... ]
    def getQuestionFixations(self, numOfQ):
        fixations = []
        for i in range(0,len(self.__Q_TIMES[numOfQ-1]),2):
            fixations.append(self.__getFixations(self.__EYE_TRACKER_RECORD_START_TIME, self.__Q_TIMES[numOfQ-1][i], self.__Q_TIMES[numOfQ-1][i+1]))
        return fixations

    # returns [ [], [], [], ... ]
    def getQuestionSaccades(self, numOfQ):
        saccades = []
        for i in range(0,len(self.__Q_TIMES[numOfQ-1]),2):
            saccades.append(self.__getSaccades(self.__EYE_TRACKER_RECORD_START_TIME, self.__Q_TIMES[numOfQ-1][i], self.__Q_TIMES[numOfQ-1][i+1]))
        return saccades

    # returns [ [], [], [], ... ]
    def getQuestionMicrosaccades(self, numOfQ):
        ms = []
        for i in range(0,len(self.__Q_TIMES[numOfQ-1]),2):
            ms.append(self.__getMicrosaccades(self.__EYE_TRACKER_RECORD_START_TIME, self.__Q_TIMES[numOfQ-1][i], self.__Q_TIMES[numOfQ-1][i+1]))
        return ms

    # returns [ [], [], [], ... ]
    def getQuestionBlinks(self, numOfQ):
        blinks = []
        for i in range(0,len(self.__Q_TIMES[numOfQ-1]),2):
            blinks.append(self.__getBlinks(self.__EYE_TRACKER_RECORD_START_TIME, self.__Q_TIMES[numOfQ-1][i], self.__Q_TIMES[numOfQ-1][i+1]))
        return blinks

    # duration in ms, from the moment the subject had started the question to the moment he/she answered it.
    def getQuestionRT(self, numOfQ):
        return utils.timeSubtraction(self.__Q_TIMES[numOfQ-1][0], self.__Q_ANS_TIMES[numOfQ-1])

    # total time spent on the question in ms.
    def getQuestionTotalTimeSpent(self, numOfQ):
        sumofSpent = 0
        for i in range(0,len(self.__Q_TIMES[numOfQ-1]),2):
            sumofSpent = sumofSpent + utils.timeSubtraction(self.__Q_TIMES[numOfQ-1][i], self.__Q_TIMES[numOfQ-1][i+1])
        return sumofSpent

    # returns dwell time in ms, fixations: [ [], [], [], ... ], ROIs:[ [], [], [], ... ]
    def dwell(self, fixations, ROIs, x_bias = 0, y_bias = 0):
        dwellTime = 0
        for fix in fixations:
            starts, ends, xs, ys, pupilSizes = fix
            for i in range(len(starts)):
                for roi in ROIs:
                    if(utils.isInPolygon(roi, [xs[i]+x_bias, ys[i]+y_bias])):
                        dwellTime = dwellTime + (ends[i] - starts[i])
        return dwellTime

    def entry(self, fixations, ROIs, x_bias = 0, y_bias = 0):
        entry = 999999
        for fix in fixations:
            starts, ends, xs, ys, pupilSizes = fix
            for i in range(len(starts)):
                for roi in ROIs:
                    if(utils.isInPolygon(roi, [xs[i]+x_bias, ys[i]+y_bias])):
                        return starts[i]
        return entry

    # ATTENTION: FROM the ROI to (All_AREAs - the ROI)
    def transition(self, fixations, ROIs, x_bias = 0, y_bias = 0):
        hit = False
        count = 0
        for fix in fixations:
            starts, ends, xs, ys, pupilSizes = fix
            for i in range(len(starts)):
                for roi in ROIs:
                    if(utils.isInPolygon(roi, [xs[i]+x_bias, ys[i]+y_bias])):
                        if hit == False:
                            hit = True
                    else:
                        if hit == True:
                            count = count + 1
                            hit = False
        return count

    def getPerformanceTestDuration(self):
        return utils.timeSubtraction(self.__Q_TIMES[0][0], self.__EXAM_FINISH)

    def __extractAnswerSheet(self):
        file__path = self.__path + "/" + self.__filePrefixName + ".txt"
        nextLineRead = False
        with open(file__path , "r") as ins:
            for line in ins:
                if nextLineRead == True:
                    self.answerSheet = line.replace("\n","").split('\t')
                    return self.answerSheet

                if line.startswith("#ANSWESHEET:"):
                    nextLineRead = True

    def getAnswerSheet(self):
        return self.answerSheet

    def getPerformance(self, keys):
        answerSheet = self.getAnswerSheet()
        correctedAnswerSheet = []
        result = 0.0
        c = 0
        for i in range(len(answerSheet)):
            if int(answerSheet[i]) == int(keys[i]):
                correctedAnswerSheet.append("c")
                c = c + 1
            elif int(answerSheet[i]) == -1:
                correctedAnswerSheet.append("b")
            else:
                correctedAnswerSheet.append("w")
        result = round(float(c)/float(len(answerSheet))*100 , 2)

        return [result, correctedAnswerSheet]



'''
data_path = "sample_data"
filePrefixName = "6np_bavafa"
data = EYEData(data_path, filePrefixName)
gazes = data.getMultimediaGazes()
fixations = data.getMultimediaFixations()

'''

'''
image__path = "center_test.jpg"
sim.showHeatmapSingleFrameVideoWithGazeLocations(image__path, gazes, 3979, 4082)
'''

#print(data.getCroppedMultimediaPupilSizesPerFrames(0, 10241))
#print(data.getCroppedMultimediaFixationsPerFrames(0, 10241))
#print(data.getCroppedMultimediaSaccadesPerFrames(0, 10241))



