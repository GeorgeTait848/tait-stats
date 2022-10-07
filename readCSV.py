import pandas as pd


def editDateFormat(str):
    #intended for a date in format dd/mm/yy and makes it yy-mm-dd
    split = str.split('/')
    return '-'.join(reversed(split))

    
def fetchDFfromCSV(key):

    'returns a pandas dataframe with the contents of the csv file with name referred to by key'

    csvDirectory = './csv_files/'

    pathsDict = {
        'dismissals': csvDirectory + 'dismissals.csv',
        'teams': csvDirectory + 'teams.csv',
        'formats': csvDirectory + 'formats.csv',
        'seasons': csvDirectory + 'seasons.csv',
        'dates': csvDirectory + 'dates.csv',
        'fixtures': csvDirectory + 'fixtures.csv',
        'stats': csvDirectory + 'stats.csv',
        'oppositions': csvDirectory + 'oppositions.csv',
    }

    if key not in pathsDict: 
        print('The key {} does not refer to a path to an existing csv file')
        print('The possible options are:')

        correctKeys = list(pathsDict.keys())

        for correctKey in correctKeys:
            print(correctKey)

        return
    
    df = pd.read_csv(pathsDict[key])

    if key == 'dates':

        for index in df.index:
         df.loc[index, 'date'] = editDateFormat(df.loc[index, 'date'])
    
    return df



    
def main():

    '''Tests the fetchDFfromCSV function'''
    names = ['dismissals', 'teams', 'formats', 'seasons', 'dates', 'fixtures', 'stats', 'oppositions']

    for name in names: 
        print(fetchDFfromCSV(name)) 
        print('\n')



if __name__ == '__main__':
    main()