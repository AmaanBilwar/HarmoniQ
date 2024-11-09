import cv2 
import os 
from nvidia import analyze_image


def make_dir():
    try:
        os.mkdir('images')
    except FileExistsError:
        pass



def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    countdown = 5

    while countdown > 0:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Cannot receive frame.")
            break
        
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, str(countdown), (200, 400), font, 5, (255, 255, 255), 5, cv2.LINE_AA)
        cv2.imshow('Camera feed', frame)
        
        cv2.waitKey(1000)
        countdown -= 1
        
    ret, frame = cap.read()
    if ret:
        make_dir()
        cv2.imwrite('images/captured_image.jpg', frame)
        print("Image captured and saved as 'captured_image.jpg'")

    cv2.imshow('Captured Image', frame)
    cv2.waitKey(3000)

    cap.release()
    cv2.destroyAllWindows()


def prompt_from_image():
    image_path='images/captured_image.jpg'
    result = analyze_image(image_path)
    print(result)
    


  
    
# if __name__ == '__main__':
#     prompt_from_image()
    