import getopt
import os
import sys
import tkinter as tk
from ui.MainWindow import MainWindow
from ui.MainCommand import MainCommand

if __name__ == "__main__":
    try:
        os.mkdir("Files")
    except FileExistsError:
        pass

    try:
        opts, args = getopt.getopt(sys.argv[1:], "c", ["cli"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    interface = "gui"

    for o, a in opts:
        if o in ("-c", "--cli"):
            interface = "cli"

    if interface == "gui":
        root = tk.Tk()
        MainWind = MainWindow(root)
        root.mainloop()
    elif interface == "cli":
        MainComm = MainCommand()
        MainComm.StartCli()