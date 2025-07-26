# Deep Live Cam - Web Version 🌐

A modern web-based version of the Deep Live Cam face swapping application. This version runs entirely in your web browser with a beautiful, responsive interface and real-time processing capabilities.

![Web Version Screenshot](https://via.placeholder.com/800x400?text=Deep+Live+Cam+Web+Interface)

## ✨ Features

- **🎥 Real-time Face Swapping**: Live camera feed processing with minimal latency
- **🌐 Web-based Interface**: No desktop application needed - runs in any modern browser
- **📱 Mobile Friendly**: Responsive design that works on desktop, tablet, and mobile
- **🔒 Privacy Focused**: All processing happens locally on your machine
- **🎨 Beautiful UI**: Modern, gradient-based interface with smooth animations
- **⚡ Easy Setup**: Simple installation and one-click startup
- **📊 Performance Monitoring**: Real-time FPS counter and processing statistics

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A webcam or camera device
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd Deep-Live-Cam-Web
   ```

2. **Install dependencies**
   ```bash
   pip install -r web_requirements.txt
   ```

3. **Start the application**
   ```bash
   python start_web.py
   ```
   
   Or run the Flask app directly:
   ```bash
   python app.py
   ```

4. **Open your browser**
   - Navigate to `http://localhost:5000`
   - Allow camera access when prompted

## 📖 How to Use

### Step 1: Upload Source Face
1. Click on the "Source Face" card on the left
2. Either click "Choose Image" or drag and drop a photo
3. Make sure the image contains a clear, front-facing face
4. Wait for the success message confirming the face was detected

### Step 2: Start Camera
1. Click the "Start Camera" button in the "Live Camera" section
2. Allow camera access when your browser prompts you
3. You should see your live camera feed appear

### Step 3: Begin Face Swapping
1. Click "Start Processing" to begin real-time face swapping
2. The system will replace detected faces in your camera feed with the source face
3. Monitor the FPS counter to see processing performance
4. Click "Stop Processing" to return to normal camera view

## 🛠️ Technical Details

### Architecture
- **Backend**: Flask web server with OpenCV for image processing
- **Frontend**: Pure HTML/CSS/JavaScript with modern ES6+ features
- **Processing**: Real-time frame processing using HTML5 Canvas and WebRTC
- **Face Detection**: OpenCV Haar Cascade classifiers
- **Communication**: RESTful API with JSON responses

### File Structure
```
├── app.py                 # Main Flask application
├── start_web.py          # Easy startup script
├── web_requirements.txt  # Web-specific dependencies
├── templates/
│   └── index.html       # Main web interface
├── static/              # Static assets (created automatically)
└── WEB_README.md        # This file
```

### API Endpoints
- `GET /` - Main web interface
- `POST /upload_source` - Upload source face image
- `POST /process_frame` - Process single video frame
- `GET /start_camera` - Initialize camera capture
- `GET /stop_camera` - Stop camera capture
- `GET /video_feed` - Real-time video stream (alternative method)

## ⚙️ Configuration

### Performance Tuning
You can adjust processing performance by modifying these parameters in the JavaScript:

```javascript
// Frame processing interval (milliseconds)
processingInterval = setInterval(processFrame, 100); // ~10 FPS

// Canvas quality
const frameData = canvas.toDataURL('image/jpeg', 0.8); // 0.8 = 80% quality
```

### Camera Settings
Modify camera resolution in the JavaScript:
```javascript
const stream = await navigator.mediaDevices.getUserMedia({ 
    video: { 
        width: { ideal: 640 },    // Change resolution
        height: { ideal: 480 },
        frameRate: { ideal: 30 }  // Change frame rate
    } 
});
```

## 🔧 Advanced Setup

### Production Deployment
For production use, consider using Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY web_requirements.txt .
RUN pip install -r web_requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "start_web.py"]
```

### HTTPS Setup
For camera access on remote devices, you'll need HTTPS. Consider using:
- Nginx reverse proxy with SSL certificates
- Cloudflare tunnels
- ngrok for development

## 🐛 Troubleshooting

### Common Issues

**Camera not working:**
- Ensure camera permissions are granted
- Try refreshing the page
- Check if another application is using the camera
- Use HTTPS for remote access

**Poor performance:**
- Reduce camera resolution
- Increase processing interval (lower FPS)
- Close other browser tabs
- Use a more powerful device

**Face not detected:**
- Ensure good lighting
- Face should be front-facing and clearly visible
- Try different source images
- Check image format (JPG, PNG, WebP supported)

**Dependencies issues:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r web_requirements.txt
```

## 🎯 Future Enhancements

- [ ] Advanced AI face swapping models (InsightFace integration)
- [ ] Multiple face support
- [ ] Video file processing
- [ ] Real-time filters and effects
- [ ] Face landmark detection visualization
- [ ] Export/save processed videos
- [ ] WebRTC peer-to-peer streaming
- [ ] Progressive Web App (PWA) support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the original LICENSE file for details.

## ⚠️ Ethical Use

Please use this software responsibly:
- Obtain consent before using someone's face
- Clearly label deepfakes when sharing
- Respect privacy and dignity of others
- Follow local laws and regulations
- Do not use for deception or harmful purposes

## 🙏 Acknowledgments

- Original Deep-Live-Cam project by hacksider
- OpenCV community for computer vision tools
- Flask framework for web development
- Font Awesome for beautiful icons

---

**Made with ❤️ for the open source community**