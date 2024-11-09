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
    
    num_pic = 5
    picture_count = 0

    while picture_count < num_pic:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Cannot receive frame.")
            break
        
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, f'Picture {picture_count + 1}', (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Camera feed', frame)
        
        make_dir()
        filename = f'images/captured_image_{picture_count + 1}.jpg'
        cv2.imwrite(filename, frame)
        print(f"Image captured and saved as '{filename}'")
        
        picture_count += 1
        cv2.waitKey(1000)
    cap.release()
    cv2.destroyAllWindows()
    


def prompt_from_image():
    image_path='images/captured_image.jpg'
    result = analyze_image(image_path)
    print(result)



'''
implementation: 



write algorithm 
to pick  the best img to analyze + generate prompts 


'''  
    
# if __name__ == '__main__':
#     prompt_from_image()
    