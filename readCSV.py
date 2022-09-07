import pandas as pd


def editDateFormat(str):
    #intended for a date in format dd/mm/yy and makes it yy-mm-dd
    split = str.split('/')
    return '-'.join(reversed(split))

def fetchDataFrames():

    pathToStats = 'csv_files/stats2022.csv'
    pathToFixtures = 'csv_files/fixtures2022.csv'

    stats = pd.read_csv(pathToStats)
    fixtures = pd.read_csv(pathToFixtures)

    #need to edit date format so compatible with sql date type.
    for index in fixtures.index:
        fixtures.loc[index, 'date'] = editDateFormat(fixtures.loc[index, 'date'])

    return fixtures, stats

    

