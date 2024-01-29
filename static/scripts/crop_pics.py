import cv2
import glob


# Function to center crop images
def center_crop(image):
    height, width = image.shape[:2]
    if height == width:
        return image  # Already a square
    elif height > width:
        start = (height - width) // 2
        return image[start:start + width, :]
    else:
        start = (width - height) // 2
        return image[:, start:start + height]

# Function to center crop all images in the folder
def center_crop_all_images(image_paths):
    for img_path in image_paths:
        img = cv2.imread(img_path)
        if img is not None:
            img = center_crop(img)
            # Save or process the cropped image here
            # For example, save it back to the same location:
            cv2.imwrite(img_path, img)
            print('cropped:', img_path)

# Example usage
image_paths = glob.glob('/Users/gauravkaul/Desktop/backprop64.github.io/static/img/*')
 
center_crop_all_images(image_paths)
