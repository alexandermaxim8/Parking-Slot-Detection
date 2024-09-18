import cv2
import numpy as np
import pickle
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

points = []
parallelogram = None
parallelograms = [] 

def mouse_callback(event, x, y, flags, param):
    global points, parallelogram

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])

    if event == cv2.EVENT_RBUTTONDOWN:
        obj_id = input("Enter an ID for the parallelogram: ")
        parallelogram = Parallelogram(points, obj_id)
        parallelograms.append(parallelogram) 
        points = []  

def draw_points(img):
    for point in points:
        cv2.circle(img, tuple(point), 5, (0, 0, 255), -1)

cv2.namedWindow("foo", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("foo", mouse_callback)

while True:
    global img
    img = cv2.imread("Screenshot 2024-09-18 015108.png")

    for p in parallelograms:
        p.draw(img)
    draw_points(img)


    # cv2.setWindowProperty("foo", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("foo", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        print(parallelograms)
        with open('parking_space.pkl', 'wb') as file: 
            pickle.dump(parallelograms, file) 
        break

cv2.destroyAllWindows()
