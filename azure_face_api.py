import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceAdministrationClient, FaceClient
from azure.ai.vision.face.models import FaceAttributeType, FaceAttributeTypeRecognition04, FaceDetectionModel, FaceRecognitionModel, QualityForRecognition

load_dotenv()
# This key will serve all examples in this document.
KEY = os.getenv("AZURE_API_KEY")

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.getenv("AZURE_FACE_API_ENDPOINT")

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, AzureKeyCredential(KEY))

def detect_faces(image_path):
    # Open the image file
    with open(image_path, 'rb') as image:
        # Detect faces in the image
        detected_faces = face_client.detect(
            image,
            recognition_model=FaceRecognitionModel.RECOGNITION04,
            return_face_id=True,
            return_face_attributes=[
                FaceAttributeType.accessories,
                FaceAttributeType.blur,
                FaceAttributeType.exposure,
                FaceAttributeType.noise,
                FaceAttributeType.occlusion
            ],
            detection_model=FaceDetectionModel.DETECTION03,
        )             
        

    if not detected_faces:
        print("No faces detected.")
        return []

    # Print the detected face attributes
    face_attributes = []
    for face in detected_faces:
        attributes = face.face_attributes
        face_info = {
            'accessories': attributes.accessories,
            'blur': attributes.blur,
            'exposure': attributes.exposure,
            'noise': attributes.noise,
            'occlusion': attributes.occlusion
        }
        face_attributes.append(face_info)
        print(f"Detected face attributes: {face_info}")

    return face_attributes

# Example usage
if __name__ == "__main__":
    image_path = "images-test/captured_image_1.jpg"
    detect_faces(image_path)