import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)

        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)

            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 75), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0),5)
            return True
        else:
            return False



#webcam
# Default webcam index is 0
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4, 1080)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# create btns
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

buttonList = []

for x in range(4):
    for y in range(4):
        xpos = x*100 + 150
        ypos = y*100 + 150
        buttonList.append(Button((xpos,ypos), 100, 100, buttonListValues[y][x]))

# button1 =Button((150,150),100,100,"5")

# variables
myEquation = ''
delayCounter = 0


#loop
while True:
    #get image from web cam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # draw button
    cv2.rectangle(img, (150, 50), (150 + 400 , 50 + 100), (225, 225, 255), cv2.FILLED)
    cv2.rectangle(img, (150, 50), (150 + 400, 50 + 100), (50, 50, 50), 3)

    #clear button
    # cv2.rectangle(img, (150, 50), (150 + 400, 550 + 100), (225, 225, 255), cv2.FILLED)
    # cv2.rectangle(img, (150, 50), (150 + 400, 550 + 100), (50, 50, 50), 3)


    for button in buttonList:
        button.draw(img)

    # check for hand
    if hands:
        lmList = hands[0]['lmList']
        x1, y1 = lmList[8][:2]
        x2, y2 = lmList[12][:2]
        length, _, img = detector.findDistance((x1, y1), (x2, y2), img)
        # print(length)

        if length<60:
            for i, button in enumerate(buttonList):
                if button.checkClick(x1,y1) and delayCounter == 0:
                    # print(buttonListValues[int(i%4)][int(i/4)])
                    myValue = buttonListValues[int(i % 4)][int(i / 4)]
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1




        # length, _, img = detector.findDistance(lmList[8], lmList[12], img)


    # avoid duplicates
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # display the equation/ result
    cv2.putText(img, myEquation, (150 +20, 50 + 70), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)
    # cv2.putText(img, "CLEAR", (270, 620), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    #Display img
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)

    if key == ord('c'):
        myEquation = ''


