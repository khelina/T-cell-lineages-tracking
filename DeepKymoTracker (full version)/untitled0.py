import cv2
import numpy as np

image=np.zeros((100,100), np.uint8)
image[50:60,50:60]=255

im2, contours, hierarchy = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cell=contours[0]
   
#area=np.count_nonzero(image)
perimeter_cv2=np.round(cv2.arcLength(cell,True),2)
#circularity=np.round(4*math.pi*area/perimeter**2,2)     
#print("area=", area)
print("perimeter_cv2=", perimeter_cv2)

#cv2.imwrite(r"C:\Users\helina\Desktop\test.tif", image)


def get_perimeter_from_contour(contour):
    perimeter = 0.0
    # Loop through points
    for i in range(len(contour)):
        pt1 = contour[i][0]
        pt2 = contour[(i + 1) % len(contour)][0]  # Next point, with wrap-around
        dist = np.linalg.norm(pt1 - pt2)
        perimeter += dist
    return perimeter

def get_traced_perimeter(image):
    """
    Find contours and compute the perimeter more accurately.
    """
    im2, contours, hierarchy= cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Use NO approximation
    if len(contours) == 0:
        return 0
    print("len(contours)=", len(contours))
    # Choose the largest contour
    main_contour = max(contours, key=cv2.contourArea)
    perimeter = get_perimeter_from_contour(main_contour)
    return perimeter
################################
perimeter_new=get_traced_perimeter(image)
print("perimeter_new=", perimeter_new)
###########################################
import cv2
import numpy as np
from skimage import measure

def calculate_perimeter(image):
    # Label the regions in the binary image
    labeled_image = measure.label(image, connectivity=2)
    
    # Find the properties of the labeled regions
    properties = measure.regionprops(labeled_image)
    
    perimeter = 0.0
    
    for prop in properties:
        # Each property has a 'perimeter' attribute
        perimeter += prop.perimeter
    
    return perimeter

# Create a sample binary image
image = np.zeros((100, 100), np.uint8)
image[50:60, 50:60] = 255

# Calculate perimeter using the ImageJ-like method
perimeter_imagej = calculate_perimeter(image)
print("perimeter_imagej=", perimeter_imagej)
################################
import cv2
import numpy as np

def calculate_perimeter(image):
    # Find contours in the binary image
    im2, contours, hierarchy= cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #print("contours=", contours)
    #print("len(contours)=", len(contours))
    perimeter = 0.0
    
    # Loop through each contour found
    for contour in contours:
        #print("contour=", contour)
        print("len(contour)=", len(contour))
        # Calculate the perimeter using a more accurate method
        for i in range(len(contour)):
            pt1 = contour[i][0]
            print("pt1=", pt1)
            pt2 = contour[(i + 1) % len(contour)][0]  # Wrap around to the first point
            dist = np.linalg.norm(pt1 - pt2)
            perimeter += dist
            
    return perimeter

# Create a sample binary image
image = np.zeros((100, 100), np.uint8)
image[50:60, 50:60] = 255  # A square object

# Calculate perimeter using the custom method
perimeter_result = calculate_perimeter(image)
print("Calculated Perimeter:", perimeter_result)