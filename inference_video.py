from ultralytics import YOLO
from parallelogram import Parallelogram
import pickle
import cv2
import numpy as np
import time
import torch
                                           
model = YOLO("best.onnx", task="obb")
# if torch.cuda.is_available():
#     model.to("cuda")
dummy_img = np.zeros((640, 640, 3), dtype=np.uint8)  # Create a black image (640x640)
_ = model.predict(dummy_img)

cap = cv2.VideoCapture("easy1.mp4")

with open('parking_space.pkl', 'rb') as file:
    parallelograms = pickle.load(file)

cv2.namedWindow("foo", cv2.WINDOW_NORMAL)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model.predict(frame)
    for result in results:
        obb = result.obb.xyxyxyxy.detach().cpu().numpy()
        # result.save(filename="result.jpg")

    img = frame
    for p in parallelograms:
        is_currently_occupied = False
        for bb in obb:
            x_c = int(np.mean([point[0] for point in bb]))
            y_c = int(np.mean([point[1] for point in bb]))
            ctr = (x_c, y_c)
            cv2.circle(img, ctr, 5, (0, 0, 255), -1)
            if cv2.pointPolygonTest(p.points, (x_c,y_c), False) == 1.0:
                is_currently_occupied = True

            if is_currently_occupied:
                p.occupied = True  # Update state to occupied
            else:
                p.occupied = False  # Otherwise, mark as unoccupied

            p.draw(img)

    cv2.imshow("foo", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()





