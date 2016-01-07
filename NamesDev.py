## * Code for yourself first! *
##
## X Save to settings file
## X Read from settings file
## X Rating
## X Get names (up to 1000)
## X '+/-' copy
## \ Controls
##   X Quit session
##   X Save session
##   ! Go back
##   X Skip
##   X Favorite
##
## ! Guy/girl session
## - UX
##
## - No settings found
## - Complete database scenario
## - Incomplete database scenario
##
##
##Settings
##order: popularity/random
##reset
##autsave


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
status = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
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

    global names; global status; global userIndex;

    print('\n  +: like  -: dislike  *: favorite  b: back  q: quit')



    for index, name in enumerate(names):
    #nextName() #BOOKMARK BOOKMARK BOOKMARK BOOKMARK
        
        print('\n'+name)
        inChar = sys.stdin.readline()[0]
        if inChar == '+':
            status[userIndex][index] = inChar
        elif inChar == '-':
            status[userIndex][index] = inChar
        elif inChar == '*':
            status[userIndex][index] = inChar
        elif inChar == '0':
            status[userIndex][index] = '0'
        elif inChar == 'q': break
        elif inChar == 's':
            saveData()
            print('Data saved.')
        elif inChar == 'b':
            print('Back it up.')
            #nextName(repeat)
            #nextName(repeat)
        else:
            print('Invalid input.')
            #REPEAT
            



#######################################
##
## 
##
        
def nextName():

    #global names; global status; global userIndex;

    print('\n  +: like  -: dislike  *: favorite  b: back  q: quit')   



#Skip done names
#Take desired order into account


#######################################
##
##  Load names
##
    
def loadNames(namesFile):

    global names; global status;

    resetData()    
    with open(namesFile, 'r') as file_:
        for line in file_:
            if ',F,' in line: 
                names.append(line.split(',')[0])
                status[0].append('0')
                status[1].append('0')
                if len(names) >= numNames: break
        
        for line in file_:
            if ',M,' in line: 
                names.append(line.split(',')[0])
                status[0].append('0')
                status[1].append('0')
                if len(names) >= numNames*2: break
    

            
#######################################
##
##  Reset data
##
        
def resetData():

    global names; global status;

    names = []
    status = [[],[]]


#######################################
##
##  Load data
##
    
def loadData():

    global users; global names; global status; global dataFile;

    resetData()    
    with open(dataFile, 'r') as file_:
        users[0] = file_.readline().split('\n')[0]
        users[1] = file_.readline().split('\n')[0]
        for line in file_:
            linesplit = line.split('\n')[0].split(',')
            names.append(linesplit[0])
            status[0].append(linesplit[1])
            status[1].append(linesplit[2])

            
#######################################
##
## Save data
##
            
def saveData():

    global users; global names; global status; global dataFile;

    with open(dataFile, 'w') as file_:
        file_.write(users[0]+'\n')
        file_.write(users[1]+'\n')
        for index, name in enumerate(names):
            file_.write(name+','+status[0][index]+','+status[1][index]+'\n')          




####################################  MAIN  ####################################


loadData()
loadNames('2013.txt')

selectUser()
startSession()
saveData()


