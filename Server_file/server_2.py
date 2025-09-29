from flask import Flask, request
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
    
    # Preprocess the image (convert to grayscale and threshold)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)

    # Run OCR
    results = reader.readtext(thresh)
    if results:
        print("\nAll OCR results:")
        for res in results:
            print(f"Text: {res[1]}, Confidence: {res[2]:.2f}")
        
        # Select highest-confidence text as the number plate
        plate_candidate = max(results, key=lambda x: x[2])
        plate_number = plate_candidate[1]
        
        # Optional: Post-processing to correct mistakes (e.g., 'O' to '0')
        plate_number = plate_number.replace('O', '0').replace('I', '1')

        print("Number Plate Detected:", plate_number)
        
        # Save to file
        with open("numbers.txt", "a") as f:
            f.write(plate_number + "\n")
        
        return plate_number
    else:
        print("No Plate Detected.")
        return "No Plate Detected", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
