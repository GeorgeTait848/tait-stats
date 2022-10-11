import updateRecords as ud
import setupTables as st
from connect import *

'''purpose of this file is to test the updateRecords.py file for three test cases: 
1: One day league game at home 1st week of 2023
2: Timed one day league game week 6 away
3: Oxfordshire three day away 2023
4: Repeat of 1 for 2024 with different opposition and mod.

Note these are bogus fixtures so will be deleted at the end of the file running.'''


def getCorrectParams(testCaseInt):

    recParams = {
        1: {
            'date': "'2023-05-06'",
            'season': 2023,
            'format': '50 over',
            'team': 'Oxford CC 1',
            'opposition': 'Cumnor CC',
            'home_away': 'home',
            'leagueFixture': True,
            'week_no': '1',
            'dismissal': 'bowled',
            'balls': '6',
            'runs': '5',
            'fours': '1',
            'sixes': '0'
            },

        2: {
            'date': "'2023-06-10'",
            'season': 2023,
            'format': 'timed od',
            'team': 'Oxford CC 1',
            'opposition': 'Great Brickhill CC',
            'home_away': 'away',
            'leagueFixture': True,
            'week_no': '6',
            'dismissal': 'not out',
            'balls': '120',
            'runs': '105',
            'fours': '8',
            'sixes': '3'
            },

        3: {
            'date': "'2023-07-16'",
            'season': 2023,
            'format': 'three day',
            'team': 'Oxfordshire CCC',
            'opposition': 'Cheshire CCC',
            'home_away': 'away',
            'leagueFixture': False,
            'dismissal': 'lbw',
            'balls': '60',
            'runs': '35',
            'fours': '6',
            'sixes': '0'
            },

        4: {
            'date': "'2024-05-05'",
            'season': 2024,
            'format': '50 over',
            'team': 'Oxford CC 1',
            'opposition': 'Cumnor CC',
            'home_away': 'home',
            'leagueFixture': True,
            'week_no': '1',
            'dismissal': 'caught',
            'balls': '6',
            'runs': '5',
            'fours': '1',
            'sixes': '0'
            }
    }


    return recParams[testCaseInt]

def testCorrectKeys(inputParams, testParams):
    return inputParams.keys() == testParams.keys()


def findIncorrectKey(inputParams, testParams):
    '''Finds the incorrect key and returns it. Only to be called when testCorrectKeys returns false.'''
    for key in testParams:
        if key not in inputParams:
            return key


def findIncorrectValue(inputParams, testParams):
    '''Finds the incorrect value in inputParams. 
    Only to be called when testParams and inputParams are not equal but the keys are the same'''

    for key in testParams:
        if testParams[key] != inputParams[key]:
            return key, inputParams[key]
            

def testRecordParams(inputParams, testCaseInt):

    correctParams = getCorrectParams(testCaseInt)
    if inputParams == correctParams:
        print('function getRecordParameters is working as expected for case {}'.format(testCaseInt))
        return True
        

    if testCorrectKeys(inputParams, correctParams) == False:
        incorrectKey = findIncorrectKey(inputParams, correctParams)
        print('key {} not found in input parameters when it was expected to be in test case {}.'.format(incorrectKey, testCaseInt))
        return False

    else: 
        key, incorrectVal = findIncorrectValue(inputParams, correctParams)
        print('Error: testParams has key-value pair {}:{} and inputParams has key-value pair {}:{} in test case {}'.format(key, correctParams[key], key, incorrectVal, testCaseInt))
        return False


def testUpdateRecords(): 

    testsPassed = []
    for i in range(1,5):
        print('Test Case {}'.format(i))
        inputParams = ud.getRecordParameters()
        testsPassed.append(testRecordParams(inputParams, i))

    if all(testsPassed) == False:

        print('testRecordParameters tests not passed. Aborting update of the database.')
        return 

    conn = fetchConnection()
    cur = conn.cursor()
    print('All tests passed for getRecordParameters. Updating the database with each test case.')

    for i in range(1,5):
        ud.updateDatabase(cur, conn, **getCorrectParams(i))
    
    successfulUpdate = True if input('Are the databases updated properly? Check in postgresql (y/n): ') =='y' else False

    if successfulUpdate:

        print('All tests passed and database properly updated')
        cur.close()
        conn.close()
        #restoring db back to original state without bogus fixtures
        st.main()
        return 
    
    print('Unsuccessful update of database. updateRecords.py will be edited and tested again.')
    cur.close()
    conn.close()
    st.main()
    return

def main():

    testUpdateRecords()

if __name__ == '__main__':

    main()






        




            


                




