import cv2
import time
import os
import HandTrackingModule as htm
from pynput.keyboard import Controller

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.75)

# Set up video capture
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# Load overlay images from the specified folder
folderpath = "folderlist"
myList = os.listdir(folderpath)

overlayList = []
for imPath in myList:
    image = cv2.imread(os.path.join(folderpath, imPath))
    if image is not None:
        overlayList.append(image)
    else:
        print(f"Failed to load image: {imPath}")

print(f"Number of loaded overlay images: {len(overlayList)}")

tipsIds = [4, 8, 12, 16, 20]
keyboard = Controller()
fistClosed = False

while True:
    # Read video frame
    success, img = cap.read()
    if not success:
        print("Failed to read frame from the video source.")
        break

    # Detect hands in the frame
    img = detector.findHands(img)
    imList = detector.findPosition(img, draw=False)
    fingers = []

    if len(imList) != 0:
        # Check thumb finger
        if imList[tipsIds[0]][1] < imList[tipsIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Check other fingers
        for id in range(1, 5):
            if imList[tipsIds[id]][2] < imList[tipsIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        print(f"Number of raised fingers: {totalFingers}")

        if totalFingers <= len(overlayList):
            # Overlay the corresponding image on top of the frame
            h, w, c = overlayList[totalFingers - 1].shape
            img[0:h, 0:w] = overlayList[totalFingers - 1]

            # Check if the fist is closed


    # Display the modified frame
    cv2.imshow("image", img)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
