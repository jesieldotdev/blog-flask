import sqlite3

conn = sqlite3.connect('db.sqlite3')
conn.row_factory=sqlite3.Row
cursor = conn.cursor()



cursor.execute('''
	SELECT * FROM BLOG_POSTS;

	''')

db = cursor.fetchall()

qt = 4
qt2 = 8
limit = db[(qt):(qt2)]

#for key in limit:
 # print(key['title'])
start = 0
for i in range(5):
  start =+ i
  end = start * 2
  posts = db[start:end]
  start =+ 4
  
for key in posts:
  print(key['title'])

conn.close()