import PySimpleGUI as sg
import cv2, numpy as np, os, shutil
from PIL import Image, ImageFilter, ImageEnhance, ImageTk

imOriginal = Image.open("images_original/1-1.png")

def adjustBrightness(im, magnitude):
    Enhancer = ImageEnhance.Brightness(im)
    return Enhancer.enhance(magnitude)

def adjustContrast(im, magnitude):
    Enhancer = ImageEnhance.Contrast(im)
    return Enhancer.enhance(magnitude)

def adjustSharpness(im, magnitude):
    Enhancer = ImageEnhance.Sharpness(im)
    return Enhancer.enhance(magnitude)



def show():
    tempImageDirPath = "./temp/img2"

    if (not os.path.exists(tempImageDirPath)):
        os.makedirs(tempImageDirPath)
    if (not os.path.exists(f"{tempImageDirPath}/temp/")):
        os.makedirs(f"{tempImageDirPath}/temp/")

    imOriginalPath = f"{tempImageDirPath}/imOriginal.png"
    imOriginal.save(imOriginalPath)

    imBlank = Image.new("1", size=imOriginal.size)
    imBlankPath = f"{tempImageDirPath}/imBlank.png"
    imBlank.save(imBlankPath)

    col1 = [
        [sg.Text("Before :")],
        [sg.Image(imOriginalPath, subsample=2)],
        [sg.Text("After : ")],
        [sg.Image(imOriginalPath, subsample=2, key="imgAfter")]
    ]

    col2 = [
        [sg.T('Operations', font='_ 18', justification='c', expand_x=True)],
        [sg.Text("Brightness : ")],
        [sg.Slider(range=(0, 10), default_value=1, resolution=0.1, tick_interval=5, orientation="h", enable_events=True, key="sliderBrightness")],
        [sg.HorizontalSeparator()],
        [sg.Text("Contrast : ")],
        [sg.Slider(range=(0, 10), default_value=1, resolution=0.1, tick_interval=5, orientation="h", enable_events=True, key="sliderContrast")],
        [sg.HorizontalSeparator()],
        [sg.Text("Sharpness : ")],
        [sg.Slider(range=(0, 10), default_value=1, resolution=0.1, tick_interval=5, orientation="h", enable_events=True, key="sliderSharpness")],
        [sg.Button("Apply", key="btnApply"), sg.Button("Reset", key="btnReset")],
        [sg.Button("Save!", key="btnSave")]
    ]

    layout = [
        [sg.T('X-ray image..?', font='_ 18', justification='c', expand_x=True)],
        [sg.Column(col1), sg.VerticalSeparator(), sg.Column(col2)]
    ]

    # Create the Window
    window = sg.Window('x rays maybe', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    count = 0
    baseImg = imOriginal
    currentImg = imOriginal
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        if event == "sliderBrightness":
            # print(values["sliderBrightness"])
            window["sliderSharpness"].update(disabled=True)
            window["sliderContrast"].update(disabled=True)
            currentImg = adjustBrightness(baseImg, float(values["sliderBrightness"]))
        if event == "sliderSharpness":
            # print(values["sliderSharpness"])
            window["sliderBrightness"].update(disabled=True)
            window["sliderContrast"].update(disabled=True)
            currentImg = adjustSharpness(baseImg, float(values["sliderSharpness"]))
        if event == "sliderContrast":
            # print(values["sliderContrast"])
            window["sliderSharpness"].update(disabled=True)
            window["sliderBrightness"].update(disabled=True)
            currentImg = adjustContrast(baseImg, float(values["sliderContrast"]))
        if event == "btnApply":
            print("updated base image")
            baseImg = currentImg
            window["sliderSharpness"].update(value=1, disabled=False)
            window["sliderContrast"].update(value=1, disabled=False)
            window["sliderBrightness"].update(value=1, disabled=False)
        if event == "btnReset":
            baseImg = imOriginal
            currentImg = baseImg
            print("resetted base image")
            window["sliderSharpness"].update(value=1, disabled=False)
            window["sliderContrast"].update(value=1, disabled=False)
            window["sliderBrightness"].update(value=1, disabled=False)
        if event == "btnSave":
            currentImg.save(f"{tempImageDirPath}/done.png")
            sg.PopupOK("Saved")

        currentImg.save(f"{tempImageDirPath}/temp/{count}.png")
        window["imgAfter"].update(f"{tempImageDirPath}/temp/{count}.png", subsample=2)

        print(count)
        count += 1


    shutil.rmtree(f"{tempImageDirPath}/temp/")
    window.close()

if __name__ == '__main__':
    show()
