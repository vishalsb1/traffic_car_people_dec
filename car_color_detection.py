import cv2
import numpy as np
from ultralytics import YOLO
import webcolors
from sklearn.cluster import KMeans

class CarColorDetector:
    def __init__(self):
        # Load YOLO model
        self.model = YOLO('yolov8n.pt')  # Will download if not present
        
        # Define color ranges in HSV
        self.color_ranges = {
            'blue': [(100, 50, 50), (130, 255, 255)],
            'red': [(0, 50, 50), (10, 255, 255)],
            'red2': [(170, 50, 50), (180, 255, 255)],  # Red wraps around
            'green': [(40, 50, 50), (80, 255, 255)],
            'yellow': [(20, 50, 50), (40, 255, 255)],
            'white': [(0, 0, 200), (180, 30, 255)],
            'black': [(0, 0, 0), (180, 255, 50)],
            'gray': [(0, 0, 50), (180, 30, 200)]
        }
        
    def detect_dominant_color(self, image_section):
        """Detect the dominant color in an image section using K-means clustering"""
        # Reshape image to be a list of pixels
        pixels = image_section.reshape((-1, 3))
        
        # Apply K-means clustering to find dominant colors
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get the most dominant color (center with most points)
        labels = kmeans.labels_
        dominant_color = kmeans.cluster_centers_[np.argmax(np.bincount(labels))]
        
        return dominant_color.astype(int)
        
    def classify_color(self, bgr_color):
        """Classify BGR color into predefined categories"""
        # Convert BGR to HSV
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
        
        # Check each color range
        for color_name, (lower, upper) in self.color_ranges.items():
            if color_name == 'red2':  # Handle red wrap-around
                if (hsv_color[0] >= lower[0] and hsv_color[0] <= upper[0] and
                    hsv_color[1] >= lower[1] and hsv_color[1] <= upper[1] and
                    hsv_color[2] >= lower[2] and hsv_color[2] <= upper[2]):
                    return 'red'
            else:
                if (hsv_color[0] >= lower[0] and hsv_color[0] <= upper[0] and
                    hsv_color[1] >= lower[1] and hsv_color[1] <= upper[1] and
                    hsv_color[2] >= lower[2] and hsv_color[2] <= upper[2]):
                    return color_name
        
        return 'other'
        
    def process_image(self, image):
        """Process image to detect cars, people, and colors"""
        original = image.copy()
        
        # Run YOLO detection
        results = self.model(image)
        
        # Initialize counters
        car_count = 0
        blue_car_count = 0
        other_car_count = 0
        people_count = 0
        car_colors = {}
        car_confidences = []
        person_confidences = []
        
        # Process detections
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Get class and confidence
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Check if detection is a car (class 2 in COCO dataset)
                    if cls == 2 and conf > 0.5:  # Car
                        car_count += 1
                        car_confidences.append(conf)
                        
                        # Extract car region for color analysis
                        car_region = original[y1:y2, x1:x2]
                        
                        if car_region.size > 0:
                            # Get dominant color
                            dominant_color_bgr = self.detect_dominant_color(car_region)
                            color_name = self.classify_color(dominant_color_bgr)
                            
                            # Count colors
                            car_colors[color_name] = car_colors.get(color_name, 0) + 1
                            
                            # Draw rectangles based on color
                            if color_name == 'blue':
                                # Red rectangle for blue cars
                                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 3)
                                blue_car_count += 1
                                label = f"Blue Car ({conf:.2f})"
                                cv2.putText(image, label, (x1, y1-10), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                            else:
                                # Blue rectangle for other color cars
                                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
                                other_car_count += 1
                                label = f"{color_name.title()} Car ({conf:.2f})"
                                cv2.putText(image, label, (x1, y1-10), 
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                    
                    # Check if detection is a person (class 0 in COCO dataset)
                    elif cls == 0 and conf > 0.5:  # Person
                        people_count += 1
                        person_confidences.append(conf)
                        
                        # Draw green rectangle for people
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f"Person ({conf:.2f})"
                        cv2.putText(image, label, (x1, y1-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Add summary text to image
        summary_y = 30
        cv2.putText(image, f"Cars: {car_count} | Blue Cars: {blue_car_count} | Other Cars: {other_car_count}", 
                    (10, summary_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(image, f"People: {people_count}", 
                    (10, summary_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Prepare results dictionary
        analysis_results = {
            'total_cars': car_count,
            'blue_cars': blue_car_count,
            'other_cars': other_car_count,
            'total_people': people_count,
            'car_colors': car_colors,
            'avg_car_confidence': np.mean(car_confidences) if car_confidences else 0,
            'avg_person_confidence': np.mean(person_confidences) if person_confidences else 0
        }
        
        return image, analysis_results
