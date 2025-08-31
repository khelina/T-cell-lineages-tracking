import cv2
import numpy as np

def find_boundary_points(image):
    """
    Find the boundary points of the white shape in a binary image.
    """
    # Find contours with no approximation (CHAIN_APPROX_NONE)
    im2, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print("len(contours)=", len(contours))
    if len(contours) == 0:
        return []
   
    # Assume the largest contour is our shape
    cnt = contours[0]
    # cnt shape: Nx1x2, flatten to Nx2
    boundary_points = [pt[0] for pt in cnt]
    return boundary_points

def calculate_perimeter(boundary_points):
    """
    Calculate perimeter by summing Euclidean distances between consecutive boundary points:
    - Straight segments as 1
    - Diagonal segments as sqrt(2)
    """
    perimeter = 0.0
    sqrt2 = np.sqrt(2)

    for i in range(len(boundary_points)):
        p1 = boundary_points[i]
        p2 = boundary_points[(i+1) % len(boundary_points)]  # wrap-around
        dx = abs(p2[0] - p1[0])
        dy = abs(p2[1] - p1[1])
        if dx > 0 and dy > 0:
            # diagonal segment
            perimeter += sqrt2
        else:
            # horizontal or vertical segment
            perimeter += 1
    return perimeter

# Load image (assumed to be binary: black background, white shape)
# Make sure the shape is white (255), background black (0)
image_path = 'your_image.png'  # replace with your image path
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Threshold to ensure binary
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Find boundary points
boundary = find_boundary_points(binary)

if boundary:
    perimeter = calculate_perimeter(boundary)
    print("Estimated perimeter (ImageJ-like):", perimeter)
else:
    print("No shape found.")
##################################
my_image=cv2.imread(r"C:\Users\helina\Desktop\test.tif",-1)
points=find_boundary_points(my_image)