"""
Author: Gemini
"""

import cv2
import numpy as np

# 1. Define 3D object points (in the object's local coordinate space)
# Assuming two triangles. The first has side lengths of 1, 2, sqrt5. The second has 2, sqrt2, sqrt2
object_points = np.array([
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [0.0, 2.0, 0.0],
    [-1.0, 1.0, 0.0]
], dtype=np.float32)

# 2. Define corresponding 2D image points
# These represent the pixel coordinates where the 3D points appear in the image
# Must have same order as object points
image_points = np.array([
    [304.8, 253.6],
    [335.0, 281.0],
    [386.0, 218.3],
    [317.3, 210.16]
], dtype=np.float32)

# 3. Define the camera matrix (Intrinsic parameters)
# Assuming a camera with a 640x480 resolution
focal_length = 50.0
center_x = 320.0
center_y = 240.0

camera_matrix = np.array([
    [focal_length, 0, center_x],
    [0, focal_length, center_y],
    [0, 0, 1]
], dtype=np.float32)

# 4. Define distortion coefficients 
# Assuming an ideal pinhole camera with no lens distortion for this mock
dist_coeffs = np.zeros((4, 1), dtype=np.float32)

# 5. Solve PnP to find the rotation (rvec) and translation (tvec) vectors
success, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)

# 6. Output the results
if success:
    print("solvePnP was successful!\n")
    
    print("Translation Vector (tvec):")
    print("This represents the [x, y, z] position of the object relative to the camera.")
    print(tvec)
    
    print("\nRotation Vector (rvec):")
    print("This is an axis-angle representation of the object's 3D rotation.")
    print(rvec)
    
    # Optional but highly recommended: Convert the rotation vector to a 3x3 rotation matrix
    rmat, _ = cv2.Rodrigues(rvec)
    print("\nRotation Matrix (rmat):")
    print("This 3x3 matrix is easier to use for standard 3D math and transformations.")
    print(rmat)
else:
    print("solvePnP failed to find a solution.")