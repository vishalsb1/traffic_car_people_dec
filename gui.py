"""
GUI Helper Functions for Car Color Detection System
This module provides utility functions for the GUI application
"""

import cv2
import numpy as np
from tkinter import messagebox


def resize_image_for_display(image, target_width=400, target_height=300):
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: OpenCV image (BGR)
        target_width: Target width in pixels
        target_height: Target height in pixels
    
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    aspect_ratio = width / height
    
    if width > height:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
    
    return cv2.resize(image, (new_width, new_height))


def validate_image(image):
    """
    Validate if the image is suitable for processing
    
    Args:
        image: OpenCV image
    
    Returns:
        tuple: (is_valid, message)
    """
    if image is None:
        return False, "Image is None"
    
    if image.size == 0:
        return False, "Image is empty"
    
    height, width = image.shape[:2]
    if width < 100 or height < 100:
        return False, "Image is too small (minimum 100x100 pixels)"
    
    if width > 4000 or height > 4000:
        return False, "Image is too large (maximum 4000x4000 pixels)"
    
    return True, "Image is valid"


def create_color_legend():
    """
    Create a legend explaining the rectangle colors
    
    Returns:
        Dictionary with color coding information
    """
    legend = {
        'blue_car': {
            'color': (0, 0, 255),  # BGR red
            'description': 'Blue Car (Red Rectangle)'
        },
        'other_car': {
            'color': (255, 0, 0),  # BGR blue
            'description': 'Other Color Car (Blue Rectangle)'
        },
        'person': {
            'color': (0, 255, 0),  # BGR green
            'description': 'Person (Green Rectangle)'
        }
    }
    return legend


def format_results_text(results):
    """
    Format analysis results into a readable string
    
    Args:
        results: Dictionary with analysis results
    
    Returns:
        Formatted string
    """
    text = f"""TRAFFIC ANALYSIS RESULTS
{'='*50}

CAR DETECTION:
- Total Cars Detected: {results.get('total_cars', 0)}
- Blue Cars: {results.get('blue_cars', 0)} (marked with RED rectangles)
- Other Color Cars: {results.get('other_cars', 0)} (marked with BLUE rectangles)

CAR COLOR BREAKDOWN:
"""
    
    car_colors = results.get('car_colors', {})
    if car_colors:
        for color, count in sorted(car_colors.items(), key=lambda x: x[1], reverse=True):
            text += f"- {color.title()}: {count}\n"
    else:
        text += "- No cars detected\n"
    
    text += f"""
PEOPLE DETECTION:
- Total People: {results.get('total_people', 0)}

DETECTION CONFIDENCE:
- Average Car Detection Confidence: {results.get('avg_car_confidence', 0):.2%}
- Average Person Detection Confidence: {results.get('avg_person_confidence', 0):.2%}

LEGEND:
🔴 Red Rectangle = Blue Car
🔵 Blue Rectangle = Other Color Car
🟢 Green Rectangle = Person
"""
    
    return text


def show_error_dialog(title, message):
    """
    Show error message dialog
    
    Args:
        title: Dialog title
        message: Error message
    """
    messagebox.showerror(title, message)


def show_info_dialog(title, message):
    """
    Show information message dialog
    
    Args:
        title: Dialog title
        message: Information message
    """
    messagebox.showinfo(title, message)


def show_warning_dialog(title, message):
    """
    Show warning message dialog
    
    Args:
        title: Dialog title
        message: Warning message
    """
    messagebox.showwarning(title, message)


def calculate_statistics(detections):
    """
    Calculate additional statistics from detections
    
    Args:
        detections: List of detection dictionaries
    
    Returns:
        Dictionary with statistics
    """
    stats = {
        'total_detections': len(detections),
        'avg_box_size': 0,
        'density': 0
    }
    
    if detections:
        box_sizes = []
        for det in detections:
            width = det.get('width', 0)
            height = det.get('height', 0)
            box_sizes.append(width * height)
        
        stats['avg_box_size'] = np.mean(box_sizes) if box_sizes else 0
    
    return stats


def draw_legend_on_image(image, x=10, y=10):
    """
    Draw a color legend directly on the image
    
    Args:
        image: OpenCV image (BGR)
        x: X coordinate for legend position
        y: Y coordinate for legend position
    
    Returns:
        Image with legend drawn
    """
    legend_height = 120
    legend_width = 250
    
    # Create semi-transparent background
    overlay = image.copy()
    cv2.rectangle(overlay, (x, y), (x + legend_width, y + legend_height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)
    
    # Add legend title
    cv2.putText(image, "Legend:", (x + 10, y + 25), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Add color boxes and labels
    y_offset = 50
    
    # Red rectangle for blue cars
    cv2.rectangle(image, (x + 10, y + y_offset), (x + 30, y + y_offset + 15), (0, 0, 255), -1)
    cv2.putText(image, "Blue Car", (x + 40, y + y_offset + 12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Blue rectangle for other cars
    y_offset += 25
    cv2.rectangle(image, (x + 10, y + y_offset), (x + 30, y + y_offset + 15), (255, 0, 0), -1)
    cv2.putText(image, "Other Car", (x + 40, y + y_offset + 12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Green rectangle for people
    y_offset += 25
    cv2.rectangle(image, (x + 10, y + y_offset), (x + 30, y + y_offset + 15), (0, 255, 0), -1)
    cv2.putText(image, "Person", (x + 40, y + y_offset + 12), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return image


# Color name to RGB mapping for UI elements
COLOR_MAP = {
    'blue': '#0000FF',
    'red': '#FF0000',
    'green': '#00FF00',
    'yellow': '#FFFF00',
    'white': '#FFFFFF',
    'black': '#000000',
    'gray': '#808080',
    'other': '#888888'
}


def get_color_hex(color_name):
    """
    Get hex color code for a color name
    
    Args:
        color_name: Name of the color
    
    Returns:
        Hex color code
    """
    return COLOR_MAP.get(color_name.lower(), '#888888')
