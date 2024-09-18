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
results = model.predict("Screenshot 2024-09-18 015108.png", conf=0.5)

img = cv2.imread("Screenshot 2024-09-18 015108.png")

with open('parking_space.pkl', 'rb') as file:
    parallelograms = pickle.load(file)

for result in results:
    obb = result.obb.xyxyxyxy.detach().cpu().numpy()
    # obb = result.obb.xyxyxyxy
    # print(obb)
    print(obb)
    result.save(filename="result.jpg")

start = time.perf_counter()

for p in parallelograms:
    for bb in obb:
        x_c = np.mean([point[0] for point in bb])
        y_c = np.mean([point[1] for point in bb])
        # if (min(p.points[0][0], p.points[3][0]) < x_c < max(p.points[1][0], p.points[2][0]) and
        #     min(p.points[1][1], p.points[0][1]) < y_c < max(p.points[2][1], p.points[3][1])):
        if cv2.pointPolygonTest(p.points, (x_c,y_c), False) == 1.0:
            print(x_c)
            print(y_c)
            print(p.points)
            p.occupied = True
            p.draw(img)
        else:
            p.draw(img)

print(time.perf_counter()-start)
cv2.namedWindow("foo", cv2.WINDOW_NORMAL)

while True:
    # cv2.imshow("Parallelogram Drawer", img)
    cv2.imshow("foo", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cv2.destroyAllWindows()





