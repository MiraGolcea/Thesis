# Max. number of subgroups learning a lab together in a time slot, taught by the single teacher
const0 = 3

# Number of days at the beginning of the week in the second semester when all courses and labs 
# are scheduled for year3 students
const1 = 3

# The cross-curriculum course is scheduled on Wednesday or Thursday in the following time slots:
# from 16:20 until 19:30. The list below holds the time slots when the cross-curriculum course 
# must be scheduled
const2 = [21, 22]      # Wednesday from 16:20 until 19:30
const3 = [29, 30]      # Thursday from 16:20 until 19:30

# The English language course, or lab (for year of study 1 and 2) is scheduled only after 16:20. 
# The list below contains the time slots when the English course (lab) cannot be scheduled
const4 = [0, 1, 2, 3, 4, 
          8, 9, 10, 11, 12, 
         16, 17, 18, 19, 20, 
         24, 25, 26, 27, 28, 
         32, 33, 34, 35, 36]

# The maximum number of slots allocated for teaching for a teacher in a day is 5
const5 = 5

# The maximum number of slots a student (class) can learn for in a day is 5
const6 = 5

# The name of the cross-curriculum course as it appears in the cNames list
const7 = "CrossCurriculum"

# The name of the English language course/lab as it appears in the cNames/labNames lists
const8 = "English"

