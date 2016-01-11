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
## X Skip completed new names
## X Complete ratings scenario: all boys or all girls finished
## X Change 'Session complete!' copy
## N Change order of controls (not needed for eventual GUI)
##
## X Loop instead of exiting for invalid user/etc.
## X Add .upper/.lower support for robust user/session detection
## X Add '1' or '2' option for user select, etc.
## X '\n' entry error
##
##
## \ UX: Plan out functionality and menu hierarchy
##   X Main menu: begin session, view results, reset
##   X View results (e.g. liked names)
##   ! No settings found upon loading
##   \ Selective names loading: only upon 1st run
##   \ New users: only upon 1st run
##   \ reset all (users, names, ratings)
##
## W Settings
##   N order: popularity/random
##   W autosave y/n
##   N skip completed names y/n
##


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
## Main Menu
##
## Start Session
## View Results
## Switch User
## Reset All
## Quit
##
        
def menu():

    global userIndex

    # Loop until completion or the user chooses to quit
    while True:   

        # Show user controls and accept input from the user
        print('\n  s: start  v: view results  u: switch user  r: reset  q: quit\n')
        inChar = sys.stdin.readline()[0]
        
        # Start a rating session
        if inChar.lower() == 's':            

            # Begin a new session
            session()

            # Save user data to file
            saveData()

        # View results
        elif inChar.lower() == 'v':                    
            viewResults()

        # Switch user ##TODO
        elif inChar.lower() == 'u':
            userIndex = abs(userIndex-1)
            print('\nHi, ' + users[userIndex] + '!')
            pass
        
        # Reset data ##TODO
        elif inChar.lower() == 'r':

            while True:   
                print('\nAre you sure you want to reset? All data will be lost.')
                resetChar = sys.stdin.readline()[0]

                if resetChar.lower() == 'y':            
                    newData()                    
                            
                else:
                    break

        # Quit
        elif inChar.lower() == 'q':            
            return
        
        # Invalid input
        else:
            print('\nInvalid input.')


#######################################
##
##  User select
##

def selectUser():

    global users; global userIndex;

    userIndex = -1;
    while userIndex < 0:            
        print('\nPlease select a user: ' + users[0] + ' or ' + users[1] + '?')
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
## Rating session
##
        
def session():

    global names; global ratings; global userIndex;

    # Initialize variables    
    newEntries = [[],[]]    #stores data for this session: nameIndex, rating
    entryIndex = 0;         #points to the current new entry being worked on

    nextName = 0;           ###for picking upcoming names [TODO]
    
    # Select a session type
    sessionType = -1;
    while sessionType < 0:            
        print('\nPlease select a session type: boys or girls?')
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

    # Loop until completion or the user chooses to quit
    while True:   
        
        # Add to the list of new entries if needed
        if entryIndex >=  len(newEntries[0]):    

            while True:
                
                # Check for completion
                if sessionType == 0 and nextName >= numNames or \
                   sessionType == 1 and nextName >= numNames*2:
                    if sessionType == 0:
                        print('\nAll girl names have been completed!')
                    else:
                        print('\nAll boy names have been completed!')
                    for index in range(len(newEntries[0])):
                        ratings[userIndex][newEntries[0][index]] = newEntries[1][index]
                    saveData()
                    return
                if ratings[userIndex][nextName] != '0':
                    nextName += 1
                else:
                    break
            
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
        elif inChar.lower() == 'q':
            for index in range(len(newEntries[0])-1):
                ratings[userIndex][newEntries[0][index]] = newEntries[1][index]
            saveData()
            return

        # Save data
        elif inChar.lower() == 's':                    
            for index in range(len(newEntries[0])-1):
                ratings[userIndex][newEntries[0][index]] = newEntries[1][index]
            saveData()
            print('\nData saved.')

        # Back
        elif inChar.lower() == 'b':     
            entryIndex -= 1

            # Check for wrap-around
            if entryIndex < 0:
                entryIndex = 0

        # Invalid input
        else:
            print('\nInvalid input.')


#######################################
##
##  View results
##
    
def viewResults():

    global users; global names; global ratings;

    both = []
    fav0 = []
    fav1 = []

    # Find favorites and overlaps

    for index, name in enumerate(names):

        # Find favorites
        if ratings[0][index] == '*':
            fav0.append(name)

        if ratings[1][index] == '*':
            fav1.append(name)

        # Find overlaps
        if ratings[0][index] == '+' and ratings[1][index] == '+' or \
           ratings[0][index] == '*' and ratings[1][index] == '+' or \
           ratings[0][index] == '+' and ratings[1][index] == '*' or \
           ratings[0][index] == '*' and ratings[1][index] == '*':
            both.append(name)        

    # Display findings
    if len(both) >0:
        print('\nNames liked by both ' + users[0] + ' and ' + users[1] + ':')
        for index, name in enumerate(both):
            print(name)
    else:
        print('No names liked by both users yet!')
    
    if len(fav0) > 0:
        print('\nNames favorited by ' + users[0] + ':')
        for index, name in enumerate(fav0):
            print(name)

    if len(fav1) > 0:
        print('\nNames favorited by ' + users[1] + ':')
        for index, name in enumerate(fav1):
            print(name)


#######################################
##
##  New data
##
    
def newData():

    global users; global names; global ratings; global userIndex; global numNames

    #Reset
    users = []
    names = []
    ratings = [[],[]]
    userIndex = 0

                    
    # User information
    print('\nWelcome! What is your name?')
    users.append(sys.stdin.readline().split('\n')[0])
    
    print('\nWhat is your partner\'s name?')
    users.append(sys.stdin.readline().split('\n')[0])

    # Load names
    print('\nWhich file has the list of names you\'d like to use?')
    namesfile = sys.stdin.readline().split('\n')[0]
    ###loadNames('2013.txt') BOOKMARK BOOKMARK BOOKMARK BOOKMARK

    # try entering


    #save data
    saveData()


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
    try:
        with open(dataFile, 'r') as file_:
            users.append(file_.readline().split('\n')[0])
            users.append(file_.readline().split('\n')[0])
            for line in file_:
                linesplit = line.split('\n')[0].split(',')
                names.append(linesplit[0])
                ratings[0].append(linesplit[1])
                ratings[1].append(linesplit[2])

        numNames = len(ratings[0])/2
    except:
        print('FILE ERROR')                 ####BOOKMARK BOOKMARK HOW TO TRY CATCH
            
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

###ERROR CATCH AND THROW BACK TO NEW DATA


selectUser()

menu()






