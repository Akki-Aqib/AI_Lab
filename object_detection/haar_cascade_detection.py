"""
Face and Eye Detection using OpenCV Haar Cascade Classifiers
Implements real-time detection from webcam or image file.

Install: pip install opencv-python
"""
import os

def detect_from_image(image_path, output_path="detected_output.jpg"):
    try:
        import cv2
        img = cv2.imread(image_path)
        if img is None:
            print(f"[Error] Could not load image: {image_path}")
            return

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Load pre-trained cascades (bundled with OpenCV)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        print(f"Faces detected: {len(faces)}")

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            # Detect eyes within each face region
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)
            print(f"  Eyes detected in this face: {len(eyes)}")
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                cv2.putText(roi_color, 'Eye', (ex, ey-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imwrite(output_path, img)
        print(f"Output saved to: {output_path}")

    except ImportError:
        print("[Error] OpenCV not installed. Run: pip install opencv-python")
    except Exception as e:
        print(f"[Error] {e}")

def detect_from_webcam():
    try:
        import cv2
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[Error] Could not open webcam.")
            return

        print("Webcam opened. Press 'q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, f'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                roi_gray  = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            cv2.putText(frame, f'Faces: {len(faces)}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face & Eye Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    except ImportError:
        print("[Error] OpenCV not installed. Run: pip install opencv-python")
    except Exception as e:
        print(f"[Error] {e}")

def simulate_detection():
    """Simulate detection without actual image/webcam"""
    print("=== Haar Cascade Simulation ===")
    print("This program uses OpenCV's pre-trained Haar Cascade classifiers.")
    print()
    print("Haar Cascade classifiers used:")
    print("  1. haarcascade_frontalface_default.xml  — Face detection")
    print("  2. haarcascade_eye.xml                  — Eye detection")
    print()
    print("Parameters:")
    print("  scaleFactor  = 1.1   (image scaled by 10% each pass)")
    print("  minNeighbors = 5     (rect must have 5 neighbors to be valid)")
    print("  minSize      = 30x30 (minimum detection region)")
    print()
    print("Simulated result for a sample image with 2 faces:")
    print("  Face 1 detected at (50, 60) | size 120x120")
    print("    Eye 1 at (15, 30) | size 30x30")
    print("    Eye 2 at (70, 30) | size 30x30")
    print("  Face 2 detected at (250, 80) | size 100x100")
    print("    Eye 1 at (10, 25) | size 25x25")
    print("    Eye 2 at (60, 25) | size 25x25")
    print()
    print("To run with real webcam:  call detect_from_webcam()")
    print("To run with image file:   call detect_from_image('photo.jpg')")

if __name__ == "__main__":
    simulate_detection()
    # Uncomment as needed:
    # detect_from_webcam()
    # detect_from_image("test_image.jpg")
