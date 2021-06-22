import tkinter as tk
from scrolledframe import ScrolledFrame


# constants

dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri"]
timeIntervals = ["08:00 – 09:30", "09:40 – 11:10", "11:20 – 12:50", "13:00 – 14:30", "14:40 – 16:10",
                 "16:20 – 17:50", "18:00 – 19:30", "19:40 – 21:10"]
nSlots = 40
year1 = 0
year2 = 1
year3 = 2
years = 3


class TTbuilder:

    def __init__(self, tt, semester1): 
        if tt == None:           # main application window was closed without TT generation
           exit() 
       
        self.tt = tt             # time table triple list tt[cls][course][slot]
        self.semester1 = semester1

        self.root = tk.Tk()  # main window
        self.root.title("Time Table")
        self.root.geometry("1200x700")
        wnd = ScrolledFrame(self.root)
        wnd.pack(expand=True, fill='both')
        self.window = wnd.inner  # scrollable inner window
        self.SetConstants()
        self.Build()
        self.root.mainloop()

    def newFrame(self, r, c, hint, txt): # displays a cell in the time table grid
        colors = ['#fff', 'peach puff', 'DarkSeaGreen1', 'light yellow']
        backgroundColor = colors[hint]
        frame = tk.Frame(master=self.window, relief=tk.SUNKEN, borderwidth=2, bg=backgroundColor)
        frame.grid(row=r, column=c, sticky=tk.NW + tk.SE, ipady=0)
        label = tk.Label(master=frame, text=txt, font=('Arial', 8), bg=backgroundColor)
        label.pack()

    def courseFrame(self, r, c, cspan, txt): # displays a merged cell for a cours name
        frame = tk.Frame(master=self.window, relief=tk.SUNKEN, borderwidth=2, bg='peach puff')
        frame.grid(row=r, column=c, columnspan=cspan, sticky=tk.NW + tk.SE, ipady=0)
        label = tk.Label(master=frame, text=txt, font=('Arial', 8), bg='peach puff')
        label.pack()

    def flatFrame(self, r, c, txt): # displays a borderless cell
        frame = tk.Frame(master=self.window)
        frame.grid(row=r, column=c, ipady=0)
        label = tk.Label(master=frame, text=txt, font=('Arial', 10))
        label.pack()

    def mergeCol(self, r, c, cspan, txt): # displays a cell obtained by merging 'cspan' columns
        frame = tk.Frame(master=self.window)
        frame.grid(row=r, column=c, columnspan=cspan, ipady=0)
        label = tk.Label(master=frame, text=txt, font=('Arial', 10))
        label.pack()

    def mergeRow(self, r, c, rspan, txt): # displays a cell obtained by merging 'rspan' rows
        frame = tk.Frame(master=self.window)
        frame.grid(row=r, column=c, rowspan=rspan, ipady=0)
        label = tk.Label(master=frame, text=txt, font=('Arial', 10))
        label.pack()
    
    def stripTitle(self, text): # returns a lecturer name without academic title
       index = text.find(". ")
       return text[index+2 :] if index != -1 else text
    
    def getCourseName(self, subgroup, timeslot): 
        if subgroup in year1SubgroupRange:
            cls = year1
        if subgroup in year2SubgroupRange:
            cls = year2
        if subgroup in year3SubgroupRange:
            cls = year3
        for course in range(nCourses[cls]):  # for each course lectured to class 'cls'
            if self.tt[cls][course][timeslot] == 1:  # if there is a course in this timeslot
                courseNames = [cNames1, cNames2, cNames3]
                teacherName = tNames[tCourse[cls][course]]
                return (1, courseNames[cls][course] + "   " + teacherName)  # tuple (1, course name + teacher's name)
        for lab in range(nLabs[cls]):  # for each laboratory taught to class 'cls'
            if self.tt[subgroup][lab][timeslot] == 1:  # if there is a lab taught to subgroup 'sg'
                laboratoryNames = [labNames1, labNames2, labNames3]
                teacherName = tNames[tLab[cls][lab]]
                return (2, laboratoryNames[cls][lab] + " - " + self.stripTitle(teacherName))  # tuple (2, lab name + teacher's name)
        return (0, "") # free slot

    def Build(self):
        currentRow = 0 # variable for keeping track of vertical position
        for y in range(years): # make time table for each year
            # Header row
            self.mergeCol(currentRow, 0, 2 + nSubgroups[y], 
                    f"UVT COMPUTER SCIENCE IN ENGLISH 2021/2022 - STUDY YEAR {y + 1} : Semester {1 if self.semester1 else 2}")

            for i in range(nSubgroups[y]):  # write subgroups header
                self.flatFrame(currentRow + 1, 2 + i, f"Subgroup {i + 1}")

            # Rightmost empty column
            self.mergeRow(currentRow + 2, 3 + nSubgroups[y], 45, "    ")

            currentRow += 2
            for i in range(5):  # Write week days
                self.mergeRow(currentRow, 0, 8, dayNames[i])
                for j in range(8):
                    self.newFrame(currentRow + j, 1, 3, f"{timeIntervals[j]}")
                self.mergeCol(currentRow + 8, 0, 2 + nSubgroups[y], " ")  # empty row
                currentRow += 9
            # Current row now is 47 rows lower than the current year's timetable header

            currentRow -= 45  # set back to first time slot (2 rows lower than the header row)
            for sg in SubgroupRange[y]:
                for i in range(nSlots):
                    if i > 0 and i % 8 == 0:  # after 8 time slots (= one day)
                        currentRow += 1  # skip the empty row separating consecutive days
                    (hint, txt) = self.getCourseName(sg, i)  # 'hint' indicates whether 'txt' is a course name, a lab name, or none of them
                    if hint == 1: # we have a course at the current time slot
                       if sg == SubgroupRange[y][0]: # first subgroup of year 'y'
                          self.courseFrame(currentRow + i, 2 + sg - SubgroupRange[y][0], nSubgroups[y], txt)
                          continue
                       else:
                          continue
                    else:
                       self.newFrame(currentRow + i, 2 + sg - SubgroupRange[y][0], hint, txt)  # pass hint to set a proper background color
                # Current row now is 6 rows lower than the current year's time table header
                currentRow -= 4  # set it back to first time slot (2 rows lower than the header row)
            currentRow += 45  # set the current row 45 + 2 = 47 rows lower than the header, to start a new time table for the next year

    def SetConstants(self):
        global nCourses, nLabs, nSubgroups,  tCourse, year3SubgroupRange, year2SubgroupRange, year1SubgroupRange 
        global SubgroupRange, tLab, cNames1, cNames2, cNames3, labNames1, labNames2, labNames3, tNames

        if self.semester1:
            import UVT_Computer_Science_Semester1 as uvt
        else:
            import UVT_Computer_Science_Semester2 as uvt
        nCourses = [len(uvt.nCourseSlotsYear1), len(uvt.nCourseSlotsYear2), len(uvt.nCourseSlotsYear3)]
        nLabs = [len(uvt.nLabSlotsYear1), len(uvt.nLabSlotsYear2), len(uvt.nLabSlotsYear3)]
        year3SubgroupRange = range(years + uvt.nSubgroups[year1] + uvt.nSubgroups[year2],
                             years + uvt.nSubgroups[year1] + uvt.nSubgroups[year2] + uvt.nSubgroups[year3])
        year2SubgroupRange = range(years + uvt.nSubgroups[year1], year3SubgroupRange[0])
        year1SubgroupRange = range(years, year2SubgroupRange[0])
        SubgroupRange = [year1SubgroupRange, year2SubgroupRange, year3SubgroupRange]
        nSubgroups = uvt.nSubgroups
        tCourse = uvt.tCourse
        tLab = uvt.tLab
        cNames1 = uvt.cNames1
        cNames2 = uvt.cNames2
        cNames3 = uvt.cNames3
        labNames1 = uvt.labNames1
        labNames2 = uvt.labNames2
        labNames3 = uvt.labNames3
        tNames = uvt.tNames
