"""
Computer Vision Service for image processing, similarity search, and analysis
"""
from typing import List, Dict, Any, Optional
import numpy as np
import cv2
from PIL import Image
from sentence_transformers import SentenceTransformer
import io
import base64


class VisionService:
    """Computer vision service for image processing"""
    
    def __init__(self):
        """Initialize vision models"""
        # Load CLIP model for image-text similarity
        self.clip_model = SentenceTransformer('clip-ViT-B-32')
    
    def encode_image(self, image: Image.Image) -> np.ndarray:
        """
        Encode image to embedding vector
        
        Args:
            image: PIL Image object
            
        Returns:
            Image embedding vector
        """
        return self.clip_model.encode(image)
    
    def encode_image_from_bytes(self, image_bytes: bytes) -> np.ndarray:
        """
        Encode image from bytes to embedding vector
        
        Args:
            image_bytes: Image bytes
            
        Returns:
            Image embedding vector
        """
        image = Image.open(io.BytesIO(image_bytes))
        return self.encode_image(image)
    
    def find_similar_images(
        self,
        query_image: Image.Image,
        image_embeddings: List[np.ndarray],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find similar images using cosine similarity
        
        Args:
            query_image: Query image
            image_embeddings: List of image embeddings to search
            top_k: Number of top results
            
        Returns:
            List of similar images with scores
        """
        query_embedding = self.encode_image(query_image)
        
        # Calculate cosine similarity
        similarities = []
        for emb in image_embeddings:
            similarity = np.dot(query_embedding, emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(emb)
            )
            similarities.append(float(similarity))
        
        # Get top k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "index": int(idx),
                "score": similarities[idx]
            })
        
        return results
    
    def detect_objects(self, image: Image.Image) -> List[Dict[str, Any]]:
        """
        Detect objects in image (placeholder - can be enhanced with YOLO, etc.)
        
        Args:
            image: PIL Image object
            
        Returns:
            List of detected objects
        """
        # Placeholder implementation
        # In production, use YOLO, Faster R-CNN, or similar
        return []
    
    def extract_features(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract visual features from image
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary of features
        """
        # Convert to OpenCV format
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Extract basic features
        features = {
            "width": image.width,
            "height": image.height,
            "aspect_ratio": image.width / image.height,
            "mean_brightness": float(np.mean(gray)),
            "std_brightness": float(np.std(gray)),
        }
        
        return features


vision_service = VisionService()

