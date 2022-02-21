import PySimpleGUI as sg
import bears_image, door_image, scenery_image, xray_image
main_menu_layout = [
    [sg.Text("Image Enhaner - GROUP x", font=("Arial", 24, "normal"))],
    [sg.Text("Click on any image below :")],
    [
        sg.Button("", image_filename="./images_png/0.png", key="img1", image_subsample=3),
        sg.Button("", image_filename="./images_png/1.png", key="img2", image_subsample=3),
        sg.Button("", image_filename="./images_png/2.png", key="img3", image_subsample=3),
        sg.Button("", image_filename="./images_png/3.png", key="img4", image_subsample=10),
        sg.Button("", image_filename="./images_png/4.png", key="img5", image_subsample=2)
    ]
]


# Create the Window
window = sg.Window('Image enhancer - main menu', main_menu_layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    if event == "img1":
        bears_image.show()
    if event == "img2":
        scenery_image.show()
    if event == "img3":
        xray_image.show()
    if event == "img4":
        door_image.show()
    if event == "img5":
        import face_image
        face_image.show()
        # note : this button can only be clicked once
        # if want to click the button again, please restart the program
    else :
        pass
window.close()