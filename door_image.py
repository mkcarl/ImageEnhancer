import PySimpleGUI as sg
import os
import cv2
from PIL import Image, ImageFont, ImageDraw
print("Started processing door image")

# read the image
#change directory as needed
imgFileName = "./images_original/3-1.jpg"

#reading image
imageColor = cv2.imread(imgFileName, cv2.IMREAD_COLOR)
imOriginal = Image.fromarray(cv2.cvtColor(imageColor, cv2.COLOR_BGR2RGB))

#convertion to HSV colorspace
imageHSV = cv2.cvtColor(imageColor, cv2.COLOR_BGR2HSV)

# Histogram equalisation on the V channel
imageHSV[:, :, 2] = cv2.equalizeHist(imageHSV[:, :, 2])


# convert image back from HSV to RGB
imageConver = cv2.cvtColor(imageHSV, cv2.COLOR_HSV2RGB)


# resize image
scale_percent = 30 # percent of original size
width = int(imageConver.shape[1] * scale_percent / 100)
height = int(imageConver.shape[0] * scale_percent / 100)
dim = (width, height)

resized = cv2.resize(imageConver, dim, interpolation=cv2.INTER_AREA)
imFinal = Image.fromarray(resized)



# Special effects

enhImage = imFinal.copy()
x,y=10,10

c,v=enhImage.width*0.6,enhImage.height*0.95

title_font = ImageFont.truetype("ZakirahsBold.ttf",100)
date_font = ImageFont.truetype("ZakirahsBold.ttf",20)

postertxt="Memories\n in \n Italy"
date="29th March 2018"

poster = ImageDraw.Draw(enhImage)

#adding outline to title text
poster.text((x-1, y-1), postertxt, font=title_font, fill=(0,0,0))
poster.text((x+1, y-1), postertxt, font=title_font, fill=(0,0,0))
poster.text((x-1, y+1), postertxt, font=title_font, fill=(0,0,0))
poster.text((x+1, y+1), postertxt, font=title_font, fill=(0,0,0))

#drawing text over outline
poster.text((x,y),postertxt,(255,255,255), font=title_font)

#drawing date text
poster.text((enhImage.width*0.7,enhImage.height*0.95),date,(255,255,255),font = date_font)

imPoster = enhImage

imageSize = (int(imOriginal.width/4), int(imOriginal.height/4))

print("Finished processing door image")

def show():
    tempImageDirPath = "../temp/img4"
    if (not os.path.exists(tempImageDirPath)):
        os.makedirs(tempImageDirPath)

    imOriginalPath = f"{tempImageDirPath}/imOriginal.png"
    imOriginal.resize(imageSize).save(imOriginalPath)

    imFinalPath = f"{tempImageDirPath}/imFinal.png"
    imFinal.resize(imageSize).save(imFinalPath)

    imBlank = Image.new("1", size=imOriginal.size)
    imBlankPath = f"{tempImageDirPath}/imBlank.png"
    imBlank.resize(imageSize).save(imBlankPath)

    imPosterPath = f"{tempImageDirPath}/imPoster.png"
    imPoster.resize(imageSize).save(imPosterPath)

    col1 = [
        [sg.Text("Original image", font=("Arial", 24, "normal"))],
        [sg.Image(imOriginalPath, key="imOriginal")]
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
    window = sg.Window('door image', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        if event == "showFinal":
            window["imFinal"].update(filename=imFinalPath)
        if event == "showSpecialEffect":
            window["imSpecialEffect"].update(filename=imPosterPath)

    window.close()


if __name__ == '__main__':
    show()
