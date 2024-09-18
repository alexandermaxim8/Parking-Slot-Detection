import numpy as np
import cv2

class Parallelogram:
    def __init__(self, points, obj_id):
        self.points = np.array(points, dtype=np.int32)
        self.obj_id = obj_id
        self.occupied = False
        self.cx, self.cy = self.centroid()
        sorted_points = sorted(self.points, key=self.angle_from_ctr)
        self.points = np.array(sorted_points, dtype=np.int32)
        print(self.points)

    def centroid(self):
        center = np.mean(self.points, axis=0)
        return int(center[0]), int(center[1])

    def draw(self, img):
        if self.occupied:
            cv2.polylines(img, [self.points], isClosed=True, color=(0, 0, 255), thickness=2)
            cv2.putText(img, f"ID: {self.obj_id}", (self.cx - 20, self.cy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.polylines(img, [self.points], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(img, f"ID: {self.obj_id}", (self.cx - 20, self.cy), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def angle_from_ctr(self, point):
        return np.arctan2(point[1] - self.cy, point[0] - self.cx)