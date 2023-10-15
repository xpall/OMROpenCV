import cv2
import numpy as np

## TO STACK ALL THE IMAGES IN ONE WINDOW
def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) # REMOVE EXTRA BRACKET
    print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    print(add)
    print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] = myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]

    return myPointsNew

def rectContour(contours):

    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        print(area)
        if area > 600:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True)
    # print(len(rectCon))
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx

def splitBoxes(img):
    rows = np.vsplit(img,20)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,15)
        for box in cols:
            boxes.append(box)
    return boxes

def drawGrid(img,questions=20,choices=15):
    secW = int(img.shape[1]/15)
    secH = int(img.shape[0]/20)
    for i in range (0,20):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0),2)
        cv2.line(img, pt3, pt4, (255, 255, 0),2)

    return img

# JL SHOW ANSWERS (GREEN AND RED) 
def showAnswers(img,myIndex,grading,ans,questions=20,choices=15):
    secH = int(img.shape[0]/choices) 
    secW = int(img.shape[1]/questions) 

    for rows in range(0,questions):             # loop for twenty rows
        studentAnswer = myIndex[rows]           # get values per rows
        isItCorrect = grading[rows]
        correctAnswer = ans[rows]
        # print(f'studentAnswer={studentAnswer}')
        # print(f'isItCorrect={isItCorrect}')
        # print(f'correctAnswer={correctAnswer}')

        if range(len(studentAnswer) > 3):
            studentAnswer.pop(3)

        for circleIndex in range(len(studentAnswer)):                 # loop per values
            centerX = (studentAnswer[circleIndex] * secW) + secW // 2 
            centerY = (rows * secH) + secH // 2         
            # print(f'centerX={centerX}, index{circleIndex} of row{rows}')
            # print(f'centerY={centerY}, index{circleIndex} of row{rows}')
            # print(f'circleIndex={circleIndex}')

            if isItCorrect[circleIndex]==1: #if correct
                myColor = (0,255,0)
                #cv2.rectangle(img,(myAns*secW,x*secH),((myAns*secW)+secW,(x*secH)+secH),myColor,cv2.FILLED)
                cv2.circle(img,(centerX,centerY),30,myColor,cv2.FILLED)
            else:
                myColor = (0,0,255)
                #cv2.rectangle(img, (myAns * secW, x * secH), ((myAns * secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
                cv2.circle(img, (centerX, centerY), 30, myColor, cv2.FILLED)

                # CORRECT ANSWER
                myColor = (0, 255, 0)
                correctAns = correctAnswer[circleIndex]
                cv2.circle(img,((correctAns * secW)+secW//2, (rows * secH)+secH//2),
                20,myColor,cv2.FILLED)

# JL FUNCTIONS - ARRAY TO CLEAN LIST
def reformatAnswers(listOfUserAnswers):
    reformattedList = []
    for item in listOfUserAnswers:
        cleaned_item = item[0].tolist() if isinstance(item[0], np.ndarray) else item[0]
        reformattedList.append(cleaned_item)
    return reformattedList

def sortReformattedAnswers(cleanedList):
    sortedDict = {
                1: 'X', 2: 'X', 3: 'X', 4: 'X', 5: 'X',
                6: 'X', 7: 'X', 8: 'X', 9: 'X', 10: 'X',
                11: 'X', 12: 'X', 13: 'X', 14: 'X', 15: 'X', 
                16: 'X', 17: 'X', 18: 'X', 19: 'X', 20: 'X',
                21: 'X', 22: 'X', 23: 'X', 24: 'X', 25: 'X',
                26: 'X', 27: 'X', 28: 'X', 29: 'X', 30: 'X', 
                31: 'X', 32: 'X', 33: 'X', 34: 'X', 35: 'X', 
                36: 'X', 37: 'X', 38: 'X', 39: 'X', 40: 'X', 
                41: 'X', 42: 'X', 43: 'X', 44: 'X', 45: 'X', 
                46: 'X', 47: 'X', 48: 'X', 49: 'X', 50: 'X'
                }
    counter = 1
    for item in cleanedList:
        for i in item:
            if i <= 4:
                sortedDict[counter] = convertToMCQ(i)
            elif i <= 9:
                sortedDict[counter + 20] = convertToMCQ(i)
            elif i <= 14:
                sortedDict[counter + 30] = convertToMCQ(i)
        counter += 1
    sortedDict = dict(sorted(sortedDict.items()))
    return sortedDict

    # Convert to ABCD
def convertToMCQ(i):
    if i == 1 or i == 6 or i == 11:
        i = 'A'
    elif i == 2 or i == 7 or i == 12:
        i = 'B'
    elif i == 3 or i == 8 or i == 13:
        i = 'C'
    elif i == 4 or i == 9 or i == 14:
        i = 'D'
    else:
        i = 'X'
    return i

def cleanedListForGrading(dirty_list):
    cleanedList = []
    for item in dirty_list:
        removeTheWordArray = list(item[0])
        cleanedList.append(removeTheWordArray)
    return cleanedList

def alignGrading(grading):
    alignedGrades = [
        [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], 
        [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], 
        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
        [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
        ]
    rowNumber = 0
    itemNumber = 0
    for item in grading:
        if itemNumber < 20:
            alignedGrades[rowNumber][0] = item
            itemNumber += 1
            rowNumber += 1
        elif itemNumber < 40:
            alignedGrades[rowNumber - 20][1] = item
            itemNumber += 1
            rowNumber += 1
        else:
            alignedGrades[rowNumber - 30][2] = item
            rowNumber += 1
    return alignedGrades
