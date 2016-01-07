## * Code for yourself first! *
##
## X Save to settings file
## X Read from settings file
## X Rating
## X Get names (up to 1000)
## X '+/-' copy
## X Controls
##   X Quit session
##   X Save session
##   X Go back
##   X Skip
##   X Favorite
## X Back action
## X Back action wrap-around
##
## X Boy/girl session
## ! Skip completed new names
##
## X '\n' entry error
##
## - Loop instead of exiting for invalid user/etc.
## - Add .upper/.lower support for robust user/session detection
## - Add '1' or '2' option for user select, etc.
##
## - ## - Selective names loading
##
## - No settings found
## - Complete database scenario: all boys or all girls finished
## - Incomplete database scenario
##
## - UX
## - New users
##
##Settings
##order: popularity/random
##reset
##autosave y/n
##skip completed names y/n 


import sys


################################################################################
##
##  Declarations/Initializations
##
##  User-customizable settings/variables are denoted by **
##

dataFile = 'data.txt'   #saved settings **
numLoadNames = 600      #when pulling from 'yob' files (per gender) **
numNames = 0            #actual (per gender) **

users = []
names = []
ratings = [[],[]]
userIndex = -1


#################################  FUNCTIONS  ##################################

  
#######################################
##
##  User select
##

def selectUser():

    global users; global userIndex;

    userIndex = -1;
    while userIndex < 0:            
        print('Please select a user: ' + users[0] + ' or ' + users[1] + '?')
        selectedUser = sys.stdin.readline().split('\n')[0]
        if selectedUser == users[0] or selectedUser == users[0].lower() or \
           selectedUser == users[0].upper() or selectedUser == '1':
            userIndex = 0
            print('\nHi, ' + users[userIndex] + '!')
            break
        elif selectedUser == users[1] or selectedUser == users[1].lower() or \
             selectedUser == users[1].upper() or selectedUser == '2':
            userIndex = 1        
            print('\nHi, ' + users[userIndex] + '!')
            break
        else:
            print('\nInvalid user.')                        


#######################################
##
## Start Session
##
        
def startSession():

    global names; global ratings; global userIndex;

    # Initialize variables    
    newEntries = [[],[]]    #stores data for this session: nameIndex, rating
    entryIndex = 0;         #points to the current new entry being worked on

    nextName = 0;           ###for picking upcoming names [TODO]
    
    # Select a session type
    sessionType = -1;
    while sessionType < 0:            
        print('Please select a session type: boys or girls?')
        selectedType = sys.stdin.readline().split('\n')[0]
        if selectedType == 'Boys' or selectedType == 'boys' or \
           selectedType == 'BOYS' or selectedType == '1':
            sessionType = 1
            nextName = numNames
            break
        elif selectedType == 'Girls' or selectedType == 'girls' or \
             selectedType == 'GIRLS' or selectedType == '2':
            sessionType = 0
            nextName = 0
            break
        else:            
            print('\nInvalid type.')  

    # Show user controls
    print('\n  +: like  -: dislike  *: favorite  b: back  q: quit')

    # Loop until the user chooses to quit
    while True:
        
        # Add to the list of new entries if needed
        if entryIndex >=  len(newEntries[0]):    

            ###Skip done names [TODO]

            # Add the nameIndex and rating
            newEntries[0].append(nextName)            
            newEntries[1].append(ratings[userIndex][entryIndex])
        
            # Select the next name
            nextName += 1

            #Take desired order into account [TODO]

        # Display the name to rate and accept input from the user
        print('\n'+names[newEntries[0][entryIndex]])
        inChar = sys.stdin.readline()[0]

        # Store valid user ratings and move on
        if inChar == '+' or inChar == '-' or inChar == '*' or inChar == '0':
            newEntries[1][entryIndex] = inChar    
            entryIndex += 1

        # Quit (but save data first)
        elif inChar == 'q':
            for index in range(len(newEntries[0])-1):
                ratings[userIndex][newEntries[0][index]] = newEntries[1][index]
            saveData()
            break

        # Save data
        elif inChar == 's':                    
            for index in range(len(newEntries[0])-1):
                ratings[userIndex][newEntries[0][index]] = newEntries[1][index]
            saveData()
            print('\nData saved.')

        # Back
        elif inChar == 'b':     
            entryIndex -= 1

            # Check for wrap-around
            if entryIndex < 0:
                entryIndex = 0

        # Invalid input
        else:
            print('\nInvalid input.')


#######################################
##
##  Load names
##
    
def loadNames(namesFile):

    global names; global ratings; global numLoadNames
       
    names = []
    ratings = [[],[]]
    with open(namesFile, 'r') as file_:
        for line in file_:
            if ',F,' in line: 
                names.append(line.split(',')[0])
                ratings[0].append('0')
                ratings[1].append('0')
                if len(names) >= numLoadNames: break
        
        for line in file_:
            if ',M,' in line: 
                names.append(line.split(',')[0])
                ratings[0].append('0')
                ratings[1].append('0')
                if len(names) >= numLoadNames*2: break


#######################################
##
##  Load data
##
    
def loadData():

    global users; global names; global ratings; global dataFile; global numNames

    users = []
    names = []
    ratings = [[],[]]
    userIndex = -1   
    with open(dataFile, 'r') as file_:
        users.append(file_.readline().split('\n')[0])
        users.append(file_.readline().split('\n')[0])
        for line in file_:
            linesplit = line.split('\n')[0].split(',')
            names.append(linesplit[0])
            ratings[0].append(linesplit[1])
            ratings[1].append(linesplit[2])

    numNames = len(ratings[0])/2

            
#######################################
##
## Save data
##
            
def saveData():

    global users; global names; global ratings; global dataFile;

    with open(dataFile, 'w') as file_:
        file_.write(users[0]+'\n')
        file_.write(users[1]+'\n')
        for index, name in enumerate(names):
            file_.write(name+','+ratings[0][index]+','+ratings[1][index]+'\n')          




####################################  MAIN  ####################################

# Load user data from file
loadData()

###loadNames('2013.txt') [TODO]


# Select one of two users
selectUser()

# Begin a new session
startSession()

# Save user data to file
saveData()


