
import numpy as np
import os
from PIL import Image


import os
import numpy as np
from PIL import Image

def LoadImages(input_data, return_filenames=False):
    if isinstance(input_data, np.ndarray):  
        return [input_data],None if return_filenames else [input_data],None
    elif isinstance(input_data, str):  
        if os.path.isfile(input_data):  
            image = Image.open(input_data)
            image_array = np.array(image).astype(np.float32)
            return [image_array], [os.path.basename(input_data)] if return_filenames else [image_array],[input_data]
        elif os.path.isdir(input_data):  
            images = []
            out_filenames = []
            out_path = []
            for filename in os.listdir(input_data):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(input_data, filename)
                    out_filenames.append(os.path.basename(image_path))
                    out_path.append(image_path)
                    image = Image.open(image_path)
                    image_array = np.array(image).astype(np.float32)
                    if return_filenames:
                        images.append((image_array, filename))
                    else:
                        images.append(image_array)
                    
            return images, out_filenames,out_path
        else:
            raise ValueError("Invalid input path.")
    elif isinstance(input_data, Image.Image):  
        image_array = np.array(input_data).astype(np.float32)
        return [image_array], None if return_filenames else [image_array],None
    else:
        raise ValueError("Input must be a NumPy array, a string (path to an image or folder), or a Pillow Image.")

def SaveImages(images, output_dir, image_names=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    saved_image_names = []  # List to store the names of the saved images

    for i, image in enumerate(images):
        # Check if a name is provided and valid, else generate a default name
        if image_names and i < len(image_names) and image_names[i]:
            filename = image_names[i]
        else:
            filename = f"image_{i}.jpg"

        # Ensure the filename has the correct extension
        filename_with_extension = os.path.splitext(filename)[0] + '.jpg'
        image_path = os.path.join(output_dir, filename_with_extension)

        # Convert and save the image
        pil_image = Image.fromarray(image.astype(np.uint8))
        pil_image.save(image_path)

        # Add the filename to the list of saved image names
        saved_image_names.append(filename_with_extension)

    return saved_image_names