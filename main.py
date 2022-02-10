import PySimpleGUI as sg


main_menu_layout = [
    [sg.Text("Image Enhaner - GROUP x")],
    [sg.Text("Click on any image below :")],
    [
        sg.Button("", image_filename="images_original/1-1.png", key="img1"),
        sg.Button("", image_filename="images_original/001.jpg", key="img2"),
        sg.Button("", image_filename="images_original/3-1.jpg", key="img3"),
        sg.Button("", image_filename="images_original/011.jpg", key="img4"),
        sg.Button("", image_filename="images_original/a.png", key="img5")
    ]
]


# Create the Window
window = sg.Window('Window Title', main_menu_layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break

window.close()