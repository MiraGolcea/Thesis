import UVT_Computer_Science_Settings as set
from z3 import *
import time


# Constants
year1 = 0
year2 = 1
year3 = 2
years = 3
nSlots = 40
week = [[i for i in range(8*j, 8*(j+1))] for j in range(5)]



class TTsolver:

   def __init__(self, callback, semester1=True, optimize=False):
      self.callback = callback 
      self.semester1 = semester1
      self.optimize = optimize
      self.timetable = None
      self.SetConstants()

   def Check(self):
      s = Optimize() if self.optimize else Solver()
      start = time.time()

      # Time table integer function: tt(class, course, timeslot)
      tt = Function('tt', IntSort(), IntSort(), IntSort(), IntSort())
      # tt will return 0, or 1, for any argument
      # for courses
      for i in range(years):  # for any class (year)
         for j in range(nCourses[i]):  # for any course taught in year 'i'
              for k in range(nSlots):  # for any time slot
                  s.add(Or(tt(i, j, k) == 0, tt(i, j, k) == 1))
      # for laboratories
      for y in range(years):  # for each year of study
          for sg in SubgroupRange[y]:  # for any subgroup in year 'y'
              for j in range(nLabs[y]):  # for any lab taught in year 'y'
                  for k in range(nSlots):  # for any time slot
                      s.add(Or(tt(sg, j, k) == 0, tt(sg, j, k) == 1))

      # Number of lectures scheduled per week for each course in each year should match curriculum
      for i in range(years):  # for each year of study
         for j in range(nCourses[i]):  # for each course tought to year 'i'
            s.add(Sum([tt(i, j, k) for k in range(nSlots)]) == nCourseSlots[i][j])
      
      # At most one lecture per time slot for each class (year of study)
      for i in range(years):  # for each class
         for k in range(nSlots):  # for each time slot
            s.add(Sum([tt(i, j, k) for j in range(nCourses[i])]) <= 1)  # sum of elements of list less, or equal 1

      # If a course is scheduled for a certain time slot, the corresponding teacher must be available
      for i in range(years):  # for each class
         for j in range(nCourses[i]):  # for each course
            for k in range(nSlots):  # for each time slot
               s.add(Implies(tt(i, j, k) == 1, A[tCourse[i][j]][k] == 1))

      # No teacher teaches more than one lecture in a time slot. If a teacher lectures a course, cannot teach any lab in the same
      # slot. A teacher cannot teach labs to more than one year of study in a time slot.
      # Many constraints in a single place to run in the same loop for better performance (avoid repeating the same loops)
      # Using list comprehension, we create lists and count how many courses and labs (for each year of study) a teacher is
      # teaching in a timeslot. Then we define the constraint that there can be either 1 course and 0 labs, or 0 course and possibly
      # more labs (for more subgroupes belonging to the same year)
      # Note that we are checking only if the labs are taught to subgroups of the same year, but not weather the labs are of the same
      # kind. This could violate the principle that a teacher cannot teach different kind of labs in a time slot.
      # We define below a constraint to address this issue
      for T in range(nTeachers):  # check each teacher
         for k in range(nSlots):  # check each time slot
            # Count how many courses and labs teacher 'T' is teaching in a given time slot
            n_courses = Sum([tt(i, j, k) for i in range(years) for j in range(nCourses[i]) if tCourse[i][j] == T])
            s.add(n_courses <= 1)  # no more than one course in a time slot
            n_labs1 = Sum([tt(sg, j, k) for sg in year1SubgroupRange for j in range(nLabs[year1]) if tLab[year1][j] == T])
            n_labs2 = Sum([tt(sg, j, k) for sg in year2SubgroupRange for j in range(nLabs[year2]) if tLab[year2][j] == T])
            n_labs3 = Sum([tt(sg, j, k) for sg in year3SubgroupRange for j in range(nLabs[year3]) if tLab[year3][j] == T])
            s.add(Implies(n_courses == 1, n_labs1 + n_labs2 + n_labs3 == 0))  # if there is a course, no labs allowed
            s.add(Implies(n_labs1 > 0, n_labs2 + n_labs3 == 0))  # A teacher teaches lab to only one year of study in a time slot
            s.add(Implies(n_labs2 > 0, n_labs1 + n_labs3 == 0))  # A teacher teaches lab to only one year of study in a time slot
            s.add(Implies(n_labs3 > 0, n_labs1 + n_labs2 == 0))  # A teacher teaches lab to only one year of study in a time slot

      # No teacher teaches different labs in a time slot and no teacher teaches the same lab to more than 'const0' (=3) subgroups 
      for T in range(nTeachers):  # check each teacher
         for k in range(nSlots):  # check each time slot
            for y in range(years):
               # Count all labs teacher 'T' is teaching in a given time slot
               n_labs = Sum([tt(sg, j, k) for sg in SubgroupRange[y] for j in range(nLabs[y]) if tLab[y][j] == T])
               s.add(n_labs <= set.const0) # no more than 3 labs (and should be of the same kind, checked below )
               # Count how many different labs teacher 'T' is teaching in this time slot
               for j in range(nLabs[y]): # check different labs
                  lab = Sum([tt(sg, j, k) for sg in SubgroupRange[y] if tLab[y][j] == T]) # number of labs of the same kind 'j'
                  s.add(Implies(n_labs > 1, Or(lab == 0, lab == n_labs))) # all labs must be of the same kind     

      # In the 3rd year of study in the 2nd semester, all courses are scheduled in the first 'const1' (=3) days of the week
      if not self.semester1:
         s.add(Sum([tt(year3, j, k) for j in range(nCourses[year3]) for k in range(8*set.const1, nSlots)]) == 0)

      # The cross-curriculum course is scheduled on Wednesday and Thursday in the following time slots:  from 16:20 until 19:30,
      # for students in the second year of study in both semesters and for students in the third year of study only in the first
      # semester and for students in the first year of study only in the second semester (const2 = [21, 22], const3 = [29, 30])

      # Constraints for 1st year students. Only for semester 2
      if not self.semester1: 
         s.add(Sum([tt(year1, crossCurriculum1, k) for k in set.const2]) == 1)  # one course on Wednesday
         s.add(Sum([tt(year1, crossCurriculum1, k) for k in set.const3]) == 1)   # one course on Thursday

      # Constraints for 2nd year students:
      s.add(Sum([tt(year2, crossCurriculum2, k) for k in set.const2]) == 1)     # one course on Wednesday
      s.add(Sum([tt(year2, crossCurriculum2, k) for k in set.const3]) == 1)      # one course on Thursday

      # Constraints for 3rd year students. Only for semester 1
      if self.semester1:
         s.add(Sum([tt(year3, crossCurriculum3, k) for k in set.const2]) == 1)  # one course on Wednesday
         s.add(Sum([tt(year3, crossCurriculum3, k) for k in set.const3]) == 1)   # one course on Thursday

      # The English language course (for year of study 1 and 2) is scheduled only after 16:20 (const4)
      custom_range = set.const4
      if "english1" in globals():  # if "english1" constant was set ("English" is in year 1 curriculum)
         s.add(Sum([tt(year1, english1, k) for k in custom_range]) == 0)  # no english course in these time slots for year 1 students
      if "english2" in globals():  # if "english2" constant was set ("English" is in year 2 curriculum)
         s.add(Sum([tt(year2, english2, k) for k in custom_range]) == 0)  # no english course in these time slots for year 2 students

      # The maximum number of slots allocated for teaching for a teacher in a day is const5 (=5)
      for T in range(nTeachers):  # check each teacher
         for day in week:  # check each day
            # Count how many courses and labs teacher 'T' is teaching in a given day
            n_courses = Sum([1 for i in range(years) for j in range(nCourses[i]) for k in day if tt(i, j, k) == 1 if tCourse[i][j] == T])
            n_labs1 = Sum([1 for sg in year1SubgroupRange for j in range(nLabs[year1]) for k in day if tt(sg, j, k) == 1 if tLab[year1][j] == T])
            n_labs2 = Sum([1 for sg in year2SubgroupRange for j in range(nLabs[year2]) for k in day if tt(sg, j, k) == 1 if tLab[year2][j] == T])
            n_labs3 = Sum([1 for sg in year3SubgroupRange for j in range(nLabs[year3]) for k in day if tt(sg, j, k) == 1 if tLab[year3][j] == T])
            s.add(n_courses + n_labs1 + n_labs2 + n_labs3 <= set.const5)

      # The maximum number of slots a student (class) can learn for is const6 (=5) a day
      for day in week:
         for y in range(years):
            for sg in SubgroupRange[y]:
               n_courses = Sum([tt(y,j,k) for j in range(nCourses[y]) for k in day])
               n_labs = Sum([tt(sg,j,k) for j in range(nLabs[y]) for k in day])
               s.add(n_courses + n_labs <= set.const6) 

      # Number of teachings scheduled per week for each lab in each year for each subgroup should match curriculum
      for y in range(years):
         for sg in SubgroupRange[y]:  # for each subgroup
            for j in range(nLabs[y]):  # for each laboratory in year 'y'
               s.add(Sum([tt(sg, j, k) for k in range(nSlots)]) == nLabSlots[y][j])  # scheduled labs should match curriculum

      # No laboratory for any subgroup in a year should be scheduled if a course is scheduled in that time slot for the respective year
      for y in range(years):
         for j in range(nCourses[y]):  # for each course in the respective year
            for k in range(nSlots):  # check each time slot
               s.add(Implies(tt(y, j, k) == 1, Sum([tt(sg, l, k) for sg in SubgroupRange[y] for l in range(nLabs[y])]) == 0))

      # At most one laboratory per time slot for any subgroup of any year of study
      for y in range(years):
         for sg in SubgroupRange[y]:  # for each subgroup of year 'y'
            for k in range(nSlots):  # for each time slot
               s.add(Sum([tt(sg, j, k) for j in range(nLabs[y])]) <= 1)  # sum of elements of list less, or equal 1

      # If a laboratory is scheduled for a certain time slot, the corresponding teacher must be available
      for y in range(years):
         for sg in SubgroupRange[y]:
            for j in range(nLabs[y]):  # for each lab of year 'y'
               for k in range(nSlots):  # for each time slot
                  s.add(Implies(tt(sg, j, k) == 1, A[tLab[y][j]][k] == 1))

      # In the 3rd year of study in the 2nd semester, all labs are scheduled in the first const1 (=3) days of the week for all subgroups
      if not self.semester1:
         for sg in year3SubgroupRange:  # for each subgroup of year 3
            s.add(Sum([tt(sg, j, k) for j in range(nLabs[year3]) for k in range(8*set.const1, nSlots)]) == 0)  # no labs Thursday, or Wednesday

      # The English language lab (for year of study 1 and 2) is scheduled only after 16:20 (const4)
      custom_range = set.const4
      if "english1_lab" in globals():  # if "english1_lab" constant was set ("English" lab is in year 1 curriculum)
         s.add(Sum([tt(sg, english1_lab, k) for sg in year1SubgroupRange for k in custom_range]) == 0)  # no english1 labs in these time slots
      if "english2_lab" in globals():  # if "english2_lab" constant was set ("English" lab is in year 2 curriculum)
         s.add(Sum([tt(sg, english2_lab, k) for sg in year2SubgroupRange for k in custom_range]) == 0)  # no english2 labs in these time slots
      
      # The timetable should not contain inbetween free slots
      """
      gaps = 0
      for y in range(years):
         for sg in SubgroupRange[y]:
            col = [Sum([tt(y,c,k) for c in range(nCourses[y])]) + Sum([tt(sg,l,k) for l in range(nLabs[y])])  for k in range(nSlots)]
            gaps += sum([(col[i+1] - col[i])*(col[i+1] - col[i]) for h in range(5) for i in range(8*h, 8*h + 7)])
      Gaps = Int('Gaps')
      s.add(Gaps == gaps)
      #s.add(Gaps < 315)
      """
      
      if self.optimize:
         
         # Optimize for lecturers' timeslot preferences
         n_courses = 0
         n_labs = 0
         for T in tPref:
            for y in range(years):
               for k in range(nSlots):
                  n_courses += Sum([tt(y, j, k) for j in range(nCourses[y]) if tCourse[y][j] == T if P[T][k] == 0])
                  n_labs += Sum([tt(sg, j, k) for sg in SubgroupRange[y] for j in range(nLabs[y]) if tLab[y][j] == T if P[T][k] == 0])
         Penalty = Int('Penalty')         
         s.add(Penalty == n_courses + n_labs)
         s.minimize(Penalty)
         
      
      result = s.check()
      end = time.time()
      print('elapsed time: ', (end - start) / 60)
      if result == sat:
         model = s.model()
         self.timetable = [[[model.evaluate(tt(i, j, k)) for k in range(nSlots)] for j in self.GetRange(i)] for i in range(years + sum(nSubgroups))]
         if self.optimize:
            print("Penalty: ", model.evaluate(Penalty))
         #print("Gaps: ", model.evaluate(Gaps))
         self.callback(self.timetable)  # Pass the timetable to the caller
         return True
      else:
         print(result)
         self.callback([])  # Pass an empty timetable to the caller
         return False

   def GetTimeTable(self):
      return self.timetable

   def GetRange(self, cls):
      if cls in range(years):
         return range(nCourses[cls])
      if cls in year1SubgroupRange:
         return range(nLabs[year1])
      if cls in year2SubgroupRange:
         return range(nLabs[year2])
      if cls in year3SubgroupRange:
         return range(nLabs[year3])

   def SetConstants(self):
      global nTeachers, nCourses, nLabs, nSubgroups, nCourseSlots, nLabSlots, tCourse, year3SubgroupRange
      global year2SubgroupRange, year1SubgroupRange, SubgroupRange, tLab, A, P, tPref, crossCurriculum1
      global crossCurriculum2, crossCurriculum3, english1, english2, english1_lab, english2_lab

      if self.semester1:
         import UVT_Computer_Science_Semester1 as uvt
         import UVT_Computer_Science_Availability1 as ava
      else:
         import UVT_Computer_Science_Semester2 as uvt
         import UVT_Computer_Science_Availability2 as ava
      nTeachers = len(uvt.tNames)
      nCourses = [len(uvt.nCourseSlotsYear1), len(uvt.nCourseSlotsYear2), len(uvt.nCourseSlotsYear3)]
      nLabs = [len(uvt.nLabSlotsYear1), len(uvt.nLabSlotsYear2), len(uvt.nLabSlotsYear3)]
      nCourseSlots = [uvt.nCourseSlotsYear1, uvt.nCourseSlotsYear2, uvt.nCourseSlotsYear3]
      nLabSlots = [uvt.nLabSlotsYear1, uvt.nLabSlotsYear2, uvt.nLabSlotsYear3]
      year3SubgroupRange = range(years + uvt.nSubgroups[year1] + uvt.nSubgroups[year2],
          years + uvt.nSubgroups[year1] + uvt.nSubgroups[year2] + uvt.nSubgroups[year3])
      year2SubgroupRange = range(years + uvt.nSubgroups[year1], year3SubgroupRange[0])
      year1SubgroupRange = range(years, year2SubgroupRange[0])
      SubgroupRange = [year1SubgroupRange, year2SubgroupRange, year3SubgroupRange]
      nSubgroups = uvt.nSubgroups
      tCourse = uvt.tCourse
      tLab = uvt.tLab
      A = ava.A
      P = ava.P
      tPref = ava.tPref
      if set.const7 in uvt.cNames1:
         crossCurriculum1 = uvt.cNames1.index(set.const7)
      if set.const7 in uvt.cNames2:
         crossCurriculum2 = uvt.cNames2.index(set.const7)
      if set.const7 in uvt.cNames3:
         crossCurriculum3 = uvt.cNames3.index(set.const7)
      if set.const8 in uvt.cNames1:
         english1 = uvt.cNames1.index(set.const8)
      if set.const8 in uvt.cNames2:
         english2 = uvt.cNames2.index(set.const8)
      if set.const8 in uvt.labNames1:
         english1_lab = uvt.labNames1.index(set.const8)
      if set.const8 in uvt.labNames2:
         english2_lab = uvt.labNames2.index(set.const8)