# img_viewer.py
from datetime import datetime

import PySimpleGUI as sg
import os.path

from sqlalchemy.dialects.mysql import DATETIME

from whisperx.ui.whisperx_executer import startTranscribe

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),


    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
    [
        sg.Button("transcribe", key="-START-")
    ],
    [sg.Text("StartTime: "),
    sg.Text("Not yet started", key="-STARTTIME-"),
    ],

    [
    sg.Text("Finish: "),
    sg.Text("Not yet started", key="-FINISHTIME-"),
    ]
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Start transcribing of file on left")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Multiline(size=(40, 40), key="-OUTPUT-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Whisperxtest", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-START-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-STARTTIME-"].update(datetime.now().__str__())
            #window["-TOUT-"].update(filename)
            startTranscribe(filename,window)

            window["-FINISHTIME-"].update(datetime.now().__str__())
        except:
            pass



window.close()