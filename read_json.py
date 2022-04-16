from kivy.storage.jsonstore import JsonStore

store = JsonStore('blog_posts.json')

for item in store:
	print(item)