import cv2, os, sys
import numpy as np
import imutils as iu
import sudoku_solver as solver

class ocrClass:

    def __init__(self):
        samples = np.loadtxt('ml/generalsamples.data',np.float32)
        responses = np.loadtxt('ml/generalresponses.data',np.float32)
        responses = responses.reshape((responses.size,1))
        #.model uses kNearest to perform OCR
        self.model = cv2.ml.KNearest_create()
        self.model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    def getNumber(self, img):
        roi = cv2.resize(img, (25,35))
        roismall = roi.reshape((1,875))
        roismall = np.float32(roismall)
        retval, results, neigh_resp, dists = self.model.findNearest(roismall, 1)
        predictedNum = int(results[0][0])
        return predictedNum

class imageClass:

    def __init__(self):
        self.captured = []
        #.gray is the grayscale captured image
        self.gray = []
        #.thres is after adaptive thresholding is applied
        self.thresh = []
        #.contours contains information about the contours found in the image
        self.contours = []

        self.cuttedThresh = []
        self.cuttedOrig = []
        self.corners = np.array([])

    def captureAndCrop(self, img):
        
        height, width = img.shape[:2]
        if height > 800 or width > 800:
            if height > width:
                self.captured = iu.resize(img, height=800)
            else:
                self.captured = iu.resize(img, width=800)
        else:
            self.captured = img

        self.gray = cv2.cvtColor(self.captured, cv2.COLOR_BGR2GRAY)

        #noise removal with gaussian blur
        self.gray = cv2.GaussianBlur(self.gray,(5,5),0)
        #then do adaptive thresholding
        self.thresh = cv2.adaptiveThreshold(self.gray,255,1,1,11,5)

        #cv2.imwrite('out/threshSudoku.png', self.thresh)

        #find countours in threshold image
        _, contours, _ = cv2.findContours(self.thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        maxArea = 0
        biggest = None
        for i in contours:
            area = cv2.contourArea(i)
            if area > 40000:
                epsilon = 0.1*cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,epsilon,True)
                #cv2.drawContours(self.captured, [i], 0, (0,0,255), 1)
                if area > maxArea and len(approx)==4:
                    maxArea = area
                    biggest = i
                    self.corners = approx
                # print( area )

        if biggest is not None:        
            pts1 = np.float32(self.rotateCorners(self.corners))
            pts2 = np.float32([[0,0],[0,450],[450,0],[450,450]])

            M = cv2.getPerspectiveTransform(pts1,pts2)
            self.cuttedThresh = cv2.warpPerspective(self.thresh,M,(450,450))
            self.cuttedOrig = cv2.warpPerspective(self.captured,M,(450,450))

            #cv2.drawContours(self.captured, [biggest], 0, (0,255,0), 3)
            #cv2.imwrite('out/contour.png', self.captured)
            cv2.imwrite('out/cuttedThresh.png', self.cuttedThresh)
            return self.captured
        return None

    def readSudoku(self):

        img = np.zeros([450,450,3],dtype=np.uint8)
        sudoku = np.zeros([9,9],dtype=np.uint32)

        #thresh = cv2.adaptiveThreshold(self.cutted,255,1,1,3,1)
        #morph = cv2.morphologyEx(thresh,cv2.MORPH_ERODE,None,iterations = 0)
        _, contours,_ = cv2.findContours(self.cuttedThresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        ocr = ocrClass()
        fieldCount = 0

        for i in contours:
            area = cv2.contourArea(i)
            if area > 50:
                [x,y,w,h] = cv2.boundingRect(i)
                if h > 15 and h < 45 and w > 8 and w < 45:
                    fieldCount += 1
                    roi = self.cuttedThresh[y:y+h,x:x+w]
                    num = ocr.getNumber(roi)

                    sudox = int((x+(w/2))//50)
                    sudoy = int((y+(h/2))//50)
                    sudoku[sudoy][sudox] = num
                    #cv2.imwrite('out/fields/' + str(num) + '/' + str(fieldCount) +'.png', roi)
                    #cv2.drawContours(img, [i], 0, (255,255,255), 1)

        #cv2.imwrite('out/contours.png', img)
        #cv2.imwrite('out/thresh.png', thresh)
        #print ("%i numbers recognized"%fieldCount)
        #print ("sudoku:\n", sudoku)
        return sudoku

    def writeSudoku(self, sudoku):
        #solutionImg = np.zeros((450, 450, 4), dtype=np.uint8)

        solutionImg = cv2.cvtColor(self.cuttedOrig, cv2.COLOR_RGB2RGBA)
        #solutionImg = self.cuttedOrig

        for y in range(9):
            for x in range(9):
                num = sudoku[y][x]
                if num != 0:
                    sx = x * 50 + 15 
                    sy = y * 50 + 38
                    cv2.putText(solutionImg,str(num),(sx,sy), 0 , 1, (0,0,0, 255), 2, 2)

        cv2.imwrite("out/onlySolution.png", solutionImg)

        pts1 = np.float32(self.rotateCorners(self.corners))
        pts2 = np.float32([[0,0],[0,450],[450,0],[450,450]])

        M = cv2.getPerspectiveTransform(pts2,pts1)
        
        width, height = self.captured.shape[:2]
        
        solutionImg = cv2.warpPerspective(solutionImg,M,(height,width))

        solution = self.captured

        y1, y2 = 0,0 +solutionImg.shape[0]
        x1, x2 = 0,0 +solutionImg.shape[1]

        alpha_s = solutionImg[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            solution[y1:y2, x1:x2, c] = (alpha_s * solutionImg[:, :, c] +
                                      alpha_l * solution[y1:y2, x1:x2, c])

        return solution

    def invertSudoku(self, sudoku, solution):
        # set all values in the solution which were given in the start sudoku to 0
        for row in range(9):
            for val in range(9):
                if sudoku[row][val] != 0:
                    solution[row][val] = 0

        return solution

    def rotateCorners(self, corners):
        # rotates the values of corners always in the same order
        # top-left, bottom-left, top-right, bottom-right
        
        tl = None # top left
        bl = None # bottom left
        tr = None # top right
        br = None # bottom right

        # getting the tl and br by getting the smallest
        # and biggest sum of the corner tupel
        biggest = 0
        smallest = 1000000
        rest = []

        for corner in corners:
            added = corner[0][0] + corner[0][1]
            if added > biggest:
                biggest = added
                br = corner[0]
            if added < smallest:
                smallest = added
                tl = corner[0]

        # getting the bl and tr corners
        for corner in corners:
            if not np.array_equal(corner[0], br) and not np.array_equal(corner[0], tl):
                rest.append(corner[0])
        if len(rest) == 2:
            if rest[0][0] > rest[1][0]:
                bl = rest[1]
                tr = rest[0]
            else:
                bl = rest[0]
                tr = rest[1]

        #print ("top-left: %a"%tl)
        #print ("bottom-left: %a"%bl)
        #print ("top-right: %a"%tr)
        #print ("bottom-right: %a"%br)

        return [[tl], [bl], [tr], [br]]

def getSolvedImage(img):
    image = imageClass()
    if img is not None:
                sudoku = image.captureAndCrop(img)
                if sudoku is not None:
                    sudoku = image.readSudoku()
                    if sudoku is not None:
                        grid = solver.sudokuToGrid(sudoku)
                        solvedGrid = solver.solve(grid)
                        if solvedGrid:
                            solution = solver.gridToSudoku(solvedGrid)
                            inverted = image.invertSudoku(sudoku, solution)
                            frame = image.writeSudoku(inverted)
                            return frame
    return False

def main():
    scanFrameNumber = 5
    frameCount = 0

    image = imageClass()

    if sys.argv[1] == "cam":

        cv2.namedWindow("preview")
        vc = cv2.VideoCapture(0)

        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False

        while rval:
            img = image.captureAndCrop(frame)
            if img is not None:
                sudoku = image.readSudoku()
                if sudoku is not None:
                    grid = solver.sudokuToGrid(sudoku)
                    solvedGrid = solver.solve(grid)
                    if solvedGrid:
                        solution = solver.gridToSudoku(solvedGrid)
                        inverted = image.invertSudoku(sudoku, solution)
                        frame = image.writeSudoku(inverted)
                        cv2.imwrite("out/solution.png", frame)

            frame = iu.resize(frame, width=800)
            cv2.imshow("preview", frame)

            rval, frame = vc.read()
            frameCount += 1
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
        cv2.destroyWindow("preview")

    else:
        img = cv2.imread(sys.argv[1])

        solvedImg = getSolvedImage(img)

        #img = cv2.imread('out/cutted.png')
        cv2.imshow("ref",solvedImg)
        key = cv2.waitKey(0)
        if key == 27:
            sys.exit()

if __name__ == '__main__': main()










