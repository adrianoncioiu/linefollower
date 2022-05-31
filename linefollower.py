import RPi.GPIO as GPIO    
import cv2
import numpy as np

in1 = 4
in2 = 17
in3 = 27
in4 = 22
en1 = 23
en2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

p1 = GPIO.PWM(en1, 100)
p2 = GPIO.PWM(en2, 100)

p1.start(100)
p2.start(100)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

capture = cv2.VideoCapture(0)  
capture.set(3,320.0) #dimensiune
capture.set(4,240.0)  #dimensiune
capture.set(5,15)  #frame rate


while cv2.waitKey(1) != 27:
    flag, frame = capture.read() 
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    ret,th1 = cv2.threshold(blur,35,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret1,th2 = cv2.threshold(th1,127,255,cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
    cv2.drawContours(frame,contours,-1,(0,255,0),3)
    cv2.imshow('frame',frame) 
    for cnt in contours:
        if cnt is not None:
            area = cv2.contourArea(cnt)
        if area>=500 :
          
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            if cx >= 200 :
                print("Vireaza dreapta")
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
            if cx < 200 and cx > 150 :
                print("Pe traeu")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)
            if cx <=150 :
                print("Vireaza stanga")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                GPIO.output(in3, GPIO.HIGH)
                GPIO.output(in4, GPIO.LOW)
            cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
        else:
            print("M-am pierdut")
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
        
        if cv2.waitKey(1) & 0xff == ord('q'):  
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)
            break
capture.release()
cv2.destroyAllWindows() 



