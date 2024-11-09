import cv2 
import os 
from nvidia import analyze_image
import time

def make_dir_test():
    try:
        os.mkdir('images-test-02')
    except FileExistsError:
        pass

def detect_faces_live(frame, face_cascade):
    if face_cascade.empty():
        print("Error: Could not load face cascade classifier.")
        return []

    # Convert the frame to grayscale for better face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw boxes around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return faces

def capture_images():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    num_pic = 5
    picture_count = 0
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    start_time = time.time()
    
    while picture_count < num_pic:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Cannot receive frame.")
            break
        
        # Detect faces in the frame
        faces = detect_faces_live(frame, face_cascade)

        if len(faces) > 0 and (time.time() - start_time) >= 10:
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, f'Picture {picture_count + 1}', (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Camera feed', frame)
            
            make_dir_test()
            filename = f'images-test-02/captured_image_{picture_count + 1}.jpg'
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as '{filename}'")
            
            picture_count += 1
            start_time = time.time()  # Reset the timer after capturing an image
        else:
            cv2.imshow('Camera feed', frame)
            cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

def prompt_from_image():
    for i in range(5):
        image_path = f'images-test-02/captured_image_{i + 1}.jpg'
        result = analyze_image(image_path)
        print(result)



'''
implementation: 

have a custom prompt from the user on what task theyre doing while listening to music for better results with music generation 

maybe i should also ask for their fav genre of music and artists they listen to 

which approach seems more suitable ? clicking 5 pics and then summarizing the emotions expresssed in them 
or clicking 1 pic and summarizing the emotions expressed in it 
and then generating prompts based on that ? and then generating music ? 


Write algorithm 
to pick  the best img to analyze + generate prompts 



'''  
    
if __name__ == '__main__':
    detect_faces_live()    