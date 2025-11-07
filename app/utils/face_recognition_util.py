import numpy as np
import face_recognition
import cv2
import base64
from typing import Optional, Tuple
import io
from PIL import Image

def encode_face_from_base64(image_base64: str) -> Optional[np.ndarray]:
    """
    Extract face encoding from base64 image string.
    
    Args:
        image_base64: Base64 encoded image string
        
    Returns:
        Face encoding as numpy array or None if no face found
    """
    try:
        # Decode base64 to image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert PIL image to numpy array
        image_array = np.array(image)
        
        # Convert to RGB if needed (face_recognition expects RGB)
        if len(image_array.shape) == 3 and image_array.shape[2] == 3:
            # Already RGB
            rgb_image = image_array
        else:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_image)
        
        if not face_locations:
            return None
            
        # Get encoding for the first face found
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        if face_encodings:
            return face_encodings[0]
            
        return None
        
    except Exception as e:
        print(f"Error encoding face: {str(e)}")
        return None

def encode_face_from_file(image_path: str) -> Optional[np.ndarray]:
    """
    Extract face encoding from image file.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Face encoding as numpy array or None if no face found
    """
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(image)
        
        if not face_locations:
            return None
            
        # Get encoding for the first face found
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if face_encodings:
            return face_encodings[0]
            
        return None
        
    except Exception as e:
        print(f"Error encoding face from file: {str(e)}")
        return None

def compare_faces(known_encoding: np.ndarray, unknown_encoding: np.ndarray, tolerance: float = 0.6) -> Tuple[bool, float]:
    """
    Compare two face encodings.
    
    Args:
        known_encoding: Known face encoding from database
        unknown_encoding: Unknown face encoding to compare
        tolerance: Similarity threshold (lower = more strict)
        
    Returns:
        Tuple of (is_match, confidence_score)
    """
    try:
        # Calculate face distance
        face_distances = face_recognition.face_distance([known_encoding], unknown_encoding)
        distance = face_distances[0]
        
        # Convert distance to confidence (inverse relationship)
        confidence = 1.0 - distance
        
        # Check if it's a match based on tolerance
        is_match = distance <= tolerance
        
        return is_match, confidence
        
    except Exception as e:
        print(f"Error comparing faces: {str(e)}")
        return False, 0.0

def encoding_to_bytes(encoding: np.ndarray) -> bytes:
    """Convert numpy array encoding to bytes for database storage."""
    return encoding.tobytes()

def bytes_to_encoding(encoding_bytes: bytes) -> np.ndarray:
    """Convert bytes from database back to numpy array encoding."""
    return np.frombuffer(encoding_bytes, dtype=np.float64)