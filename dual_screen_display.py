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
        self.text_windows = ["Text Window 1", "Text Window 2"]  # 여러 텍스트 창
        
        # Text storage - 두 개의 창을 위한 캡션 저장
        self.window1_captions: List[str] = []  # Text Window 1 캡션들
        self.window2_captions: List[str] = []  # Text Window 2 캡션들
        self.max_captions = self.MAX_CAPTIONS
        
        # Window management
        self.window_capacity = 0  # 한 창당 최대 캡션 수
        
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
        """Create multiple windows (camera + text windows)"""
        # Create camera window
        cv2.namedWindow(self.camera_window, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.camera_window, self.window_width, self.window_height)
        
        # Create text windows
        for i, window_name in enumerate(self.text_windows):
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, self.window_width, self.window_height)
        
        # Position windows
        cv2.moveWindow(self.camera_window, 100, 100)  # 카메라 창 위치
        cv2.moveWindow(self.text_windows[0], self.window_width + 150, 100)  # 첫 번째 텍스트 창
        cv2.moveWindow(self.text_windows[1], self.window_width + 150, self.window_height + 200)  # 두 번째 텍스트 창
    
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
        """Add a new caption to Window 1, overflow goes to Window 2"""
        # Calculate window capacity if not done yet
        if self.window_capacity == 0:
            self._calculate_window_capacity()
        
        # Add new caption to Window 1 (right side)
        self.window1_captions.append(caption)
        
        # If Window 1 is full, move oldest caption to Window 2
        if len(self.window1_captions) > self.window_capacity:
            # Move the oldest caption from Window 1 to Window 2
            overflow_caption = self.window1_captions.pop(0)
            self.window2_captions.append(overflow_caption)
            
            # If Window 2 is also full, remove oldest caption
            if len(self.window2_captions) > self.window_capacity:
                self.window2_captions.pop(0)
        
        self._update_text_display()
    
    def _calculate_window_capacity(self):
        """Calculate how many captions can fit in one text window"""
        column_width = self.COLUMN_WIDTH
        char_height = self.font_size + self.CHAR_SPACING
        
        # Calculate how many columns can fit horizontally
        max_columns = (self.window_width - 40) // column_width
        
        # Calculate how many characters can fit in each column (full height)
        max_chars_per_column = (self.window_height - 40) // char_height
        
        # Estimate capacity based on average caption length
        # Assume average caption is about 30 characters
        avg_caption_length = 30
        self.window_capacity = max_columns * max(1, int(avg_caption_length / 20))  # Rough estimate
        
    def _update_text_display(self):
        """Update both text windows with vertical Chinese-style layout"""
        # Update Window 1
        self._update_single_window(self.window1_captions, 0)
        
        # Update Window 2  
        self._update_single_window(self.window2_captions, 1)
    
    def _update_single_window(self, captions: List[str], window_index: int):
        """Update a single text window with vertical Chinese-style layout"""
        # Create PIL image with black background
        pil_image = Image.new('RGB', (self.window_width, self.window_height), 'black')
        draw = ImageDraw.Draw(pil_image)
        
        if captions:
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
            visible_captions = captions[-max_columns:] if len(captions) > max_columns else captions
            
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
        
        # Add footer with window info
        window_num = window_index + 1
        footer_text = f"Window {window_num} | Captions: {len(captions)} | Press 'q' to quit"
        draw.text(
            (20, self.window_height - 30),
            footer_text,
            font=self.font,
            fill='white'
        )
        
        # Convert PIL image back to OpenCV format
        text_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Show in the specific text window
        cv2.imshow(self.text_windows[window_index], text_image)
        
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
        print("🖥️  All display windows closed")
