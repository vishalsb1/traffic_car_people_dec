"""
Configuration settings for Car Color Detection System
Modify these values to customize the application behavior
"""

# Detection Settings
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for detections (0.0 to 1.0)
YOLO_MODEL = 'yolov8n.pt'  # Model options: yolov8n.pt, yolov8s.pt, yolov8m.pt

# Display Settings
DISPLAY_WIDTH = 400  # Width for image display in GUI
DISPLAY_HEIGHT = 300  # Height for image display in GUI

# Rectangle Colors (BGR format)
BLUE_CAR_COLOR = (0, 0, 255)  # Red rectangle for blue cars
OTHER_CAR_COLOR = (255, 0, 0)  # Blue rectangle for other cars
PERSON_COLOR = (0, 255, 0)  # Green rectangle for people

# Rectangle Thickness
RECTANGLE_THICKNESS = 3

# Color Detection Settings
KMEANS_CLUSTERS = 3  # Number of clusters for K-means color detection
COLOR_CONFIDENCE_THRESHOLD = 0.3  # Minimum color presence to be considered

# HSV Color Ranges (Hue, Saturation, Value)
COLOR_RANGES = {
    'blue': [(100, 50, 50), (130, 255, 255)],
    'red': [(0, 50, 50), (10, 255, 255)],
    'red2': [(170, 50, 50), (180, 255, 255)],  # Red wraps around
    'green': [(40, 50, 50), (80, 255, 255)],
    'yellow': [(20, 50, 50), (40, 255, 255)],
    'white': [(0, 0, 200), (180, 30, 255)],
    'black': [(0, 0, 0), (180, 255, 50)],
    'gray': [(0, 0, 50), (180, 30, 200)]
}

# COCO Dataset Class IDs
PERSON_CLASS_ID = 0
CAR_CLASS_ID = 2

# GUI Settings
WINDOW_TITLE = "Car Color Detection & Traffic Analysis"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Webcam Settings
WEBCAM_INDEX = 0  # Change to 1, 2, etc. if default camera doesn't work
WEBCAM_FPS = 30  # Frames per second for webcam capture

# Text Display Settings
FONT = 1  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
FONT_THICKNESS = 2
TEXT_COLOR = (255, 255, 255)  # White

# Performance Settings
ENABLE_GPU = False  # Set to True if you have CUDA-capable GPU
MAX_IMAGE_SIZE = 4000  # Maximum width/height in pixels
MIN_IMAGE_SIZE = 100  # Minimum width/height in pixels

# File Settings
SUPPORTED_IMAGE_FORMATS = [
    ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")
]

SAVE_IMAGE_FORMATS = [
    ("JPEG files", "*.jpg"),
    ("PNG files", "*.png")
]

# Debug Settings
DEBUG_MODE = False  # Enable verbose logging
SHOW_CONFIDENCE = True  # Show confidence scores on detections
