import numpy as np
import cv2
import base64
from typing import Optional, Tuple
import io
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def encode_face_from_base64(image_base64: str) -> Optional[np.ndarray]:
    try:
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)
        
        logger.warning("Using dummy face encoding - install face_recognition for actual functionality")
        dummy_encoding = np.random.random(128).astype(np.float64)
        
        return dummy_encoding
        
    except Exception as e:
        print(f"Error encoding face: {str(e)}")
        return None

def encode_face_from_file(image_path: str) -> Optional[np.ndarray]:
    try:
        image = Image.open(image_path)
        logger.warning("Using dummy face encoding - install face_recognition for actual functionality")
        dummy_encoding = np.random.random(128).astype(np.float64)
        return dummy_encoding
        
    except Exception as e:
        print(f"Error encoding face from file: {str(e)}")
        return None

def compare_faces(known_encoding: np.ndarray, unknown_encoding: np.ndarray, tolerance: float = 0.6) -> Tuple[bool, float]:
    try:
        distance = np.linalg.norm(known_encoding - unknown_encoding)
        normalized_distance = min(distance / 2.0, 1.0)
        confidence = 1.0 - normalized_distance
        is_match = normalized_distance <= tolerance
        
        logger.warning("Using dummy face comparison - install face_recognition for actual functionality")
        return is_match, confidence
        
    except Exception as e:
        print(f"Error comparing faces: {str(e)}")
        return False, 0.0

def encoding_to_bytes(encoding: np.ndarray) -> bytes:
    return encoding.tobytes()

def bytes_to_encoding(encoding_bytes: bytes) -> np.ndarray:
    return np.frombuffer(encoding_bytes, dtype=np.float64)