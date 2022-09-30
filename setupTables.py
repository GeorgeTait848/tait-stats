from readCSV import *
from connect import *


def getFieldsInfo(tableName):
    tableFields = {

        'dismissals': '''dismissal_id SERIAL PRIMARY KEY,
            dismissal_name VARCHAR(50) NOT NULL''',
        
        'teams': '''team_id SERIAL PRIMARY KEY,
            team_name VARCHAR(50)''',

        'formats': '''format_id SERIAL PRIMARY KEY,
            format_name VARCHAR(50)''',
        
        'seasons': '''season_id SERIAL PRIMARY KEY,
            year INT NOT NULL''',

        'dates': '''date_id SERIAL PRIMARY KEY,
            season_id INT NOT NULL,
            week_no int,
            date date NOT NULL,
            CONSTRAINT fk_season
                FOREIGN KEY(season_id) REFERENCES seasons(season_id)''',

        'fixtures': '''fixture_id SERIAL PRIMARY KEY,
            date_id INT NOT NULL,
            format_id INT NOT NULL,
            team_id INT NOT NULL,
            opposition VARCHAR(50) NOT NULL,
            home_away VARCHAR(50) NOT NULL,
            CONSTRAINT fk_date
                FOREIGN KEY(date_id) REFERENCES dates(date_id),
            CONSTRAINT fk_format
                FOREIGN KEY(format_id) REFERENCES formats(format_id),
            CONSTRAINT fk_team
                FOREIGN KEY(team_id) REFERENCES teams(team_id)''',
        
        'stats': '''fixture_id INT NOT NULL,
            dismissal_id INT NOT NULL,
            balls INT NOT NULL,
            runs INT NOT NULL,
            fours INT NOT NULL,
            sixes INT NOT NULL,
            CONSTRAINT fk_fixture
                FOREIGN KEY(fixture_id) REFERENCES fixtures(fixture_id),
            CONSTRAINT fk_dismissal
                FOREIGN KEY(dismissal_id) REFERENCES dismissals(dismissal_id)'''
    }

    if tableName not in tableFields:
        names = list(tableFields.keys())

        print(' \n{} is not a required table name.'.format(tableName))
        print('The names of the tables of this database are:')
    
        for name in names:
            print(name)

        return

    return tableFields[tableName]
    


def createTable (conn, cursor, tableName): 

    fieldsInfo = getFieldsInfo(tableName)

    cursor.execute('DROP TABLE IF EXISTS {} CASCADE;'.format(tableName))
    conn.commit()

    sql_query = '''CREATE TABLE {}(
        {});'''.format(tableName, fieldsInfo)

    cursor.execute(sql_query)
    conn.commit()
    print('Successfully created table {}.'.format(tableName))


def getInsertStatement(tableName, *cols):

    query = 'INSERT INTO {} ('.format(tableName)

    for i in range(len(cols)-1):
        query += '{}, '.format(cols[i])

    query += '{})'.format(cols[len(cols)-1])

    return query



def initialiseTableFromDF(conn, cursor, tableName, containsIDs = True, keepIDs = False):

    df = fetchDFfromCSV(tableName)
    header = df.columns.tolist()
    data = df.itertuples()

    if containsIDs: 
        if keepIDs:
            startIndex = 1
        else: 
            startIndex = 2
            header.pop(0) #remove id column from header

    else: 
        startIndex = 1 #ie always ignore pd indices.
    
    query = getInsertStatement(tableName, *header)
    query += '''
    VALUES 
        '''
    for row in data:
        temp = '('

        for i in range(startIndex, len(row)-1):

            #keep string symbols for sql
            if type(row[i]) != str:
                temp += '{}, '.format(row[i])
            else:
                temp += "'{}', ".format(row[i])

        if type(row[len(row)-1]) != str:
            temp += '{}),'.format(row[len(row)-1])
        else: 
            temp += "'{}'),".format(row[len(row)-1])

        query += temp + '''
        '''

    query = query[:-10] + ';' # 9 characters of whitespace and then comma to be removed and replaced by ; to end query

    
    cursor.execute(query)
    conn.commit()
    print('Successfully initialised table {}'.format(tableName))


def main():
    conn = fetchConnection()
    cursor = conn.cursor()

    namesWithoutStats = ['dismissals', 'teams', 'formats', 'seasons', 'dates', 'fixtures']
    for name in namesWithoutStats: 

        createTable(conn, cursor, name)
        initialiseTableFromDF(conn, cursor, name)

    #stats requires the column fixture_id to be kept as it has no serial column

    createTable(conn, cursor, 'stats')
    initialiseTableFromDF(conn, cursor, 'stats', containsIDs=False)

    cursor.close()
    conn.close()

    


if __name__ == '__main__':
    main()



    






    
    

    
