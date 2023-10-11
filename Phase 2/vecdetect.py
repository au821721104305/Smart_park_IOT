import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained vehicle detection classifier (Haar Cascade)
car_cascade = cv2.CascadeClassifier('/content/haarcascade_car.xml')

# Create a VideoCapture object to capture video from a file or camera (you can specify the source)
video_source = '/content/pexels_videos_2406459 (2160p).mp4'  # Replace with your video path or use 0 for the default camera
cap = cv2.VideoCapture(video_source)

# Define parking space boundaries (x, y, width, height)
parking_spaces = [(60, 60, 50, 50),(60, 60, 50, 50),(60, 60, 50, 50),(60, 60, 50, 50),(60, 60, 50, 50)]  # Example: Two parking spaces

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale for vehicle detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect cars in the frame using the car_cascade classifier
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # Initialize a list to track parking space occupancy
    occupancy_status = ['Vacant'] * len(parking_spaces)

    # Draw rectangles around detected cars and check parking space occupancy
    for i, (x, y, w, h) in enumerate(cars):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Check if the detected car is within any parking space
        for j, (px, py, pw, ph) in enumerate(parking_spaces):
            if x >= px and y >= py and x + w <= px + pw and y + h <= py + ph:
                occupancy_status[j] = 'Occupied'

    # Print parking space availability
    for j, status in enumerate(occupancy_status):
        print(f'Space {j + 1}: {status}')

    # Display the frame with detected cars and parking space occupancy using Matplotlib
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.imshow(frame_rgb)
    plt.axis('off')
    plt.show()

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
