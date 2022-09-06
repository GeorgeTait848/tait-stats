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


def insertData(conn, cursor, cols, dataFrame):
    pass




def main():

    fixturesTableName, statsTableName = getTableNames()

    fixturesFieldInfo, statsFieldInfo = getTableFieldInfo()

    conn = fetchConnection()
    cursor = conn.cursor()

    createTable(conn, cursor, fixturesTableName, fixturesFieldInfo)
    createTable(conn, cursor, statsTableName, statsFieldInfo)

    cursor.close()
    conn.close()
    


if __name__ == '__main__':
    main()

    # conn = fetchConnection()
    # cursor = conn.cursor()

    # cursor.execute('DROP TABLE IF EXISTS stats')
    # cursor.execute('DROP TABLE IF EXISTS fixtures')
    # conn.commit()



    






    
    

    
