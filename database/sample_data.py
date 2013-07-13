#!/usr/bin/python
import sqlite3

conn = sqlite3.connect('athena.db')
print "Opened database"

conn.execute("INSERT INTO map (name, type, short_description, description, n, e, s, w, ne, nw, se, sw) \
		VALUES ('test room', 'road', 'A stone road', 'A road covered in rough stones.  It would hurt to walk on without and footwear.', 1, 1, 1, 1, 0, 0, 0, 0)");
conn.commit()
print "records saved"
conn.close()
