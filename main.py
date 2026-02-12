import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np
from car_color_detection import CarColorDetector
import threading

class TrafficAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Color Detection & Traffic Analysis")
        self.root.geometry("1200x800")
        
        self.detector = CarColorDetector()
        self.current_image = None
        self.processed_image = None
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        ttk.Button(control_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Process Image", command=self.process_image).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Save Result", command=self.save_result).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Start Webcam", command=self.start_webcam).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Stop Webcam", command=self.stop_webcam).grid(row=0, column=4, padx=5)
        
        # Image display frames
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Original image
        original_frame = ttk.LabelFrame(image_frame, text="Original Image", padding="5")
        original_frame.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.original_label = ttk.Label(original_frame)
        self.original_label.grid(row=0, column=0)
        
        # Processed image
        processed_frame = ttk.LabelFrame(image_frame, text="Processed Image", padding="5")
        processed_frame.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.processed_label = ttk.Label(processed_frame)
        self.processed_label.grid(row=0, column=0)
        
        # Results panel
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.results_text = tk.Text(results_frame, height=8, width=80)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        self.webcam_active = False
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        
        if file_path:
            self.current_image = cv2.imread(file_path)
            self.display_original_image()
            
    def display_original_image(self):
        if self.current_image is not None:
            # Resize for display
            display_image = cv2.resize(self.current_image, (400, 300))
            display_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage
            pil_image = Image.fromarray(display_image)
            photo = ImageTk.PhotoImage(pil_image)
            
            self.original_label.configure(image=photo)
            self.original_label.image = photo
            
    def process_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Process in separate thread to prevent GUI freezing
        threading.Thread(target=self._process_image_thread, daemon=True).start()
        
    def _process_image_thread(self):
        try:
            # Process the image
            result_image, results = self.detector.process_image(self.current_image.copy())
            self.processed_image = result_image
            
            # Update GUI in main thread
            self.root.after(0, self._update_processed_image, result_image, results)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
            
    def _update_processed_image(self, result_image, results):
        # Display processed image
        display_image = cv2.resize(result_image, (400, 300))
        display_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
        
        pil_image = Image.fromarray(display_image)
        photo = ImageTk.PhotoImage(pil_image)
        
        self.processed_label.configure(image=photo)
        self.processed_label.image = photo
        
        # Update results
        self.update_results(results)
        
    def update_results(self, results):
        self.results_text.delete(1.0, tk.END)
        
        result_text = f"""TRAFFIC ANALYSIS RESULTS
{'='*50}

CAR DETECTION:
- Total Cars Detected: {results['total_cars']}
- Blue Cars: {results['blue_cars']} (marked with RED rectangles)
- Other Color Cars: {results['other_cars']} (marked with BLUE rectangles)

CAR COLOR BREAKDOWN:
"""
        
        for color, count in results['car_colors'].items():
            result_text += f"- {color.title()}: {count}\n"
            
        result_text += f"""
PEOPLE DETECTION:
- Total People: {results['total_people']}

DETECTION CONFIDENCE:
- Average Car Detection Confidence: {results.get('avg_car_confidence', 0):.2f}
- Average Person Detection Confidence: {results.get('avg_person_confidence', 0):.2f}
"""
        
        self.results_text.insert(tk.END, result_text)
        
    def save_result(self):
        if self.processed_image is None:
            messagebox.showwarning("Warning", "No processed image to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )
        
        if file_path:
            cv2.imwrite(file_path, self.processed_image)
            messagebox.showinfo("Success", "Image saved successfully!")
            
    def start_webcam(self):
        if not self.webcam_active:
            self.webcam_active = True
            threading.Thread(target=self._webcam_thread, daemon=True).start()
            
    def stop_webcam(self):
        self.webcam_active = False
        
    def _webcam_thread(self):
        cap = cv2.VideoCapture(0)
        
        while self.webcam_active:
            ret, frame = cap.read()
            if ret:
                self.current_image = frame.copy()
                
                # Process frame
                try:
                    result_image, results = self.detector.process_image(frame)
                    self.processed_image = result_image
                    
                    # Update GUI
                    self.root.after(0, self._update_webcam_display, frame, result_image, results)
                    
                except Exception as e:
                    print(f"Processing error: {e}")
                    
        cap.release()
        
    def _update_webcam_display(self, original, processed, results):
        # Update original image
        display_original = cv2.resize(original, (400, 300))
        display_original = cv2.cvtColor(display_original, cv2.COLOR_BGR2RGB)
        pil_original = Image.fromarray(display_original)
        photo_original = ImageTk.PhotoImage(pil_original)
        self.original_label.configure(image=photo_original)
        self.original_label.image = photo_original
        
        # Update processed image
        display_processed = cv2.resize(processed, (400, 300))
        display_processed = cv2.cvtColor(display_processed, cv2.COLOR_BGR2RGB)
        pil_processed = Image.fromarray(display_processed)
        photo_processed = ImageTk.PhotoImage(pil_processed)
        self.processed_label.configure(image=photo_processed)
        self.processed_label.image = photo_processed
        
        # Update results
        self.update_results(results)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficAnalysisApp(root)
    root.mainloop()
