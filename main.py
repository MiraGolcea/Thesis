import tkinter as tk
from ttbuilder import TTbuilder
from ttsolver import TTsolver
import sys
import subprocess
import threading


TT  = None   # Timetable to be generated
sem = None   # True for semester 1, False for semester 2


class AppWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Time Table")
        self.root.geometry('240x300')
        self.solver = None
        # Logo
        logo = tk.PhotoImage(file='uvt.png')
        logo_label = tk.Label(image=logo, compound=tk.CENTER)
        logo_label.image = logo
        logo_label.pack() #logo_label.grid(column=1, row=0)

        # Menus, items
        appMenu = tk.Menu(self.root)
        self.root.config(menu=appMenu)

        curricMenu = tk.Menu(appMenu)
        appMenu.add_cascade(label="Curriculum", menu=curricMenu)
        curricMenu.add_command(label="First Semester", command=self.editSem1)
        curricMenu.add_command(label="Second Semester", command=self.editSem2)

        lectMenu = tk.Menu(appMenu)
        appMenu.add_cascade(label="Lecturers", menu=lectMenu)
        lectMenu.add_command(label="Time Management Sem1", command=self.availability1)
        lectMenu.add_command(label="Time Management Sem2", command=self.availability2)

        settingsMenu = tk.Menu(appMenu)
        appMenu.add_cascade(label="Settings", menu=settingsMenu)
        settingsMenu.add_command(label="Configure", command=self.settings)

        helpMenu = tk.Menu(appMenu)
        appMenu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="Using Instructions", command=self.help)

        # Buttons
        self.opt = tk.IntVar()
        self.opt.set(True)
        self.chkbutton = tk.Checkbutton(self.root, text="Optimize", variable=self.opt)
        self.chkbutton.pack()
        self.button1 = tk.Button(self.root, text = 'Generate Semester 1 Timetable', command=self.sem1)
        self.button1.pack()
        self.button2 = tk.Button(self.root, text = 'Generate Semester 2 Timetable', command=self.sem2)
        self.button2.pack()

        self.root.mainloop()

    def buildTT(self, tt):
        global TT
        if tt == []:
           button = self.button1 if(sem) else self.button2
           button.configure(text = "Failed To Generate A Timetable")
           print("A timetable could not be generated")
        else: 
           TT = tt
           self.root.destroy()

    def sem1(self):
        global sem
        sem = True
        self.button1.configure(text = "Working ...")
        self.button1.configure(state = tk.DISABLED)
        self.button2.configure(state = tk.DISABLED) 
        self.root.update()
        self.solver = TTsolver(self.buildTT, True, self.opt.get())
        solvThread = threading.Thread(target = self.solver.Check, args = (), daemon = True)
        solvThread.start()

    def sem2(self):
        global semI
        semI = False
        self.button2.configure(text="Working ...")
        self.button2.configure(state = tk.DISABLED)
        self.button1.configure(state = tk.DISABLED) 
        self.root.update()
        self.solver = TTsolver(self.buildTT, False, self.opt.get())
        solvThread = threading.Thread(target = self.solver.Check, args = (), daemon = True)
        solvThread.start()       

    def editSem1(self):
        self.editTextfile('UVT_Computer_Science_Semester1.py')

    def editSem2(self):
        self.editTextfile('UVT_Computer_Science_Semester2.py') 
  
    def availability1(self):
        self.editTextfile('UVT_Computer_Science_Availability1.py')

    def availability2(self):
        self.editTextfile('UVT_Computer_Science_Availability2.py')

    def settings(self):
        self.editTextfile('UVT_Computer_Science_Settings.py')

    def help(self):
        self.editTextfile('UVT_Computer_Science_Instructions.txt')

    def editTextfile(self, fName):
        editor = {'win32':'notepad', 'linux':'gpedit', 'linux2':'gpedit'}
        try: # This works for Windows and Linux
           subprocess.run([editor[sys.platform] , fName], check=True)
        except: # For other OS we kindly ask the user to manually open the file for editing
           print("Open 'UVT_Computer_Science_Semester2.py' in a text editor")


AppWindow()
TTbuilder(TT, sem)