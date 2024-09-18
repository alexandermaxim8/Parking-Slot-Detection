import cv2
import numpy as np
import pickle  # Import the class
from parallelogram import Parallelogram

# class Parallelogram:
#     def __init__(self, points, obj_id):
#         self.points = np.array(points, dtype=np.int32)
#         self.obj_id = obj_id
#         self.cx, self.cy = self.centroid()

#     def centroid(self):
#         center = np.mean(self.points, axis=0)
#         return int(center[0]), int(center[1])

#     def draw(self, img):
#         cv2.polylines(img, [self.points], isClosed=True, color=(0, 255, 0), thickness=2)
#         cv2.putText(img, f"ID: {self.obj_id}", (self.cx - 20, self.cy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

# Load the pickled parallelograms from the file
with open('parking_space.pkl', 'rb') as file:
    parallelograms = pickle.load(file)

# Load the image
img = cv2.imread("parking lot.jpg")
if img is None:
    print("Error loading image")
else:
    # Draw each loaded parallelogram on the image
    for p in parallelograms:
        p.draw(img)

    # Display the result
    cv2.imshow("Redrawn Parallelograms", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
