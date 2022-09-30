from connect import *
from datetime import datetime as dt


def getRecordParameters():

    params = {}

    date_str = input('Please enter date of fixture in the form YYYY-MM-DD: ')
    date = dt.strptime(date_str, '%Y-%m-%d').date()
    season = date.year

    params['date'] = "'{}'".format(date_str)
    params['season'] = season

    params['fomat'] = input('Enter the format of the fixture: ')

    params['team'] = input('Enter who the fixture was played for: ')
    params['opposition'] = input('Enter the opposition: ')
    params['home_away'] = 'home' if input('Was this a home fixture? (y/n): ') else 'away'

    leagueFixture = True if input('Was this a league fixture? (y/n): ') == 'y' else False

    if leagueFixture:
        params['week_no'] = input('Enter the week number for the fixture: ')

    params['dismissal_name'] = input('Enter mode of dismissal: ')
    params['balls'] = input('enter balls faced: ')
    params['runs'] = input('Enter runs scored: ')
    params['fours'] = input('Enter number of fours hit: ')
    params['sixes'] = input('Enter number of sixes hit: ')

    return params
    


def updateRecords(**params):

    pass