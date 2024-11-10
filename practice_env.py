import cv2
import os
from suno_api import generate_audio_by_prompt, get_audio_information
from dotenv import load_dotenv
import time
from summarization import summarize_prompts
from nvidia import analyze_image
from azure.storage.blob import BlobClient


load_dotenv()
azure_connection_string = os.environ.get("AZURE_CONNECTION_STRING")


def make_dir_test():
    try:
        os.mkdir("images-test-02")
    except FileExistsError:
        pass


def detect_faces_live(frame, face_cascade):
    if face_cascade.empty():
        print("Error: Could not load face cascade classifier.")
        return []

    # Convert the frame to grayscale for better face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    # Draw boxes around the detected faces
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return faces


def capture_images():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    num_pic = 5
    picture_count = 0
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
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
            cv2.putText(
                frame,
                f"Picture {picture_count + 1}",
                (50, 50),
                font,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow("Camera feed", frame)

            make_dir_test()
            filename = f"images-test-02/captured_image_{picture_count + 1}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as '{filename}'")

            picture_count += 1
            start_time = time.time()  # Reset the timer after capturing an image
        else:
            cv2.imshow("Camera feed", frame)
            cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


def prompt_from_image():
    with open("prompt.txt", "w") as f:
        for i in range(5):
            image_path = f"images-test-02/captured_image_{i + 1}.jpg"
            result = analyze_image(image_path)
            if result is not None:
                f.write(result + "\n")
            else:
                print(f"No result for image {i + 1}")


def upload_images():
    container_name = "makeuchackathon-imagestorage"
    # Create a BlobServiceClient object
    for i in range(5):
        blob_name = f"captured_image_{i + 1}.jpg"
        file_path = f"images-test-02/captured_image_{i + 1}.jpg"

        blob_client = BlobClient.from_connection_string(
            conn_str=azure_connection_string,
            container_name=container_name,
            blob_name=blob_name,
        )

        try:
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
                print(f"Uploaded {blob_name} successfully.")
        except Exception as e:
            print(f"Failed to upload {blob_name}. Error: {e}")


def generate_music():
    prompt = summarize_prompts("prompt.txt")
    data = generate_audio_by_prompt({
        "prompt": prompt,
        "make_instrumental": False,
        "wait_audio": False
    })

    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # sleep 5s
        time.sleep(5)

    
if __name__ == "__main__":
    # capture_images()
    prompt_from_image()
    generate_music()
    # upload_images()

