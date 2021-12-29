import cv2, time
#1. Create an object. Zero for external camera
video = cv2.VideoCapture(0)

#8. a variable 
a=0
while True:
    a = a + 1
    #3. Create frame object

    check, frame = video.read()

    print(check)
    print(frame)  #Representing the image

    #6. Converting to grayscale
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #frame to gray


    #4. Show the frame!
    cv2.imshow("Capturing..!", gray) #frame to gray

    #5. For press any key to out (miliseconds)
    #cv2.waitKey(0)

    #7. For playing
    key=cv2.waitKey(1)
    if key == ord('q'):
        break
print(a)

#2. Shutdown the camea
video.release()

cv2.destroyAllWindows
