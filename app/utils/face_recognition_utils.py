import numpy as np
import face_recognition
import cv2
import base64
from io import BytesIO
from PIL import Image

def decode_base64_image(base64_string: str) -> np.ndarray:
    """Decode base64 string to numpy array image"""
    try:
        # Remove header if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_string)
        
        # Convert to PIL Image
        pil_image = Image.open(BytesIO(image_data))
        
        # Convert to RGB if needed
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert to numpy array
        image_array = np.array(pil_image)
        
        return image_array
    except Exception as e:
        raise ValueError(f"Failed to decode base64 image: {str(e)}")

def extract_face_encoding(image: np.ndarray) -> np.ndarray:
    """Extract face encoding from image"""
    # Find face locations
    face_locations = face_recognition.face_locations(image)
    
    if not face_locations:
        raise ValueError("No face detected in the image")
    
    if len(face_locations) > 1:
        raise ValueError("Multiple faces detected. Please use image with single face")
    
    # Extract face encoding
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    if not face_encodings:
        raise ValueError("Could not extract face encoding")
    
    return face_encodings[0]

def compare_faces(stored_encoding: np.ndarray, current_encoding: np.ndarray, threshold: float = 0.6) -> tuple[bool, float]:
    """Compare two face encodings and return match status and confidence"""
    # Calculate distance
    distance = face_recognition.face_distance([stored_encoding], current_encoding)[0]
    
    # Convert distance to similarity (confidence)
    confidence = 1 - distance
    
    # Check if match based on threshold
    is_match = distance <= threshold
    
    return is_match, confidence

def encode_face_to_bytes(face_encoding: np.ndarray) -> bytes:
    """Convert face encoding numpy array to bytes for storage"""
    return face_encoding.tobytes()

def decode_face_from_bytes(face_bytes: bytes) -> np.ndarray:
    """Convert bytes back to face encoding numpy array"""
    return np.frombuffer(face_bytes, dtype=np.float64)