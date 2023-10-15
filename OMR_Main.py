import cv2
import numpy as np
import utlis


########################################################################
webCamFeed = True
pathImage = "pic1.png"
cap = cv2.VideoCapture(0)
cap.set(10,160)
heightImg =  1080 #540 # 794 - for A4 aspect ratio
widthImg  =  1920 #960 # 1123 - for A4 aspect ratio
questions = 20
choices = 15
ansDict = {1: 'C', 2: 'A', 3: 'A', 4: 'A', 5: 'B', 6: 'A', 7: 'A', 8: 'A', 9: 'B', 10: 'A', 11: 'C', 12: 'D', 13: 'C', 14: 'B', 15: 'A', 16: 'B', 17: 'B', 18: 'B', 19: 'B', 20: 'B', 21: 'A', 22: 'B', 23: 'C', 24: 'D', 25: 'C', 26: 'B', 27: 'A', 28: 'B', 29: 'C', 30: 'D', 31: 'B', 32: 'C', 33: 'C', 34: 'B', 35: 'A', 36: 'B', 37: 'C', 38: 'D', 39: 'D', 40: 'D', 41: 'A', 42: 'A', 43: 'B', 44: 'C', 45: 'D', 46: 'C', 47: 'B', 48: 'A', 49: 'A', 50: 'A'}
########################################################################


items_match=0

while True:

    if webCamFeed:success, img = cap.read()
    else:img = cv2.imread(pathImage)
    img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
    imgFinal = img.copy()
    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
    imgCanny = cv2.Canny(imgBlur,10,70) # APPLY CANNY 

    try:
        ## FIND ALL COUNTOURS
        imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
        rectCon = utlis.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
        biggestPoints= utlis.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
        gradePoints = utlis.getCornerPoints(rectCon[1]) # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE
        

        if biggestPoints.size != 0 and gradePoints.size != 0:

            # BIGGEST RECTANGLE WARPING
            biggestPoints=utlis.reorder(biggestPoints) # REORDER FOR WARPING
            cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
            pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
            # imgWarpColoredResizedJL = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE
            # imgWarpColored = cv2.resize(imgWarpColoredResizedJL, (794, 1123)) # RESIZE TO A4 RATIO JL
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE
            # cv2.imshow('Birds-eye-view', imgWarpColored)

            # SECOND BIGGEST RECTANGLE WARPING
            cv2.drawContours(imgBigContour, gradePoints, -1, (255, 0, 0), 20) # DRAW THE BIGGEST CONTOUR
            gradePoints = utlis.reorder(gradePoints) # REORDER FOR WARPING
            ptsG1 = np.float32(gradePoints)  # PREPARE POINTS FOR WARP
            ptsG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])  # PREPARE POINTS FOR WARP
            matrixG = cv2.getPerspectiveTransform(ptsG1, ptsG2)# GET TRANSFORMATION MATRIX
            imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150)) # APPLY WARP PERSPECTIVE
            # cv2.imshow('Grade', imgGradeDisplay)

            # APPLY THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
            imgThresh = cv2.threshold(imgWarpGray, 100, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE
            # cv2.imshow('Inverse-color', imgThresh)

            boxes = utlis.splitBoxes(imgThresh) # GET INDIVIDUAL BOXES                      
            # cv2.imshow('Split Test ', boxes[17])
            countR=0
            countC=0
            myPixelVal = np.zeros((questions,choices)) # TO STORE THE NON ZERO VALUES OF EACH BOX
            for image in boxes:
                # cv2.imshow(str(countR)+str(countC),image)
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC]= totalPixels
                countC += 1
                if (countC==choices):countC=0;countR +=1

            # FIND THE USER ANSWERS AND PUT THEM IN A LIST
            myIndex=[]
            for x in range (0,questions):
                arr = myPixelVal[x]
                myIndexVal = np.where(arr >= (np.amax(arr))-900)
                myIndex.append(myIndexVal)
            # myIndexHackTry = utlis.cleanedListForGrading(myIndex)
            # print(f'myIndex: {myIndex}')
            # print(f'myIndexHackTry: {myIndexHackTry}')

            # JL convert to dictionary
            cleanedList = utlis.reformatAnswers(myIndex)
            answersDictFormat = utlis.sortReformattedAnswers(cleanedList) 
            print(f'Answers-Dict: {answersDictFormat}')

            # Rename dicts
            dict_a = ansDict
            dict_b = answersDictFormat
            grading = []

            # Initialize a counter
            items_match = 0

            # Iterate through keys in dict_a
            for key, value_a in dict_a.items():
                # Check if the key exists in dict_b and has the same value
                if key in dict_b and dict_b[key] == value_a:
                    items_match += 1
                    grading.append(1)
                else:
                    grading.append(0)
            print(f'Grading: {grading}')

            # Print the count of keys with the same values in both dictionaries
            # print("Match values: ", items_match)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            score = items_match # FINAL GRADE
            print(f'Score: {score}')

            # DISPLAYING ANSWERS
            # JL remake index for grading
            myIndex = utlis.cleanedListForGrading(myIndex)
            # print(f'myIndex: {myIndex}')
            ans = [[2, 6], [3, 7], [4, 8], [3, 9], [2, 8], [3, 7], [4, 6], [2, 7], [2, 8], [3, 9], [3, 7, 11], [4, 7, 11], [3, 8, 12], [2, 7, 13], [1, 6, 14], [2, 7, 13], [2, 8, 12], [2, 9, 11], [2, 9, 11], [2, 9, 11]]

            # JL remake grading to match myIndex format // array of 20
            alignedGrading = utlis.alignGrading(grading)
            print(f'alignedGrading = {alignedGrading}')
            print(f'myIndex = {myIndex}') 
            print(f'ans = {ans}')

            utlis.showAnswers(imgWarpColored,myIndex,alignedGrading, ans) # DRAW DETECTED ANSWERS
            utlis.drawGrid(imgWarpColored) # DRAW GRID
            imgRawDrawings = np.zeros_like(imgWarpColored) # NEW BLANK IMAGE WITH WARP IMAGE SIZE
            utlis.showAnswers(imgRawDrawings, myIndex, alignedGrading, ans) # DRAW ON NEW IMAGE
            invMatrix = cv2.getPerspectiveTransform(pts2, pts1) # INVERSE TRANSFORMATION MATRIX
            imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg)) # INV IMAGE WARP

            # DISPLAY GRADE
            imgRawGrade = np.zeros_like(imgGradeDisplay,np.uint8) # NEW BLANK IMAGE WITH GRADE AREA SIZE
            cv2.putText(imgRawGrade,str(int(score))+"/50",(10,100)
                        ,cv2.FONT_HERSHEY_COMPLEX,3,(0,255,255),3) # ADD THE GRADE TO NEW IMAGE
            invMatrixG = cv2.getPerspectiveTransform(ptsG2, ptsG1) # INVERSE TRANSFORMATION MATRIX
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg)) # INV IMAGE WARP

            # SHOW ANSWERS AND GRADE ON FINAL IMAGE
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1,0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1,0)

            # IMAGE ARRAY FOR DISPLAY
            imageArray = ([img,imgGray, imgCanny, imgContours],
                          [imgBigContour, imgThresh, imgWarpColored, imgFinal])
            cv2.imshow("Final Result", imgFinal)
    except:
        imageArray = ([img,imgGray,imgCanny,imgContours],
                      [imgBlank, imgBlank, imgBlank, imgBlank])

    # LABELS FOR DISPLAY
    lables = [["Original","Gray","Edges","Contours"],
              ["Biggest Contour","Threshold","Warpped","Final"]]

    stackedImage = utlis.stackImages(imageArray,0.5,lables)
    cv2.imshow("Result", stackedImage)

    # SAVE IMAGE WHEN 's' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Scanned/myImage"+str(items_match)+".jpg",imgFinal)
        cv2.rectangle(stackedImage, ((int(stackedImage.shape[1] / 2) - 230), int(stackedImage.shape[0] / 2) + 50),
                      (1100, 350), (0, 255, 0), cv2.FILLED)
        cv2.putText(stackedImage, "Scan Saved", (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)),
                    cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
        cv2.imshow('Result', stackedImage)
        cv2.waitKey(300)
        items_match += 1