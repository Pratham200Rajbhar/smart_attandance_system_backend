import numpy as np
import base64
from io import BytesIO
from PIL import Image
import face_recognition
def decode_base64_image(base64_string: str) -> np.ndarray:
    if base64_string.startswith('data:'):
        base64_string = base64_string.split(',', 1)[1]
    image_data = base64.b64decode(base64_string)
    pil_image = Image.open(BytesIO(image_data))
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    return np.array(pil_image)
def extract_face_encoding(image: np.ndarray):
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return None
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings[0] if face_encodings else None
def encode_face_to_bytes(face_encoding: np.ndarray) -> bytes:
    return face_encoding.tobytes()
def decode_face_from_bytes(face_bytes: bytes) -> np.ndarray:
    return np.frombuffer(face_bytes, dtype=np.float64)
def compare_faces(known_encoding: np.ndarray, unknown_encoding: np.ndarray) -> float:
    distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
    similarity = 1 - distance
    return max(0, min(1, similarity))
