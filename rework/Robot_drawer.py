import cv2
import numpy as np

resolution_k = 5
segmetn_size = 2.2

output_sprite = np.zeros((18 * resolution_k, 18 * resolution_k, 4))
cv2.circle(output_sprite, (9 * resolution_k, 9 * resolution_k), 9 * resolution_k, ( 255,255,255, 255), -1)
cv2.rectangle(output_sprite, (18 * resolution_k, 0), (18 * resolution_k - int(segmetn_size * resolution_k), 18 * resolution_k), (0, 0, 0, 0), -1)

cv2.imshow("Robot_sprite", output_sprite)
cv2.waitKey()
cv2.imwrite("Robot_sprite.png", output_sprite)