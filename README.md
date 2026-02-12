# Car Color Detection & Traffic Analysis System

A machine learning-based computer vision application that detects cars and people at traffic signals, identifies car colors, and provides real-time analysis through an intuitive GUI.

## Features

🚗 **Car Detection & Counting**
- Detects and counts all cars in images or video streams
- Accurate bounding box detection using YOLOv8

🎨 **Color Detection**
- Identifies car colors (blue, red, green, yellow, white, black, gray, etc.)
- Uses K-means clustering for dominant color extraction
- HSV color space analysis for accurate classification

🔴 **Smart Rectangle Marking**
- Red rectangles for blue cars
- Blue rectangles for all other color cars
- Green rectangles for people

👥 **People Detection**
- Counts the number of people at traffic signals
- Displays confidence scores

📊 **Real-time Analysis**
- Displays detailed statistics
- Car color breakdown
- Detection confidence scores

🖼️ **GUI Features**
- Side-by-side original and processed image preview
- Load and process static images
- Real-time webcam processing
- Save processed results
- Detailed results panel

## Requirements

- Python 3.8 or higher
- Webcam (optional, for real-time detection)

## Installation

1. **Clone or download this project**

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

3. **The YOLOv8 model will be automatically downloaded on first run**

## Usage

### Running the Application

```bash
python main.py
```

### Using the GUI

1. **Load Image**: Click to select and load an image file (JPG, PNG, etc.)
2. **Process Image**: Analyze the loaded image for cars, colors, and people
3. **Save Result**: Save the processed image with detections
4. **Start Webcam**: Begin real-time detection using your webcam
5. **Stop Webcam**: Stop the webcam feed

### Understanding the Output

**Rectangle Colors:**
- 🔴 **Red Rectangle** = Blue car detected
- 🔵 **Blue Rectangle** = Other color car (red, green, yellow, white, black, etc.)
- 🟢 **Green Rectangle** = Person detected

**Results Panel Shows:**
- Total number of cars
- Number of blue cars vs other cars
- Color breakdown of all detected cars
- Number of people present
- Detection confidence scores

## Project Structure

```
car_color_detection/
│
├── main.py                    # Main GUI application
├── car_color_detection.py     # Core detection and color analysis
├── gui.py                     # GUI helper (optional)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## How It Works

### 1. Object Detection
- Uses YOLOv8 (You Only Look Once) neural network
- Pre-trained on COCO dataset
- Detects cars (class 2) and people (class 0)

### 2. Color Detection
- Extracts region of interest (ROI) for each detected car
- Applies K-means clustering (k=3) to find dominant colors
- Converts BGR to HSV color space
- Matches against predefined color ranges
- Returns the most prominent color

### 3. Visualization
- Draws colored rectangles based on detection type
- Adds labels with confidence scores
- Displays summary statistics on image
- Updates GUI with detailed results

## Technical Details

**Machine Learning Model:**
- YOLOv8n (nano) - Fast and efficient
- Real-time capable
- Confidence threshold: 0.5

**Color Detection:**
- K-means clustering with 3 clusters
- HSV color space analysis
- 8 predefined color categories

**GUI Framework:**
- Tkinter for cross-platform compatibility
- Threading for responsive UI
- PIL/Pillow for image handling

## Troubleshooting

**Issue: Import errors**
- Ensure all packages from requirements.txt are installed
- Try: `pip install --upgrade -r requirements.txt`

**Issue: YOLOv8 model download fails**
- Check internet connection
- Model will be saved in: `~/.ultralytics/`

**Issue: Webcam not working**
- Ensure webcam permissions are granted
- Try changing camera index in code: `cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`

**Issue: Slow processing**
- Reduce image size before processing
- Use GPU acceleration if available (requires CUDA setup)

## Performance Tips

1. **For better accuracy:**
   - Use high-quality, well-lit images
   - Ensure cars are clearly visible
   - Avoid heavily occluded vehicles

2. **For faster processing:**
   - Resize large images before processing
   - Close other applications
   - Use smaller YOLO model (already using nano)

## Future Enhancements

- [ ] Add support for video files
- [ ] Implement GPU acceleration
- [ ] Add more color categories
- [ ] Export results to CSV/JSON
- [ ] Add traffic flow analysis
- [ ] Multi-camera support

## License

This project is for educational purposes.

## Credits

- **YOLOv8** by Ultralytics
- **OpenCV** for computer vision operations
- **scikit-learn** for K-means clustering

## Author

Created as part of a machine learning and computer vision project.

---

**Note:** The first run will download the YOLOv8 model (~6MB) automatically. Subsequent runs will use the cached model.
