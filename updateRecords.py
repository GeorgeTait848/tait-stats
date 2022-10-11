from connect import *
from datetime import datetime as dt
from setupTables import getInsertStatement


def getRecordParameters():

    recParams = {}

    date_str = input('Please enter date of fixture in the form YYYY-MM-DD: ')
    date = dt.strptime(date_str, '%Y-%m-%d').date()
    season = date.year

    recParams['date'] = "'{}'".format(date_str)
    recParams['season'] = season

    recParams['format'] = input('Enter the format of the fixture: ')

    recParams['team'] = input('Enter who the fixture was played for: ')
    recParams['opposition'] = input('Enter the opposition: ')
    recParams['home_away'] = 'home' if input('Was this a home fixture? (y/n): ') == 'y' else 'away'

    recParams['leagueFixture'] = True if input('Was this a league fixture? (y/n): ') == 'y' else False

    if recParams['leagueFixture']:
        recParams['week_no'] = input('Enter the week number for the fixture: ')

    recParams['dismissal'] = input('Enter mode of dismissal: ')
    recParams['balls'] = input('enter balls faced: ')
    recParams['runs'] = input('Enter runs scored: ')
    recParams['fours'] = input('Enter number of fours hit: ')
    recParams['sixes'] = input('Enter number of sixes hit: ')

    return recParams
    
def getForeignKeyIDQuery(key):

    '''Returns a string representing the SQL query to get the id and value pair for a necessary foreign key.'''

    queries = {
        'season': 'SELECT year, season_id FROM seasons;',
        'team': 'SELECT team_name, team_id FROM teams;',
        'opposition': 'SELECT opposition_name, opposition_id FROM oppositions',
        'format': 'SELECT format_name, format_id FROM formats',
        'team': 'SELECT team_name, team_id FROM teams',
        'dismissal': 'SELECT dismissal_name, dismissal_id FROM dismissals',
    }

    return queries[key]

def getNonChildColToInsert(key):

    # Tables formats, dismissals will never need to be updated.
    # Unless I start playing in hundred fixtures or a new format/mode of dismissal is invented. 
    #in which case, it will be simpler to update the tables manually.

    cols = {
        'season': 'year',
        'team': 'team_name',
        'opposition': 'opposition_name',
    }

    return cols[key]




def updateNonChildTable(cursor, conn, key, **recParams):
    '''The non-child tables contain no foreign key constraints, meaning they can be updated from the input data. 
    By design, all non-child tables also may not need to be updated. 
    This function updates those tables directly from the parameters, if called by getNewEntryID'''

    col = getNonChildColToInsert(key)
    insertStatement = '''INSERT INTO {}s ({})
    VALUES ('{}');'''.format(key, col, recParams[key])

    cursor.execute(insertStatement)
    conn.commit()

    print('Added {} {} to table {}s'.format(key, recParams[key], key))


def getNonChildEntryID(cursor, conn, key, staticTable = False, **recParams):

    query = getForeignKeyIDQuery(key)
    cursor.execute(query)
    containedInDB = dict(cursor.fetchall())

    if recParams[key] in containedInDB:
        return containedInDB[recParams[key]]

    if staticTable: 
        print('Entry not found in static table, manually update this table and retry')
        return

    if input('{} {} was not found in the database. Would you like to add it? (y/n): '.format(key, recParams[key])) == 'y':
        updateNonChildTable(cursor, conn, key, **recParams)
        return getNonChildEntryID(cursor, conn, key, staticTable,  **recParams)

    else:
        print('''You have chosen not to add the {} {} to the database. 
        To continue, enter a season which already exists or one you wish to add to the database.'''.format(key, recParams[key]))

        return

def updateDatesTable(cursor, conn, **recParams):

    season_id = getNonChildEntryID(cursor, conn, 'season', **recParams)
    date = recParams['date']

    cols = ['season_id', 'date']
    leagueFixture = recParams['leagueFixture']

    if leagueFixture:
        cols[1:2] = ['week_no', 'date']

    insertStatement = getInsertStatement('dates', *cols) 
    query = insertStatement + '''
    VALUES'''

    if leagueFixture: 
        weekNo = recParams['week_no']

        query += '''
        ({},{},{});'''.format(season_id, weekNo, date)

    else:
        query += '''
        ({},{});'''.format(season_id, date)

    cursor.execute(query)
    conn.commit()



def getNewEntryDateID(cursor, conn, **recParams):

    updateDatesTable(cursor, conn, **recParams)
    cursor.execute("SELECT date_id FROM dates WHERE date = {};".format(recParams['date']))
    date_id = cursor.fetchone()[0]
    

    return date_id
    

def updateFixturesTable(cursor, conn, **recParams): 

    date_id = getNewEntryDateID(cursor, conn, **recParams)
    format_id = getNonChildEntryID(cursor, conn, 'format', True, **recParams)

    parentTables = ['teams', 'oppositions']
    entryValues = [date_id, format_id]

    for tableName in parentTables:
        key = tableName[:-1]
        entryValues.append(getNonChildEntryID(cursor, conn, key, **recParams))
    
    entryValues.append(recParams['home_away'])

    query = '''INSERT INTO fixtures (date_id, format_id, team_id, opposition_id, home_away)
    VALUES 
        ({},{},{},{},'{}');'''.format(entryValues[0], entryValues[1], entryValues[2], entryValues[3], entryValues[4])

    cursor.execute(query)
    conn.commit()


def getNewEntryFixtureID(cursor, conn, **recParams):

    updateFixturesTable(cursor, conn, **recParams)
    cursor.execute('SELECT max(fixture_id) FROM fixtures')
    fixture_id = cursor.fetchone()[0]
    return fixture_id


    
def updateDatabase(cursor, conn, **recParams):

    '''Updates the tait_2022_stats database with a new entry defined by recParams.
    Explicitly, this function only updates the stats table but it calls functions which update all the other tables in the database.'''

    fixture_id  = getNewEntryFixtureID(cursor, conn, **recParams)
    dismissal_id = getNonChildEntryID(cursor, conn, 'dismissal', True, **recParams)
    balls = recParams['balls']
    runs = recParams['runs']
    fours = recParams['fours']
    sixes = recParams['sixes']


    query = '''INSERT INTO stats(fixture_id, dismissal_id, balls, runs, fours, sixes)
        VALUES
            ({},{},{},{},{},{});'''.format(fixture_id, dismissal_id, balls, runs, fours, sixes)

    cursor.execute(query)
    conn.commit()


def main():
    conn = fetchConnection()
    cur = conn.cursor()

    recParams = getRecordParameters()

    updateDatabase(cur, conn, **recParams)
    cur.close()
    conn.close()

    print('Successfully updated all tables in the database with the new record')



if __name__ == '__main__':
    main()


