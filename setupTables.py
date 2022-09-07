from operator import le
from readCSV import *
from connect import *


def getTableNames():
    return 'fixtures', 'stats'


def getTableFieldInfo():

    fixturesFieldInfo = '''fixture_id SERIAL PRIMARY KEY,
    home_away VARCHAR(50) NOT NULL,
    opposition VARCHAR(50) NOT NULL,
    format VARCHAR(50) NOT NULL,
    date DATE NOT NULL'''

    statsFieldInfo = '''fixture_id SERIAL PRIMARY KEY,
    balls_faced INT NOT NULL,
    runs_scored INT NOT NULL,
    fours INT NOT NULL,
    sixes INT NOT NULL,
    m_o_d VARCHAR(50) NOT NULL,
    FOREIGN KEY(fixture_id) REFERENCES fixtures(fixture_id)'''

    return fixturesFieldInfo, statsFieldInfo



def createTable (conn, cursor, tableName, fieldInfo): 

    cursor.execute('DROP TABLE IF EXISTS {}'.format(tableName))
    conn.commit()

    sql_query = '''CREATE TABLE {}(
        {}
        );'''.format(tableName, fieldInfo)

    cursor.execute(sql_query)
    conn.commit()
    print('Successfully created table {}.'.format(tableName))


def getInsertStatement(tableName, *cols):

    query = 'INSERT INTO {} ('.format(tableName)

    for i in range(len(cols)-1):
        query += '{}, '.format(cols[i])

    query += '{})'.format(cols[len(cols)-1])

    return query



def initialiseTableFromDF(conn, cursor, tableName, df, containsIDs = True, keepIDs = False):

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
            temp += '''{}),
            '''.format(row[len(row)-1])
        else: 
            temp += "'{}'),".format(row[len(row)-1])

        query += temp + '''
        '''

    query = query[:-10] + ';' # 9 characters of whitespace and then comma to be removed and replaced by ; to end query

    
    cursor.execute(query)
    conn.commit()
    print('Successfully initialised table {}'.format(tableName))
    






def main():
    fixtures_df, stats_df = fetchDataFrames()

    fixturesTableName, statsTableName = getTableNames()
    fixturesFieldInfo, statsFieldInfo = getTableFieldInfo()

    conn = fetchConnection()
    cursor = conn.cursor()

    createTable(conn, cursor, fixturesTableName, fixturesFieldInfo)
    createTable(conn, cursor, statsTableName, statsFieldInfo)
    initialiseTableFromDF(conn, cursor, fixturesTableName, fixtures_df)
    initialiseTableFromDF(conn, cursor, statsTableName, stats_df)
    # createTable(conn, cursor, statsTableName, statsFieldInfo)

    cursor.close()
    conn.close()
    


if __name__ == '__main__':
    main()



    






    
    

    
