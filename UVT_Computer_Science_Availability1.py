# First semester lecturers' names
Lecturer_Names = ["Lect Dr. Chis M.", "Lect Dr. Micota F.", "Prof Dr. Istrate G.", "Conf Dr. Craciun A.", "Lect Dr. Cira C.", "Assist Dr. Vulpe A.", "Conf Dr. Pop D.", "Lect Dr. Ivan O.", "Inf Drd. Stinga O.", "Drd. Galis D.", "Lect Dr. Dramnesc I.", "Dr. Horhat R.", "Lect Dr. Pungila C.", "Lect Dr. Popa Andreescu H.", "Dr. Copie A.", "Conf Dr. Kaslik E.", "Ing. Birdac L.", "Lect Dr. Erascu M.", "Lect Dr. Iuhasz G.", "Ing. Munteanu A.", "", "Conf Dr. Marin M.", "Lect Dr. Bonchis C.", "Lect Dr. Neagul M."]

# All University staff is initially set as available at any timeslot
A = [[1 for i in range(40)] for j in range(len(Lecturer_Names))]  # Availability initialized to "available" for all slots

# Set a particular lecturer's unavailability. The first index is the index in the Lecturer_Names list, the second index is 
# the time slot when he/she is unavailable. Time slots run from 0 to 39 (ex: 9 is the second time slot on Tuesday)

# University Senate members are unavailable Thursday first two time slots
# A[1][24] = A[1][25] = 0



# Time slot preferences initialized to "preferred" for all slots for all lecturers
P = [[1 for i in range(40)] for j in range(len(Lecturer_Names))]  # Preference initialized to "preferred" for all slots

# List with lecturers having preferences
tPref = [2, 3, 16, 18, 19]

# Individual preferences
P[2][0] = P[2][8] = P[2][16] = P[2][24] = P[2][32] = 0        # lecturer 2 (Istrate G) prefers not to teach in the first slot of the day
P[3][0] = P[3][8] = P[3][16] = P[3][24] = P[3][32] = 0        # lecturer 3 (Craciun A) prefers not to teach in the first slot of the day
P[18][0] = P[18][8] = P[18][16] = P[18][24] = P[18][32] = 0   # lecturer 18 (Iuhasz G) prefers not to teach in the first slot of the day
P[16] = [0 for i in range(40)]
for i in [0,7,8,15,16,23,24,31,32,39]:                        # extern 16 (Birdac L) prefers first, or last slot of a day
   P[16][i] = 1
P[19] = [0 for i in range(40)]
for i in [0,7,8,15,16,23,24,31,32,39]:                        # extern 19 (Muntean A) prefers first, or last slot of a day
   P[19][i] = 1