# SQLSEQUEL - A NEW DATABASE LANGUAGE
# THIS SOFTWARE IS BASED LOOSELY OFF OF SQL.
# IT UTILISES A 2D ARRAY CONSISTING OF LISTS WITHIN A LIST.

# I PLAN TO ADD .CSV EXPORT AT A LATER DATE. 
# UPDATE - THIS HAS BEEN REPLACED WITH TXT EXPORTED AND A PARSER.

# INITIALISES 2D ARRAY FOR DATA STORAGE

database = [

    # INDEX ROW TO PREVENT INDEX ERROR
    
    []
    
]

# DEFINES HEADERS OF TABLE, AND HENCE NUMBER OF COLUMNS

def init():

    # UNTIL A FLAG MANUALLY QUITS THE INITIATION, ADD FIELDS.
    
    while True:
        fieldName = ""        
        
        fieldName = input("Enter the field name, IMPORTTABLE to use an existing table, \
or STOP to stop.")

        # STOP ADDING RECORDS, PROCEED TO RUNTIME
        
        if fieldName == "STOP":
            return 0

        # OR WE COULD IMPORT table.txt
        
        if fieldName == "IMPORTTABLE":
            importTable()

        # OTHERWISE, ADD THE FIELD TO THE INDEX ROW
        
        if fieldName != "IMPORTTABLE":
            database[0].append(fieldName)

            # DON'T FORGET TO PAD THE OTHER RECORDS

            for i in range(1, len(database)):
                database[i].append("")

# IMPORT TABLE

def importTable():

    # OPEN THE table.txt FILE
    try:
        global database
        
        f = open("table.txt", "rt")

        database = []
        
        wholeTableString = f.read()
        lineByLine = wholeTableString.splitlines()

        # THIS MAKES A 2D ARRAY FROM THE FILE.
        for i in lineByLine:
            database.append(i.split())

        # MAKE SURE THAT EACH RECORD HAS THE SAME NUMBER OF FIELDS AS THE INDEX ROW

        for i in range(1, len(database)):

            # IF THE ROW IS SHORTER, ADD SOME FIELDS
            
            if len(database[i]) < len(database[0]):

                # FOR J IN THE RANGE 0 to DISPARITY IN FIELDS
                
                for j in range(0, (len(database[0]) - len(database[i]))):
                    # ADD EMPTY TO THE END
                    database[i].append("")

            # IF THE ROW IS LONGER, POP FIELD FROM END
            
            if len(database[0]) < len(database[i]):

                # FOR J IN THE RANGE DISPARITY TO 0
                
                for j in range(len(database[i]) - len(database[0]), 0, -1):
                    database[i].pop(-1)
        
        f.close()
    
    # NO PRE EXISTING TABLE
    
    except FileNotFoundError:
        print("table.txt file not found.")
        return 1

    print(database)

# ESTABLISHES THE INTERPRETATION VARIABLE

interpretedCommand = ""

# DISPLAYS THE TABLE

def displayTable():
    for i in database:
        print(i)

# MODIFIES FIELD IN RECORD

def modify():
    global interpretedCommand
    global database

    # CHECKS SYNTAX AND ARGUMENTS
    
    try:
        
        if interpretedCommand[2] != "IN":
            print("Syntax Error")
            return 1
        
        # CARRIES OUT RECORD MODIFICATION. CHECKS FOR EXISTENCE OF FIELD.

        try:
            database[int(interpretedCommand[3])][database[0].index(
            interpretedCommand[1])] = interpretedCommand[4]

        # THROWS EXCEPTION
        
        except ValueError:
            print("Field does not exist.")
            return 1
    
    # THROWS EXCEPTION
    
    except IndexError:
        print("Syntax Error. MODIFY (field) IN (record) (content)")
        return 1

# DELETES CONTENT OF DATABASE, EXCLUDING TITLE INDEX

def dropTable():
    global database
    for i in range(1, len(database)):
        for j in range(len(database[i])):
            database[i][j] = ""
    return 1

# RETURNS CERTAIN FIELDS

def select():
    global interpretedCommand
    global database

    # CHECKS SYNTAX AND ARGUMENTS
    
    try:
        if interpretedCommand[2] != "FROM" and interpretedCommand[2] != "WHERE":
            print("Syntax Error")
            return 1

        # SELECT FIELD IN A RECORD
        
        if interpretedCommand[2] == "FROM":
            if interpretedCommand[1] == "*":
                print(database[int(interpretedCommand[3])])
            else:

                # ATTEMPTS TO RETURN FIELDS
                
                try:
                    print(database[int(interpretedCommand[3])][database[0].index(interpretedCommand[1])])
                
                # THROWS EXCEPTION
                
                except IndexError:
                    print("Field not found.")
                    return 1

        # SELECT RECORDS THAT MEET A SPECIFIC CONDITION
        
        elif interpretedCommand[2] == "WHERE":

            # MAKE A SUB ARRAY TO SIMPLIFY PARSING
    
            evalSubArray = []

            # ADD THE 3 SECTIONS OF THE EVAL SUB ARRAY
            # BY TAKING THE LAST 3 OF THE FULL COMMAND

            # TRY ADDING THE LAST 3
            try:
                for i in range(0, 3):
                    evalSubArray.append(interpretedCommand[i + 3])

            except IndexError:
                print("Cannot evaluate condition. Syntax: (field) (== or !=) (content).")
                return 1
            
            try:

                try:

                    # GET THE INDEX OF THE FIELD IN INDEX ROW
                    conditionToCheck = database[0].index(evalSubArray[0])

                # IF IT DOESN'T EXIST
                except ValueError:
                    print("Condition does not match database.")
                    return 1

                # MAKE AN ARRAY TO STORE RECORDS MATCHING THE CONDITION
                resultsArray = []

                # IF OUR EVAL IS FIELD EQUALS CONTENT:
                if evalSubArray[1] == "==":

                    # FOR EVERY ROW IN THE DATABASE
                    for i in range(0, len(database)):

                        # CHECK THE FIELD IN THE RECORD AND SEE IF IT EQUALS THE CONTENT
                        if database[i][conditionToCheck] == evalSubArray[2]:

                            # ADD THE RECORD TO THE ARRAY IF IT DOES
                            resultsArray.append(i)

                # OR IF THE EVAL IS FIELD NOT EQUALS CONTENT
                elif evalSubArray[1] == "!=":

                    # FOR EVERY ROW IN THE DATABASE
                    for i in range(0, len(database)):

                        # CHECK THE FIELD IN THE RECORD 
                        # AND SEE IF IT DOESN'T EQUAL THE CONTENT
                        if database[i][conditionToCheck] != evalSubArray[2]:

                            # ADD THE RECORD TO THE ARRAY IF THIS IS TRUE
                            resultsArray.append(i)

                # IF THE OPERATOR ISNT EQUALS OR NOT EQUALS
                else:
                    print("Cannot evaluate condition. Use == or !=.")
                    return 1

                # IF THEY WANT THE WHOLE RECORD
                if interpretedCommand[1] == "*":

                    for i in resultsArray:

                        # PRINT ALL RECORDS THAT MATCHED OUR CONDITIONS
                        print(database[i])

                else:

                    for i in resultsArray:

                        # OR PRINT THE SPECIFIC FIELD THEY ASKED FOR
                        print(database[i][database[0].index(interpretedCommand[1])])

            # IF THE EVAL STRING IS TOO SHORT
            except IndexError:
                print("Cannot evaluate condition. Syntax: (field) (== or !=) (content).")
                return 1
    
    # THROWS EXCEPTION IF ANYTHING ELSE IS MISSING
    
    except IndexError:
        print("Syntax Error. SELECT (field) FROM (record), or SELECT (field) WHERE (condition)", 
              "Use * to select an entire record.")
        return 1

# ADDS A RECORD TO THE TABLE

def addRecord():
    global interpretedCommand
    global database

    # ADDS THE CORRECT NUMBER OF FIELDS TO THE NEW RECORD
    
    database.append([])
    for i in range(len(database[0])):
        database[-1].append("")

# SAVE TABLE

def save():

    # OPENS TABLE STORAGE FILE AND OVERWRITES A BLANK

    f = open("table.txt", "wt")
    f.write("")
    f.close()

    # OPENS IN APPEND MODE TO ADD CURRENT DATA

    f = open("table.txt", "at")

    # PREVENTS "DATA SHIFTS" BY REPLACING BLANKS WITH NULL.

    for i in range(0, len(database)):
        for j in range(0, len(database[i])):
            if database[i][j] == "":
                database[i][j] = "NULL"

    # FOR THE LENGTH OF THE DATABASE:

    for i in range(0, len(database)):

        # SET THE FIRST PART OF THE STRING TO WRITE

        lineToWrite = str(database[i][0])

        # FOR THE LENGTH OF THE ROW, EXCLUDING FIRST WORD

        for j in range(1, len(database[i])):

            # APPEND TO WRITE CONTAINER

            lineToWrite = lineToWrite + " " + database[i][j]

        # WRITE TO TEXT FILE

        f.write(lineToWrite)

        if i != (len(database) - 1):
            f.write("\n")

    # TIDY UP

    f.close()

# SEARCH FOR A CERTAIN STRING IN A CERTAIN FIELD

def search():
    try:
        if interpretedCommand[1] != "FOR":
            print("Syntax Error")
            return 1

        resultsArray = []
        columnNumber = database[0].index(interpretedCommand[2])
        searchQuery = interpretedCommand[3]

        for i in range(1, len(database)):
            if database[i][columnNumber] == searchQuery:
                resultsArray.append(i)

        print(resultsArray)

    except IndexError:
        print("Syntax Error")
        return 1
        
# LAUNCHES RUNTIME ENVIRONMENT TO RUN COMMANDS IN. LOOPS BACK INTO ITSELF.

def runtime():
    global interpretedCommand

    cmd = input()
    interpretedCommand = cmd.split()

    try:
        if interpretedCommand[0] == "MODIFY":
            modify()
            displayTable()
        elif interpretedCommand[0] == "DROPTABLE":
            dropTable()
            displayTable()
        elif interpretedCommand[0] == "SELECT":
            select()
        elif interpretedCommand[0] == "ADDRECORD":
            addRecord()
            displayTable()
        elif interpretedCommand[0] == "SAVE":
            save()
            displayTable()
        elif interpretedCommand[0] == "SEARCH":
            search()
        else:
            print("Command Unknown")
    except IndexError:
        print("Command Unknown")

# RUNS THE CODE, BOTH INITIATION AND RUNTIME.

init()
while True:
    runtime()