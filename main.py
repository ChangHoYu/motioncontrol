import cv2
import mediapipe as mp
import pyautogui
import serial
import time

py_serial = serial.Serial(

    port='COM3',

    baudrate=9600,
)

x1 = y1 = x2= y2 = x3 = y3 = x4 = y4 = 0
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FPS, 1)
fps = cam.get(cv2.CAP_PROP_FRAME_COUNT)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

active = 0
mode = ''
brightness = 255
def putText(mode, loc=(500, 100), color=(0, 0, 0)):
    cv2.putText(frame, str(mode), loc, cv2.FONT_HERSHEY_COMPLEX, 1, color, 3)

while cam.isOpened():
    check, frame = cam.read()
    frame = cv2.flip(frame, 1)
    commend = ''
    finger = [0, 0, 0]

    if not check:
        break

    frame_width, frame_height, _ = frame.shape
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            # for _ in range(3):
            #     print(landmarks[0].x)
            
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_height)
                y = int(landmark.y * frame_width)

                if id == 8 :
                    # cv2.circle(img=frame, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y
                    

                if id == 4:
                    # cv2.circle(img=frame, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                    x2 = x
                    y2 = y
                    
                
                if id == 12:
                    x3 = x
                    y3 = y
                
                if id == 0 :
                    x4 = x
                    y4 = y

        light_control = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (0.5) // 4
        volume_control_check = ((x3 - x1) ** 2 + (y3 - y1) ** 2) ** (0.5) // 4 
        volume_control = ((x4 - x3) ** 2 + (y4 - y3) ** 2) ** (0.5) // 4

        # cv2.line(frame, (x1,y1), (x2,y2), (0,255, 255), 4, 1)

        # if dist > 30 :
        #     pyautogui.press('volumeup')
        #     putText('volume up')qqqqq
        # else :
        #     pyautogui.press('volumedown')
        #     putText('volume down')

        if volume_control_check < 20 :
            finger[0] = 1
        else :
            finger[0] = 0
        
        if light_control < 10 :
            finger[1] = 1
            
        elif light_control > 100:
            finger[2] = 1

        
        print(light_control)
        print(mode)
        if finger[1] == 1 and  active == 0 :
            mode = 'light on'
            active = 1
            commend = 'a'
            commend = commend.encode('utf-8')
            py_serial.write(commend)
        elif finger[2] == 1 and active == 1:
            mode = 'light off'
            active = 0
            putText(mode)
            commend = 'b'
            commend = commend.encode('utf-8')
            py_serial.write(commend)    
        
            
        if  active == 1 :
            if finger[0] == 1 and finger[1] == 0 :
                if volume_control < 70 :
                    mode = 'light down'
                    putText(mode)
                    commend = 'd'
                    commend = commend.encode('utf-8')
                    py_serial.write(commend)
                        # brightness -= 1
                else:
                    mode = 'light up'
                    putText(mode)
                    commend = 'u'
                    commend = commend.encode('utf-8')
                    py_serial.write(commend) 
                
                    #     if brightness >=255 :
                    #         pass
                    #     else :
                    #         brightness += 1
                    # brightness = str(brightness)
                    # py_serial.write(brightness) 
        
            
            # if mode == 'light on' and active == 1:
            #     if finger[0] == 1 and finger[1] == 0 :
            #         if volume_control < 70 :
            #             mode = 'light down'
            #             putText(mode)
            #             pyautogui.press('volumedown')
            #         else :
            #             mode = 'light up'
            #             putText(mode)
            #             pyautogui.press('volumeup')
        # elif finger[0] == 0 and finger[1] == 1 and active == 1 :
        #     mode = 'light off'
        #     putText(mode)

        #     commend = 'b'
        #     commend = commend.encode('utf-8')

        #     py_serial.write(commend)

            
            

            

        


    cv2.imshow('test', frame)

    if cv2.waitKey(25) == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()
