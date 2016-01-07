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
##
## ! Boy/girl session
## ! Selective names loading
##
## X Back action
## X Back action wrap-around
##
## ! Skip completed new names
##
## - Loop instead of exiting for invalid user/etc.
## - Add .upper/.lower support for robust user/session detection
## - Add '1' or '2' option for user select, etc.
##
## - UX
##
## - No settings found
## - Complete database scenario
## - Incomplete database scenario
##
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

dataFile = 'data.txt'   #saved settings**
numNames = 600              #per gender**

users = ['Austin', 'Emily']
names = ['Emma', 'Olivia', 'Sophia', 'Isabella', 'Ava', 'Noah', 'Liam', 'Mason', 'Jacob', 'William']
ratings = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
userIndex = -1


#################################  FUNCTIONS  ##################################

  
#######################################
##
##  User select
##

def selectUser():

    global users; global userIndex;
    
    print('Please select a user: ' + users[0] + ' or ' + users[1] + '?')
    selectedUser = sys.stdin.readline().split('\n')[0]
    
    if selectedUser == users[0]:
        userIndex = 0
        print('\nHi, ' + users[userIndex] + '!')
    elif selectedUser == users[1]:
        userIndex = 1
        print('\nHi, ' + users[userIndex] + '!')
    else:
        print('\nInvalid user.')
        sys.exit()
        


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

    global names; global ratings;

    resetData()    
    with open(namesFile, 'r') as file_:
        for line in file_:
            if ',F,' in line: 
                names.append(line.split(',')[0])
                ratings[0].append('0')
                ratings[1].append('0')
                if len(names) >= numNames: break
        
        for line in file_:
            if ',M,' in line: 
                names.append(line.split(',')[0])
                ratings[0].append('0')
                ratings[1].append('0')
                if len(names) >= numNames*2: break

            
#######################################
##
##  Reset data
##
        
def resetData():

    global names; global ratings;

    names = []
    ratings = [[],[]]


#######################################
##
##  Load data
##
    
def loadData():

    global users; global names; global ratings; global dataFile;

    resetData()    
    with open(dataFile, 'r') as file_:
        users[0] = file_.readline().split('\n')[0]
        users[1] = file_.readline().split('\n')[0]
        for line in file_:
            linesplit = line.split('\n')[0].split(',')
            names.append(linesplit[0])
            ratings[0].append(linesplit[1])
            ratings[1].append(linesplit[2])

            
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


