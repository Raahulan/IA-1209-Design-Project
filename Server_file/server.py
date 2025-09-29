from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np

app = Flask(__name__)
reader = easyocr.Reader(['en'])

@app.route('/upload', methods=['POST'])
def upload_image():
    img_bytes = request.data
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Run OCR
    results = reader.readtext(img)
    if results:
        number_plate = results[0][1]
        print("Detected:", number_plate)
        
        # Save to file
        with open("numbers.txt", "a") as f:
            f.write(number_plate + "\n")
        
        return number_plate
    else:
        return "No Plate Detected", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
