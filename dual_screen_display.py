#!/usr/bin/env python3
"""
Dual Screen Display Module
Shows camera feed in one window and cumulative text in another.
"""

import cv2
import numpy as np
from typing import List, Optional
import time
from PIL import Image, ImageDraw, ImageFont

class DualScreenDisplay:
    """Manages dual screen display with camera and text windows"""
    
    # ================================
    # DISPLAY SETTINGS - 수정 가능한 설정들
    # ================================
    WINDOW_WIDTH = 2560        # 화면 너비 (2K: 2560, 4K: 3840)
    WINDOW_HEIGHT = 1440       # 화면 높이 (2K: 1440, 4K: 2160)
    FONT_SIZE = 24             # 글자 크기
    FONT_PATH = "/Users/xavi/Desktop/real_code/2025ATC/assets/fonts/Acumin Variable Concept.ttf"
    
    # 텍스트 레이아웃 설정
    COLUMN_WIDTH = 25          # 컬럼 간격 (가로 간격)
    CHAR_SPACING = 2           # 글자 간격 (세로 여백)
    MAX_CAPTIONS = 200         # 최대 저장 캡션 수
    
    # ================================
    
    def __init__(self, window_width=None, window_height=None):
        # 설정값 사용 또는 매개변수 사용
        self.window_width = window_width or self.WINDOW_WIDTH
        self.window_height = window_height or self.WINDOW_HEIGHT
        self.camera_window = "Camera Feed"
        self.text_window = "Generated Captions"
        
        # Text storage
        self.captions: List[str] = []  # List of caption strings only
        self.max_captions = self.MAX_CAPTIONS
        
        # Font setup
        self.font_path = self.FONT_PATH
        self.font_size = self.FONT_SIZE
        self.font = None
        self._load_font()
        
        # Vertical layout settings
        self.chars_per_column = None  # No limit - use full height
        self.column_width = self.COLUMN_WIDTH
        
        # Create windows
        self._create_windows()
        
    def _create_windows(self):
        """Create the dual windows"""
        # Create camera window
        cv2.namedWindow(self.camera_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.camera_window, self.window_width, self.window_height)
        
        # Create text window
        cv2.namedWindow(self.text_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.text_window, self.window_width, self.window_height)
        
        # Position windows side by side
        cv2.moveWindow(self.camera_window, 100, 100)
        cv2.moveWindow(self.text_window, self.window_width + 150, 100)
    
    def _load_font(self):
        """Load the custom font"""
        try:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
            print(f"✅ Custom font loaded: {self.font_path}")
        except Exception as e:
            print(f"⚠️  Could not load custom font: {e}")
            print("📝 Using default font")
            try:
                self.font = ImageFont.load_default()
            except:
                self.font = None
        
    def display_camera_frame(self, frame, current_caption: str = ""):
        """Display camera frame with optional caption overlay"""
        display_frame = frame.copy()
        
        # Add current caption overlay if available
        if current_caption:
            # Wrap text for better display
            wrapped_caption = self._wrap_text(current_caption, 60)
            y_offset = 30
            
            for line in wrapped_caption.split('\n'):
                cv2.putText(
                    display_frame,
                    line,
                    (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),  # Green color
                    2
                )
                y_offset += 25
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        cv2.putText(
            display_frame,
            f"Live - {timestamp}",
            (10, display_frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),  # White color
            1
        )
        
        cv2.imshow(self.camera_window, display_frame)
        
    def add_caption(self, caption: str):
        """Add a new caption to the text display"""
        self.captions.append(caption)
        
        # Keep only the latest captions
        if len(self.captions) > self.max_captions:
            self.captions.pop(0)
        
        self._update_text_display()
        
    def _update_text_display(self):
        """Update the text display window with vertical Chinese-style layout"""
        # Create PIL image with black background
        pil_image = Image.new('RGB', (self.window_width, self.window_height), 'black')
        draw = ImageDraw.Draw(pil_image)
        
        if self.captions:
            # Calculate layout - 실시간으로 설정값 사용
            column_width = self.COLUMN_WIDTH
            char_height = self.font_size + self.CHAR_SPACING
            
            # Calculate how many characters can fit in each column (full height)
            max_chars_per_column = (self.window_height - 40) // char_height
            
            # Use full height if no limit specified
            if self.chars_per_column is None:
                chars_per_column = max_chars_per_column
            else:
                chars_per_column = min(self.chars_per_column, max_chars_per_column)
            
            # Calculate how many columns can fit horizontally
            max_columns = (self.window_width - 40) // column_width
            
            # Keep only the latest captions that can fit on screen
            visible_captions = self.captions[-max_columns:] if len(self.captions) > max_columns else self.captions
            
            # Start from right side and work left (newest on right)
            start_x = self.window_width - 20
            current_column = 0
            
            # Process each caption as a separate column (newest first)
            for caption in reversed(visible_captions):
                # Replace spaces with hyphens
                caption_text = caption.replace(" ", "-")
                chars = list(caption_text)
                
                # Calculate column position (right to left)
                column_x = start_x - (current_column * column_width)
                
                if column_x < 20:  # Stop if we run out of space
                    break
                
                # Draw characters vertically in this column
                for j, char in enumerate(chars):
                    char_y = 20 + (j * char_height)
                    
                    if char_y + char_height > self.window_height - 20:
                        break
                    
                    # Draw character
                    draw.text(
                        (column_x, char_y),
                        char,
                        font=self.font,
                        fill='white'
                    )
                
                # Move to next column for next caption
                current_column += 1
        
        # Add footer
        footer_text = f"Total Captions: {len(self.captions)} | Press 'q' to quit"
        draw.text(
            (20, self.window_height - 30),
            footer_text,
            font=self.font,
            fill='white'
        )
        
        # Convert PIL image back to OpenCV format
        text_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        cv2.imshow(self.text_window, text_image)
        
    def _wrap_text(self, text: str, max_chars_per_line: int) -> str:
        """Wrap text to fit within specified character limit (kept for compatibility)"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= max_chars_per_line:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(current_line)
        
        return "\n".join(lines)
        
    def check_for_quit(self) -> bool:
        """Check if user wants to quit (pressed 'q' in either window)"""
        key = cv2.waitKey(1) & 0xFF
        return key == ord('q')
        
    def cleanup(self):
        """Clean up windows and resources"""
        cv2.destroyAllWindows()
        print("🖥️  Display windows closed")
