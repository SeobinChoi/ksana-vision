#!/usr/bin/env python3
"""
Camera Management Module
Handles camera initialization, frame capture, and display.
"""

import cv2
import time
from typing import Optional, Tuple

class CameraManager:
    """Manages camera operations and display"""
    
    def __init__(self, camera_index=0, show_window=False):
        self.camera_index = camera_index
        self.show_window = show_window
        self.cap = None
        self.current_caption = ""
        
    def initialize(self):
        """Initialize camera capture"""
        print(f"📷 Initializing camera (index {self.camera_index})...")
        
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print("❌ Cannot open camera. Please check:")
            print("   - Camera is not being used by another application")
            print("   - Camera permissions are granted")
            print("   - Camera index is correct (try 0, 1, or 2)")
            return False
        
        # Set camera properties for better quality
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("✅ Camera initialized successfully!")
        return True
    
    def read_frame(self) -> Tuple[bool, Optional[cv2.Mat]]:
        """Read a frame from the camera"""
        if not self.cap:
            return False, None
        
        ret, frame = self.cap.read()
        return ret, frame
    
    def display_frame(self, frame, caption: str = ""):
        """Display frame with optional caption overlay"""
        if not self.show_window:
            return
        
        # Create display frame with caption
        display_frame = frame.copy()
        
        if caption:
            self.current_caption = caption
            # Add caption text to the frame
            cv2.putText(
                display_frame, 
                caption, 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (0, 255, 0), 
                2
            )
        
        cv2.imshow('BLIP Camera Captioning', display_frame)
    
    def check_for_quit(self) -> bool:
        """Check if user wants to quit (pressed 'q')"""
        if not self.show_window:
            return False
        
        key = cv2.waitKey(1) & 0xFF
        return key == ord('q')
    
    def release(self):
        """Release camera and close windows"""
        if self.cap:
            self.cap.release()
        
        if self.show_window:
            cv2.destroyAllWindows()
        
        print("📷 Camera released")
    
    def get_camera_info(self):
        """Get camera information"""
        if not self.cap:
            return {"status": "not_initialized"}
        
        return {
            "camera_index": self.camera_index,
            "width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": int(self.cap.get(cv2.CAP_PROP_FPS)),
            "show_window": self.show_window
        }
