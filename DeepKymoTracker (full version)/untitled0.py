import cv2

def resize_image_aspect_ratio(image, window_size):    
    original_height, original_width = image.shape[:2]
    target_height= window_size   
    aspect_ratio = original_width / original_height
    target_width = int(target_height * aspect_ratio)
    resized_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_AREA)
    return resized_image
