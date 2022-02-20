import PySimpleGUI as sg
import os
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

# read the image
imOriginal = Image.open("images_original/001.jpg")

# Brighten the img
brightnessEnhancer = ImageEnhance.Brightness(imOriginal)
imBrighter = brightnessEnhancer.enhance(1.4)

# Remove some noise in the image
denoise = cv2.fastNlMeansDenoisingColored(imBrighter.__array__(), h=20, hColor=15)

# final image
imDenoise = Image.fromarray(denoise)
imFinal = imDenoise.copy()


# Special effects
draw = ImageDraw.Draw(imFinal)

font = ImageFont.truetype("impact.ttf", 60)

draw.text((60,20), "ME AND THE BOYS WHEN", font=font, stroke_width=3, stroke_fill=(0,0,0))
draw.text((40,imDenoise.height - 100), "WE FINISH ISE ASSIGNMENT", font=font, stroke_width=3, stroke_fill=(0,0,0), align="center")



# imFinal.show()

def show():
    tempImageDirPath = "./temp/img3"
    if (not os.path.exists(tempImageDirPath)):
        os.makedirs(tempImageDirPath)

    imOriginalPath = f"{tempImageDirPath}/imOriginal.png"
    imOriginal.save(imOriginalPath)

    imFinalPath = f"{tempImageDirPath}/imFinal.png"
    imFinal.save(imFinalPath)

    imBlank = Image.new("1", size=imOriginal.size)
    imBlankPath = f"{tempImageDirPath}/imBlank.png"
    imBlank.save(imBlankPath)

    imDenoisePath = f"{tempImageDirPath}/imDenoise.png"
    imDenoise.save(imDenoisePath)

    col1 = [
        [sg.Text("Original image", font=("Arial", 24, "normal"))],
        [sg.Image(imOriginalPath, subsample=2, key="imOriginal")]
    ]
    col2 = [
        [sg.Text("Enhanced image", font=("Arial", 24, "normal"))],
        [sg.Image(imBlankPath, key="imFinal")],
        [sg.Button("Show", key="showFinal")]

    ]
    col3 = [
        [sg.Text("Special effect", font=("Arial", 24, "normal"))],
        [sg.Image(imBlankPath, key="imSpecialEffect")],
        [sg.Button("Show", key="showSpecialEffect")]
    ]

    layout = [[sg.Column(col1), sg.VerticalSeparator(), sg.Column(col2), sg.VerticalSeparator(), sg.Column(col3)]]

    # Create the Window
    window = sg.Window('3 bears', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        if event == "showFinal":
            window["imFinal"].update(filename=imDenoisePath)
        if event == "showSpecialEffect":
            window["imSpecialEffect"].update(filename=imFinalPath)

    window.close()


if __name__ == '__main__':
    show()
