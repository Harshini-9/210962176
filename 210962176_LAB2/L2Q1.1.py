import cv2
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Create object
root = Tk()

# Adjust size
root.geometry("1000x600")

# Global variables to hold the current images
original_image = None
original_image_cv = None  # OpenCV format image for transformations


# Change the label text and apply the selected transformation
def show():
    label.config(text=clicked.get())
    apply_transformation()


# Open image file and display in rectangle
def open_image():
    global original_image, original_image_cv
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg")])
    if file_path:
        try:
            # Load image with OpenCV
            image_cv = cv2.imread(file_path)
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

            # Resize image to fit the rectangles
            image_cv = cv2.resize(image_cv, (350, 200))

            # Save OpenCV image for transformations
            original_image_cv = image_cv

            # Convert image to PIL format
            original_image = Image.fromarray(image_cv)

            # Convert image to PhotoImage format for Tkinter
            photo = ImageTk.PhotoImage(original_image)

            # Clear previous images from the canvas
            canvas.delete("original")
            canvas.delete("transformed")

            # Display the original image in the left part of the canvas
            canvas.create_image(175, 150, image=photo, tags="original")

            # Keep a reference to the image to prevent garbage collection
            canvas.original_image = photo
        except Exception as e:
            print(f"Error loading image: {e}")


# Apply selected transformation based on dropdown menu
def apply_transformation():
    if original_image_cv is not None:
        # Convert OpenCV image to float32 for precision
        image_np = original_image_cv.astype(np.float32)

        # Apply the selected transformation
        transformation = clicked.get()

        if transformation == "Image negative":
            # Apply image negative transformation using OpenCV
            img_neg = cv2.bitwise_not(original_image_cv)
            transformed_image_np = img_neg
        elif transformation == "Log transformation":
            # Apply log transformation using OpenCV
            img_log = (np.log(image_np + 1) / np.log(1 + np.max(image_np))) * 255
            img_log = np.array(img_log, dtype=np.uint8)
            transformed_image_np = img_log
        elif transformation == "Gamma correction":
            # Apply gamma correction using OpenCV
            # Apply Gamma=2.2 on the normalized image and then multiply by scaling constant (For 8 bit, c=255)
            gamma_two_point_two = np.array(255 * (image_np / 255) ** 2.2, dtype='uint8')
            # Similarly, Apply Gamma=0.4
            gamma_correction = np.array(255 * (image_np / 255) ** 0.4, dtype='uint8')

            # Here we choose to display gamma correction with Gamma=0.4 for simplicity
            transformed_image_np = gamma_correction
        elif transformation == "GrayScaling ":
            gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
            transformed_image_np = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        else:
            transformed_image_np = image_np.astype(np.uint8)  # No transformation

        # Convert the transformed image back to PIL format
        transformed_image = Image.fromarray(transformed_image_np)

        # Convert image to PhotoImage format for Tkinter
        photo_transformed = ImageTk.PhotoImage(transformed_image)

        # Display the transformed image in the right part of the canvas
        canvas.create_image(825, 150, image=photo_transformed, tags="transformed")

        # Keep a reference to the image to prevent garbage collection
        canvas.transformed_image = photo_transformed
    else:
        print("No image to transform.")


# Dropdown menu options
options = [
    "Image negative", "Log transformation", "Gamma correction", "GrayScaling"]

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set("Image negative")

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()

# Create button, it will change label text
button = Button(root, text="Click Me", command=show)
button.pack()

# Create Open Image button
open_image_button = Button(root, text="Open Image", command=open_image)
open_image_button.pack()

# Create Label
label = Label(root, text=" ")
label.pack()

# Create Canvas
canvas = Canvas(root, width=1000, height=500, bg="white")
canvas.pack()

# Execute tkinter
root.mainloop()
