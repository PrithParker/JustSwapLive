#!/usr/bin/env python3

import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import base64
import io
from PIL import Image
import threading
import time
import queue

app = Flask(__name__)
CORS(app)

# Global variables for face swapping
source_face = None
face_swapper = None
face_detector = None
video_capture = None
processing_queue = queue.Queue(maxsize=10)

class FaceSwapProcessor:
    def __init__(self):
        self.source_embedding = None
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def load_source_face(self, image_data):
        """Load and process the source face image"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image.convert('RGB'))
            
            # Detect face in source image
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                self.source_face = image_np
                return True
            return False
        except Exception as e:
            print(f"Error loading source face: {e}")
            return False
    
    def simple_face_swap(self, frame):
        """Simple face replacement using OpenCV (placeholder for more advanced AI models)"""
        if self.source_face is None:
            return frame
            
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                # Simple overlay - in a real implementation, this would use AI face swapping
                source_resized = cv2.resize(self.source_face, (w, h))
                source_bgr = cv2.cvtColor(source_resized, cv2.COLOR_RGB2BGR)
                
                # Create a mask for better blending
                mask = np.ones((h, w, 3), dtype=np.uint8) * 255
                center = (x + w // 2, y + h // 2)
                
                # Use seamless cloning for better integration
                try:
                    frame = cv2.seamlessClone(source_bgr, frame, mask, center, cv2.NORMAL_CLONE)
                except:
                    # Fallback to simple replacement
                    frame[y:y+h, x:x+w] = source_bgr
                    
                # Draw rectangle around detected face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
            return frame
        except Exception as e:
            print(f"Error in face swap: {e}")
            return frame

# Initialize the face swap processor
processor = FaceSwapProcessor()

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/upload_source', methods=['POST'])
def upload_source():
    """Handle source face image upload"""
    try:
        data = request.json
        image_data = data.get('image')
        
        if processor.load_source_face(image_data):
            return jsonify({'status': 'success', 'message': 'Source face loaded successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'No face detected in the image'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Process a single frame for face swapping"""
    try:
        data = request.json
        frame_data = data.get('frame')
        
        # Decode frame
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        frame_image = Image.open(io.BytesIO(frame_bytes))
        frame_np = np.array(frame_image.convert('RGB'))
        frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
        
        # Process frame
        processed_frame = processor.simple_face_swap(frame_bgr)
        
        # Encode result
        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'processed_frame': f'data:image/jpeg;base64,{frame_base64}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/video_feed')
def video_feed():
    """Video streaming route for real-time processing"""
    def generate():
        global video_capture
        if video_capture is None:
            video_capture = cv2.VideoCapture(0)
            
        while True:
            ret, frame = video_capture.read()
            if ret:
                processed_frame = processor.simple_face_swap(frame)
                
                # Encode frame as JPEG
                _, buffer = cv2.imencode('.jpg', processed_frame)
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                break
                
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera')
def start_camera():
    """Start camera capture"""
    global video_capture
    try:
        if video_capture is None:
            video_capture = cv2.VideoCapture(0)
        return jsonify({'status': 'success', 'message': 'Camera started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_camera')
def stop_camera():
    """Stop camera capture"""
    global video_capture
    try:
        if video_capture is not None:
            video_capture.release()
            video_capture = None
        return jsonify({'status': 'success', 'message': 'Camera stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)