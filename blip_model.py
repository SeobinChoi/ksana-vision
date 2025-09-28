#!/usr/bin/env python3
"""
BLIP Model Management Module
Handles BLIP model loading, processing, and caption generation.
"""

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

class BLIPModelManager:
    """Manages BLIP model loading and caption generation"""
    
    def __init__(self, model_name="Salesforce/blip-image-captioning-base"):
        self.model_name = model_name
        self.device = self._get_device()
        self.processor = None
        self.model = None
        
    def _get_device(self):
        """Determine the best available device"""
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"
    
    def load_model(self):
        """Load BLIP model and processor"""
        print(f"🔄 Loading {self.model_name}...")
        print(f"📱 Using device: {self.device}")
        
        try:
            # Load processor with fast tokenizer
            self.processor = BlipProcessor.from_pretrained(
                self.model_name, 
                use_fast=True
            )
            
            # Load model with appropriate settings and use safetensors
            self.model = BlipForConditionalGeneration.from_pretrained(
                self.model_name,
                device_map=self.device,
                dtype=torch.float16 if self.device in ["mps", "cuda"] else torch.float32,
                use_safetensors=True
            )
            
            print("✅ Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def generate_caption(self, image):
        """Generate caption for the given image"""
        if not self.processor or not self.model:
            return "Error: Model not loaded"
        
        try:
            # Ensure image is PIL Image
            if hasattr(image, 'shape'):  # OpenCV frame
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(image_rgb)
            else:
                pil_image = image
            
            # Process with BLIP
            inputs = self.processor(images=pil_image, return_tensors="pt").to(self.device)
            
            # Generate caption
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs, 
                    max_length=50, 
                    num_beams=5,
                    do_sample=False
                )
            
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            return caption
            
        except Exception as e:
            return f"Error generating caption: {e}"
    
    def get_model_info(self):
        """Get information about the loaded model"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "loaded": self.model is not None
        }

# Import cv2 here to avoid circular imports
import cv2
