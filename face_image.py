import numpy as np
import cv2
from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk
import tkinter.font as tkFont
import os
print("Started processing face image")

tempImageDirPath = "./temp/img5"
if (not os.path.exists(tempImageDirPath)):
    os.makedirs(tempImageDirPath)

#read image
face = cv2.imread('./images_original/a.png')

# LAB Color Model
LAB_Color = cv2.cvtColor(face, cv2.COLOR_BGR2LAB)

# YCbCr Filtering
ycbCr_image = cv2.cvtColor(face, cv2.COLOR_BGR2YCrCb)

# Threshold
res, thresh = cv2.threshold(face, 120, 255, cv2.THRESH_BINARY)

# Gabor Filter
def create_gaborfilter():
    filters = []
    num_filters = 16
    ksize = 35 
    sigma = 3.0 
    lambd = 10.0
    gamma = 0.5
    psi = 0 
    for theta in np.arange(0, np.pi, np.pi / num_filters):
        kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_64F)
        kern /= 1.0 * kern.sum()
        filters.append(kern)
    return filters

def apply_filter(img, filters):
    newimage = np.zeros_like(img)
    depth = -1
     
    for kern in filters:
        image_filter = cv2.filter2D(img, depth, kern) 
        np.maximum(newimage, image_filter, newimage)
    return newimage

gfilters = create_gaborfilter()
gabor_image = apply_filter(face, gfilters)

# Sharpening using addWeighted()
sharpen_image1 = cv2.addWeighted(face, 1.5, LAB_Color, -0.5, 0)
sharpen_image2 = cv2.addWeighted(sharpen_image1, 1.1, ycbCr_image, -0.1, 0)
sharpen_image3 = cv2.addWeighted(sharpen_image2, 1.1, gabor_image, -0.1, 0)
enhanced_image = sharpen_image3.copy()
cv2.imwrite(f"{tempImageDirPath}/EnhancedImage.jpg", enhanced_image)

# Putting a text
x,y,w,h = 0,0,400,20

# Create background rectangle with color
cv2.rectangle(sharpen_image3, (x,x), (x + w, y + h), (255,255,255), -1)

#new image
new_image = cv2.putText(
  img = sharpen_image3,
  text = "MAN OF THE YEAR",
  org=(x + int(w/10),y + int(h/0.9)),
  fontFace = cv2.FONT_HERSHEY_COMPLEX,
  fontScale = 0.7,
  color = (0, 0, 0),
  thickness = 1
)

#add text
position = (170, 350)
text = "Featuring\nThe\nLegendary\nSmile"
font_scale = 0.75
color = (0, 0, 255)
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
line_height = text_size[1] + 5
x, y0 = position

for i, line in enumerate(text.split("\n")):
    y = y0 + i * line_height
    cv2.putText(img = sharpen_image3,
                text = line,
                org = (x, y),
                fontFace = font,
                fontScale = font_scale,
                color = color,
                thickness = thickness
            )

position = (10, 350)
text = "90's Pop\nIcon"
font_scale = 0.75
color = (0, 0, 255)
thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
line_height = text_size[1] + 5
x, y0 = position

for i, line in enumerate(text.split("\n")):
    y = y0 + i * line_height
    cv2.putText(img = sharpen_image3,
                text = line,
                org = (x, y),
                fontFace = font,
                fontScale = font_scale,
                color = color,
                thickness = thickness
            )

row, col = sharpen_image3.shape[:2]
bottom = sharpen_image3[row-2:row, 0:col]

#red border
bordersize = 10
border = cv2.copyMakeBorder(
    sharpen_image3,
    top=bordersize,
    bottom=bordersize,
    left=bordersize,
    right=bordersize,
    borderType=cv2.BORDER_CONSTANT,
    value=[0, 0, 255],
)

cv2.imwrite(f"{tempImageDirPath}/FinalImage.jpg", border)

print("Finished processing face image")


# GUI
# https://realpython.com/python-gui-tkinter/
root = Toplevel()
root.geometry("1200x600")
root.title("Image Enhancer")
fontStyle = tkFont.Font(family="Lucida Grande", size=20)

label = Label(root, text = "Original Image", compound='top', font = fontStyle)
label.grid(row = 1, column = 1)

original_image = ImageTk.PhotoImage(Image.open("./images_original/a.png"))
label = Label(root, image = original_image, compound='top')
label.grid(row = 2, column = 1)

# Separator
separator = ttk.Separator(root, orient="vertical").grid(row = 1, column=2, sticky='ew', ipadx=50)

label = Label(root, text = "Enhanced Image", compound='top', font = fontStyle)
label.grid(row = 1, column = 3)

#image after doing transformation
def enhanced_image():
    global image1
    image1 = ImageTk.PhotoImage(Image.open(f"{tempImageDirPath}/EnhancedImage.jpg"))
    label = Label(root, image = image1, compound='top')
    label.grid(row = 2, column = 3)

#show button
button_show = Button(root, text = "Show", command = enhanced_image)
button_show.grid(row = 3, column = 3)

# Separator
separator = ttk.Separator(root, orient="vertical").grid(row = 1, column=4, sticky='ew', ipadx=50)

label = Label(root, text = "Special Effect", compound='top', font = fontStyle)
label.grid(row = 1, column = 5)

#image with texts
def special_effects_image():
    global image2
    image2 = ImageTk.PhotoImage(Image.open(f"{tempImageDirPath}/FinalImage.jpg"))
    label = Label(root, image = image2, compound='top')
    label.grid(row = 2, column = 5)

#show button
button_show = Button(root, text = "Show", command = special_effects_image)
button_show.grid(row = 3, column = 5)

def show():
    #open the window
    root.mainloop()

if __name__ == '__main__':
    show()


