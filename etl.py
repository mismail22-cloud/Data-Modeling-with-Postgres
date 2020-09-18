import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)



def process_song_file(cur, filepath):
    """
    This function process a Songs file , loading data to Songs ,Artist dimension tables. 
    """
    # open song file
    df = pd.read_json (filepath,lines=True) 

    # insert song record
    song_data_df = pd.DataFrame(df, columns= ['song_id','title','artist_id','year','duration']).iloc[0]
    song_data_df.year = song_data_df.year.astype(int) 
    song_data = song_data_df.tolist() 
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data_df=pd.DataFrame(df,columns=['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']).iloc[0]
    artist_data=artist_data_df.tolist()
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    """
    This function process a Log file , loading data to Time ,User dimension tables and Songsplay Fact Table. 
    """
    # open log file
    df = pd.read_json (filepath,lines=True)
    df = df[df['page']== 'NextSong']
    # filter by NextSong action
    time_data_df = pd.DataFrame(df, columns= ['ts'])

    # convert timestamp column to datetime
    time_data_df = pd.to_datetime(time_data_df.ts)
    
    # insert time data records
    time_data = [time_data_df.tolist(),time_data_df.dt.hour,time_data_df.dt.day,time_data_df.dt.week,time_data_df.dt.month,time_data_df.dt.year,time_data_df.dt.weekday]
    column_labels = ['start_time','Hour','Day','Week','Month','Year','weekday'] 
    time_data_ser ={column_labels[0]:time_data[0],column_labels[1]:time_data[1],column_labels[2]:time_data[2],column_labels[3]:time_data[3],column_labels[4]:time_data[4],column_labels[5]:time_data[5],column_labels[6]:time_data[6]}
    time_df = pd.DataFrame(time_data_ser)


    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame(df, columns= ['userId', 'firstName', 'lastName', 'gender' , 'level'])
    user_df.userId = user_df.userId.astype(int) 
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = list( [pd.to_datetime(row.ts), row.userId, row.level, songid, artistid, row.sessionId, row.location,  row.userAgent] )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """
    This function process the files by getting files matching extension , printing total number of files , calling respective functions for processing  each file 
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()