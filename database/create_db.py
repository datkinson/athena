#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('athena.db')
print "Opened database"
conn.execute('''CREATE TABLE map
		(id int primary key,
		name text not null,
		type text,
		short_description text,
		description text,
		n int,
		e int,
		s int,
		w int,
		ne int,
		nw int,
		se int,
		sw int,
		up int,
		down int);''')
print "Table created"
conn.close()

