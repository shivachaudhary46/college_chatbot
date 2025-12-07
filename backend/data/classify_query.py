import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
from functools import lru_cache
from typing import Dict, Optional
import time

class QueryClassifier:
    """
    Singleton pattern classifier that loads model once and keeps it in memory.
    Perfect for FastAPI chatbot that handles multiple concurrent requests.
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QueryClassifier, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize only once"""
        if not QueryClassifier._initialized:
            self.model = None
            self.tokenizer = None
            self.id2label = None
            self.device = None
            self.load_model()
            QueryClassifier._initialized = True
    
    def load_model(self, model_path: str = "data/trained_model"):
        """Load model, tokenizer, and configurations"""
        try:
            print("🔄 Loading model...")
            start_time = time.time()
            
            # Convert to absolute path and fix Windows path issue
            import os
            model_path = os.path.abspath(model_path)
            # Convert backslashes to forward slashes for HuggingFace compatibility
            model_path = model_path.replace('\\', '/')
            print(f"📁 Model path: {model_path}")
            
            # Verify path exists
            if not os.path.exists(model_path.replace('/', '\\')):
                raise FileNotFoundError(f"Model directory not found: {model_path}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                local_files_only=True,
                trust_remote_code=True
            )
            
            # Load model
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_path,
                local_files_only=True,
                trust_remote_code=True
            )
            self.model.eval()  # Set to evaluation mode
            
            # Load label mappings
            with open(f"{model_path}/config.json", "r") as f:
                config = json.load(f)
                self.id2label = {int(k): v for k, v in config.get("id2label", {}).items()}
            
            # Set device (GPU if available)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            
            # Optional: Use half precision for faster inference (if GPU available)
            if torch.cuda.is_available():
                self.model.half()  # Convert to FP16 for faster inference
            
            load_time = time.time() - start_time
            print(f"✅ Model loaded in {load_time:.2f}s")
            print(f"✅ Device: {self.device}")
            print(f"✅ Labels: {list(self.id2label.values())}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    @lru_cache(maxsize=1000)  # Cache recent predictions
    def predict_cached(self, text: str) -> str:
        """Cached prediction for identical queries (faster for repeated questions)"""
        return str(self.predict(text))
    
    def predict(self, text: str, return_all_probs: bool = False) -> Dict:
        """
        Predict query classification
        
        Args:
            text: User query
            return_all_probs: Whether to return probabilities for all classes
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            start_time = time.time()
            
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128  # Reduced from 512 for faster inference
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Predict
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                label_id = torch.argmax(probs, dim=-1).item()
                confidence = probs[0][label_id].item()
            
            predicted_label = self.id2label.get(label_id, f"unknown_{label_id}")
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            result = {
                "query_type": predicted_label,
                "confidence": round(confidence, 4),
                "inference_time_ms": round(inference_time, 2)
            }
            
            # Optionally include all probabilities
            if return_all_probs:
                result["all_probabilities"] = {
                    self.id2label.get(i, f"Label_{i}"): round(probs[0][i].item(), 4)
                    for i in range(len(probs[0]))
                }
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "query_type": "unknown"
            }
    
    def predict_batch(self, texts: list) -> list:
        """Predict multiple queries at once (more efficient)"""
        if self.model is None:
            return [{"error": "Model not loaded"}] * len(texts)
        
        try:
            # Tokenize all texts at once
            inputs = self.tokenizer(
                texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                label_ids = torch.argmax(probs, dim=-1)
            
            results = []
            for i, label_id in enumerate(label_ids):
                results.append({
                    "query_type": self.id2label.get(label_id.item(), "unknown"),
                    "confidence": round(probs[i][label_id].item(), 4)
                })
            
            return results
            
        except Exception as e:
            return [{"error": str(e), "query_type": "unknown"}] * len(texts)


# ============================================
# GLOBAL INSTANCE (Initialize once)
# ============================================

classifier = None

def get_classifier() -> QueryClassifier:
    """Get or create classifier instance"""
    global classifier
    if classifier is None:
        classifier = QueryClassifier()
    return classifier
