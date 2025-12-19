"""
NLP Service for semantic search, sentiment analysis, and text processing
"""
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import spacy
from textblob import TextBlob


class NLPService:
    """NLP service for various text processing tasks"""
    
    def __init__(self):
        """Initialize NLP models"""
        # Load sentence transformer for semantic search
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load spaCy for NER and text processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model not installed
            self.nlp = None
    
    def semantic_search(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search on documents
        
        Args:
            query: Search query
            documents: List of documents to search
            top_k: Number of top results to return
            
        Returns:
            List of results with scores
        """
        # Encode query and documents
        query_embedding = self.semantic_model.encode(query)
        doc_embeddings = self.semantic_model.encode(documents)
        
        # Calculate cosine similarity
        similarities = np.dot(doc_embeddings, query_embedding) / (
            np.linalg.norm(doc_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "document": documents[idx],
                "score": float(similarities[idx]),
                "index": int(idx)
            })
        
        return results
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "polarity": float(polarity),
            "subjectivity": float(subjectivity)
        }
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from text
        
        Args:
            text: Text to process
            
        Returns:
            List of extracted entities
        """
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        
        return entities
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for texts
        
        Args:
            texts: List of texts
            
        Returns:
            Numpy array of embeddings
        """
        return self.semantic_model.encode(texts)


nlp_service = NLPService()

