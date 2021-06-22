# Second semester lecturers' names
Lecturer_Names = ["Assis. Spataru A.", "Conf Dr. Kaslik E.", "Conf Dr. Pop D.", "Lect Dr. Erascu M.", "Conf Dr. Mindruta C.", "Prof Dr. Istrate G.", "Conf Dr. Marin M.", "Assis Dr. Coroban L.", "Lect Dr. Muresan R.", "Lect Dr. Mafteiu-Scai L.", "Lect Dr. Pungila C.", "Lect Dr. Popa Andreescu H.", "Ing. Ciocan F.", "Lect Dr. Mihalas S.", "Assis Dr. Brandibur O.", "Ing. Stoichescu F.", "Lect Dr. Iuhasz G.", "Lect Dr. Gaianu M.", "Lect Dr. Ivan O.", "Lect Dr. Miculescu A.", "", "Conf Dr. Craciun A.", "Lect Dr. Sancira M.", "Inf Drd. Stinga O."]

# All University staff is initially set as available at any timeslot
A = [[1 for i in range(40)] for j in range(len(Lecturer_Names))]  # Availability initialized to 1 for all

# Set a particular lecturer's unavailability. The first index is the index in the Lecturer_Names list, the second index is 
# the time slot when he/she is unavailable. Time slots run from 0 to 39 (ex: 9 is the second time slot on Tuesday)

# University Senate members are unavailable Thursday first two time slots
# A[senator_index][24] = A[senator_index][25] = 0



# Time slot preferences initialized to "preferred" for all slots for all lecturers
P = [[1 for i in range(40)] for j in range(len(Lecturer_Names))]  # Preference initialized to "preferred" for all slots

# List with lecturers having preferences
tPref = [5, 9, 12, 16, 22]

# Individual preferences
P[5][0] = P[5][8] = P[5][16] = P[5][24] = P[5][32] = 0        # lecturer 5 (Istrate G) prefers not to teach in the first slot of the day
P[16][0] = P[16][8] = P[16][16] = P[16][24] = P[16][32] = 0   # lecturer 16 (Iuhasz G) prefers not to teach in the first slot of the day
for slot in range(24, 40):
   P[22][slot] = 0                                            # lecturer 22 (Sancira M) prefers to teach in the first 3 days of the week
for slot in range(0, 16):
   P[9][slot] = 0                                             # lecturer 9 (Mafteiu-Scai L) prefers to teach in the last 3 days of the week
P[12] = [0 for i in range(40)]
for i in [0,7,8,15,16,23,24,31,32,39]:                        # extern 12 (Ciocan F) prefers first, or last slot of a day
   P[12][i] = 1