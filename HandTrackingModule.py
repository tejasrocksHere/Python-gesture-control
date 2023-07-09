import  cv2
import mediapipe as mp
import  time

# class creation
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils # it gives small dots onhands total 20 landmark points

    def findHands(self,img,draw=True):
        # Send rgb image to hands
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB) # process the frame
    #     print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    #Draw dots and connect them
                    self.mpDraw.draw_landmarks(img,handLms,
                                                self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self,img, handNo=0, draw=True):


        lmlist = []

        # check wether any landmark was detected
        if self.results.multi_hand_landmarks:
            #Which hand are we talking about
            myHand = self.results.multi_hand_landmarks[handNo]
            # Get id number and landmark information
            for id, lm in enumerate(myHand.landmark):
                 # id will give id of landmark in exact index number
                # height width and channel
                h,w,c = img.shape
                #find the position
                cx,cy = int(lm.x*w), int(lm.y*h) #center
                # print(id,cx,cy)
                lmlist.append([id,cx,cy])

                # Draw circle for 0th landmark
                if draw:
                    cv2.circle(img,(cx,cy), 5 , (255,0,255), cv2.FILLED)

        return lmlist

def main():
   pass

if __name__ == "__main__":
    main()