import PySimpleGUI as sg
import os
import numpy as np
import cv2
from PIL import Image, ImageEnhance
print("Started processing scenery image")

# read the image
imOriginal = Image.open("./images_original/011.jpg")

# Brighten the img
brightnessEnhancer = ImageEnhance.Brightness(imOriginal)
imBrighter = brightnessEnhancer.enhance(1.7)

# Remove some noise in the image
denoise = cv2.fastNlMeansDenoisingColored(imBrighter.__array__(), h=7, hColor=7)
hsv = cv2.cvtColor(denoise, cv2.COLOR_RGB2HSV)

# Slightly brighten the image again by change the HSV value
h, s, v = cv2.split(hsv)
newHSV = cv2.merge([cv2.add(h, 0), cv2.add(s, 0), cv2.add(v, 20)])
final = cv2.cvtColor(newHSV, cv2.COLOR_HSV2RGB)

# final image
imFinal = Image.fromarray(final)


# Special effects
postcardTemplate = Image.open("./internet_images/vykort_pressade_blommor_baksida.png")
# link : https://charlottaduse.com/wp-content/uploads/2020/07/vykort_pressade_blommor_baksida.png
postcardTemplate = postcardTemplate.convert("RGBA")
postcardTemplateArray = np.asarray(postcardTemplate)
for i in range(postcardTemplateArray.shape[0]):
    for j in range(postcardTemplateArray.shape[1]):
        if postcardTemplateArray[i][j][0] > 127 and postcardTemplateArray[i][j][1] > 127 and postcardTemplateArray[i][j][2] > 127:
            # if the pixel is white, make it transparent
            # 0 alpha = transparent
            postcardTemplateArray[i][j][3] = 0

postcardTemplateTransparent = Image.fromarray(postcardTemplateArray)


imPostcardBackground = imFinal.copy()
imPostcardBackground = imPostcardBackground.convert("RGBA")
imPostcardBackgroundFlipped = imPostcardBackground.transpose(Image.FLIP_LEFT_RIGHT)
postcardTemplateResized = postcardTemplateTransparent.resize(imFinal.size)
imPostcardBackgroundFlipped.paste(postcardTemplateResized, (0, 0), postcardTemplateResized)

imPostcardFinal = imPostcardBackgroundFlipped.copy()

print("Finished processing scenery image")


def show():
    tempImageDirPath = "../temp/img1"
    if (not os.path.exists(tempImageDirPath)):
        os.makedirs(tempImageDirPath)

    imOriginalPath = f"{tempImageDirPath}/imOriginal.png"
    imOriginal.save(imOriginalPath)

    imFinalPath = f"{tempImageDirPath}/imFinal.png"
    imFinal.save(imFinalPath)

    imBlank = Image.new("1", size=imOriginal.size)
    imBlankPath = f"{tempImageDirPath}/imBlank.png"
    imBlank.save(imBlankPath)

    imPostcardFinalPath = f"{tempImageDirPath}/imPostcardFinal.png"
    imPostcardFinal.save(imPostcardFinalPath)

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
    window = sg.Window('house image', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        if event == "showFinal":
            window["imFinal"].update(filename=imFinalPath)
        if event == "showSpecialEffect":
            window["imSpecialEffect"].update(filename=imPostcardFinalPath)

    window.close()


if __name__ == '__main__':
    show()
