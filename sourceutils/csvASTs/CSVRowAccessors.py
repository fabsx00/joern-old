
ROW_TYPE = 0
START_POS = 1
END_POS = 2
LEVEL = 3
CONDITION = 4

def getCSVRowType(row):
    return row[ROW_TYPE]

def getCSVRowStartPos(row):
    return row[START_POS].split(':')

def getCSVRowEndPos(row):
    return row[END_POS].split(':')

def getCSVRowLevel(row):
    return row[LEVEL]

def getCSVRowCondition(row):
    return row[CONDITION]