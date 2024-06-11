# SQLSEQUEL - A NEW DATABASE LANGUAGE
# [==============================] INDICATES END OF CODE SECTION
# THIS SOFTWARE IS BASED LOOSELY OFF OF SQL.
# IT UTILISES A 2D ARRAY CONSISTING OF LISTS WITHIN A LIST.
# I PLAN TO ADD .CSV EXPORT AT A LATER DATE.

# INITIALISES 2D ARRAY FOR DATA STORAGE

database = [

    # INDEX ROW TO PREVENT INDEX ERROR
    
    []

    # [==============================]
    
]

# [==============================]

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

        # IMPORT table.txt
        if fieldName == "IMPORTTABLE":
            importTable()

        # OTHERWISE, ADD THE FIELD TO THE INDEX ROW
        if fieldName != "IMPORTTABLE":
            database[0].append(fieldName)

            for i in range(1, len(database)):
                database[i].append("")

# [==============================]

# DISPLAYS THE TABLE

def displayTable():
    for i in database:
        print(i)

# [==============================]

# SAVE TABLE

def save():
    
    # OPENS TABLE STORAGE FILE AND OVERWRITES A BLANK
    f = open("table.txt", "wt")
    f.write("")
    f.close()

    # OPENS IN APPEND MODE TO ADD CURRENT DATA
    f = open("table.txt", "at")

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
                
# [==============================]

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

    print(database)

# ESTABLISHES THE INTERPRETATION VARIABLE

interpretedCommand = ""

# [==============================]

# MODIFIES FIELD IN RECORD

def modify():
    global interpretedCommand
    global database

    # CHECKS SYNTAX AND ARGUMENTS
    
    try:
        
        if interpretedCommand[2] != "IN":
            print("Syntax Error")
            return 0

    # [==============================]
        
        # CARRIES OUT RECORD MODIFICATION. CHECKS FOR EXISTENCE OF FIELD.

        try:
            database[int(interpretedCommand[3])][database[0].index(
            interpretedCommand[1])] = interpretedCommand[4]

        # [==============================]

        # THROWS EXCEPTION
        
        except ValueError:
            print("Field does not exist.")
            return 0
        
        # [==============================]
    
    # THROWS EXCEPTION
    
    except IndexError:
        print("Syntax Error. MODIFY (field) IN (record) (content)")
        return 0

    # [==============================]

# [==============================]

# DELETES CONTENT OF DATABASE, EXCLUDING TITLE INDEX

def dropTable():
    global database
    for i in range(1, len(database)):
        for j in range(len(database[i])):
            database[i][j] = ""
    return 0

# [==============================]

# RETURNS CERTAIN FIELDS

# TODO: return the actual field, this is a bit broken

def select():
    global interpretedCommand
    global database

    # CHECKS SYNTAX AND ARGUMENTS
    
    try:
        if interpretedCommand[2] != "FROM":
            print("Syntax Error")
            return 0
        if interpretedCommand[1] == "*":
            print(database[int(interpretedCommand[3])])
        else:

            # ATTEMPTS TO RETURN FIELDS
                
            try:
                print(database[int(interpretedCommand[3])][database[0].index(interpretedCommand[1])])

            # [==============================]
                
            # THROWS EXCEPTION
                
            except IndexError:
                print("Field not found.")

                # [==============================]
    
    # [==============================]
    
    # THROWS EXCEPTION
    
    except IndexError:
        print("Syntax Error. SELECT (field) FROM (record).", 
              "Use * to select an entire record.")

    # [==============================]

# [==============================]

# ADDS A RECORD TO THE TABLE

def addRecord():
    global interpretedCommand
    global database

    # ADDS THE CORRECT NUMBER OF FIELDS TO THE NEW RECORD
    
    database.append([])
    for i in range(len(database[0])):
        database[-1].append("")

    # [==============================]

# [==============================]

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
        else:
            print("Command Unknown")
    except IndexError:
        print("Command Unknown")

# [==============================]

# RUNS THE CODE, BOTH INITIATION AND RUNTIME.

init()
while True:
    runtime()

# [==============================]