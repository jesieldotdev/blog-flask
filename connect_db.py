import sqlite3

conn = sqlite3.connect('db.sqlite3')
conn.row_factory=sqlite3.Row
cursor = conn.cursor()



cursor.execute('''
	SELECT * FROM BLOG_POSTS;

	''')

db = cursor.fetchall()

conn.close()