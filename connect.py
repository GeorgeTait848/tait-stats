from configparser import ConfigParser
import psycopg2 as pg


def fetchConnection():

    #dictionary containing info about database for connection
    db_info = config()

    #connect to the database, MUST be closed at end of session.
    connection = pg.connect(**db_info)
    print('Successfully connected to: {}'.format(db_info['database']))
    
    return connection


def config(filename = 'params.ini', section = 'postgresql'):

    parser = ConfigParser()
    try:
        parser.read(filename)
    except:
        raise Exception('Could not read {}'.format(filename))


    if parser.has_section(section) == False:
        raise Exception('Section {} not found in file {}'.format(section, filename))


    db_info = dict(parser.items(section))

    return db_info




