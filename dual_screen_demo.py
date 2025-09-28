#!/usr/bin/env python3
"""
Dual Screen Demo Script
Demonstrates the dual screen display functionality with camera and text windows.
"""

from caption_engine import CaptionEngine

def main():
    """Run dual screen demo"""
    print("🖥️  Starting Dual Screen Demo")
    print("=" * 50)
    
    # Create caption engine with dual screen enabled
    engine = CaptionEngine(
        model_name="Salesforce/blip-image-captioning-base",
        camera_index=0,
        show_camera=False,  # Disabled when dual_screen is True
        interval=3,  # Generate captions every 3 seconds
        dual_screen=True  # Enable dual screen display
    )
    
    # Initialize and run
    if not engine.initialize():
        print("❌ Failed to initialize caption engine")
        return
    
    try:
        engine.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        engine.cleanup()

if __name__ == "__main__":
    main()
