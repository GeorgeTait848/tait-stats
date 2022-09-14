import pandas as pd
import numpy as np
from connect import fetchConnection
import plotly.express as px

class StatsAnalyser: 

    def __init__(self, connection):

        self.connection = connection
        self.cursor =  self.connection.cursor()

    def getAverage(self):

        cur = self.cursor

        cur.execute('SELECT runs_scored FROM stats;')
        allRuns = pd.DataFrame(self.cursor.fetchall(), columns=['runs_scored'])
        totalRuns = allRuns['runs_scored'].sum()
        
        cur.execute("SELECT COUNT(m_o_d) FROM stats WHERE m_o_d != 'not out'")
        noOfDismissals = cur.fetchone()[0]

        return totalRuns/noOfDismissals


    def getLocalAverages(self, overGames=3):
        '''returns a dataframe of moving averages for the most recent overGames games. default number of games is three.'''

        cur = self.cursor
        
        cur.execute('SELECT fixture_id, runs_scored, m_o_d FROM stats')
        data = pd.DataFrame(cur.fetchall(), columns=['id', 'runs', 'mod'])

        runs = data['runs'].tolist()
        mods = data['mod'].tolist()
        ids = data['id']
        averages = []

        for i in range(overGames-1,len(runs)):

            localRuns = runs[i-(overGames-1):i+1]
            local_mods = mods[i-(overGames-1):i+1]


            localTotal = sum(localRuns)
            localDismissals = list(filter(lambda str: (str != 'not out'), local_mods))
            localNumDismissals = len(localDismissals)
            localAve = localTotal/localNumDismissals
            localDict = {'week no.': ids[i], 'local ave': localAve}
            
            
            averages.append(localDict)

        return pd.DataFrame(averages)

    def plotLocalAverages(self, overGames=3):

        localAves = self.getLocalAverages(overGames)
        fig = px.line(localAves, x='week no.', y='local ave', markers=True)
        fig.show()



def main():

    conn = fetchConnection()

    analyser = StatsAnalyser(conn)
    analyser.plotLocalAverages()


if __name__ == '__main__':
    main()