import sqlite3
import os

# Creates agents.sqlite
# TMC has issues with binary files, so we will go around by creating it locally from the text dump.

db = \
"""
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Users (name TEXT, password TEXT, balance REAL);
INSERT INTO Users VALUES('admin','coffee', 100);
INSERT INTO Users VALUES('bob','passwd', 250);
INSERT INTO Users VALUES('alice', 'redqueen', 300);
COMMIT;
"""

if os.path.exists('users.sqlite'):
	print('tasks.sqlite already exists')
else:
	conn = sqlite3.connect('users.sqlite3')
	conn.cursor().executescript(db)
	conn.commit()