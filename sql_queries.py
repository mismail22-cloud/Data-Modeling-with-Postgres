# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users  "
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = ("Create table songplays (songplay_id serial primary key, start_time timestamp, user_id integer not null, level varchar(10), song_id varchar(50) , artist_id varchar(50) ,session_id integer, location varchar(50), user_agent varchar(200))")

user_table_create = ("Create table users(user_id integer primary key, first_name varchar(20), last_name varchar(20), gender varchar(5), level varchar(10))")

song_table_create = ("Create table songs(song_id varchar(50)  primary key, title varchar(200), artist_id varchar(50), year integer, duration numeric)")


artist_table_create = ("Create table artists(artist_id varchar(50)  primary key, name varchar(200), location varchar(200), latitude float, longitude float)")

time_table_create = ("Create table time(start_time timestamp primary key, hour int, day integer, week integer, month integer, year integer, weekday integer)")


# INSERT RECORDS

songplay_table_insert = ("insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location,  user_agent) values(%s, %s, %s,%s, %s,%s,%s,%s)")

user_table_insert = ("insert into users(user_id , first_name , last_name , gender , level ) values (%s, %s, %s,%s, %s) ON CONFLICT (user_id) DO UPDATE SET level=excluded.level  ")

song_table_insert = ("insert into songs (song_id,title,artist_id,year,duration) VALUES (%s, %s, %s,%s, %s) ON CONFLICT DO NOTHING")

artist_table_insert = ("insert into artists (artist_id, name, location , latitude , longitude ) VALUES (%s, %s, %s,%s, %s) ON CONFLICT DO NOTHING")


time_table_insert = ("insert into time(start_time , hour , day , week , month , year , weekday ) VALUES (%s, %s, %s,%s, %s,%s, %s) ON CONFLICT DO NOTHING")

# FIND SONGS

song_select = ("select song_id, artists.artist_id from songs join artists on artists.artist_id=songs.artist_id where title=%s  and  name=%s and duration=%s")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]