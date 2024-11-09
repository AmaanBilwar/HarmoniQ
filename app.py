import cv2 
import time 


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

countdown = 5

while countdown > 0:
    #Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Cannot receive frame.")
        break
    
    #Display the countdown on the frame/window
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame, str(countdown), (200, 400), font, 5, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.imshow('Camera feed', frame)
    
    cv2.waitKey(1000)
    countdown -= 1
    
# capture the final frame
ret, frame = cap.read()
if ret:
    cv2.imwrite('captured_image.jpg', frame)
    print("Image captured and saved as 'captured_image.jpg'")

# Display the captured image for a few seconds
cv2.imshow('Captured Image', frame)
cv2.waitKey(3000)

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()