import re, sqlite3
from pyquery import PyQuery
from collections import Counter

def main():
	full_lyrics = ""		
	#open up the input file
	links = open('links.txt')
		
	for line in links:
		#create the PyQuery object and parse text
		results = PyQuery(url='%s' % line.strip())
		results = results('div.lyricbox').remove('script').text()
		full_lyrics += results
			
	#establish the database
	conn = sqlite3.connect('counts.db')
	c = conn.cursor()
	c.execute("DROP TABLE IF EXISTS counts")
	c.execute("CREATE TABLE IF NOT EXISTS counts (word TEXT, count INTEGER)")

	#remove all apostrophes to avoid getting chopped into separate words
	full_lyrics = full_lyrics.replace("'", "")
	#splits lyrics into list of words
	words = re.findall(r'\w+', full_lyrics.lower()) 
	#actually counts the words, puts them into a list of tuples
	counts = Counter(words).most_common()

	#writing the list of tuples into sqlite db
	for word in counts:
		c.execute("INSERT INTO counts ('word', 'count') VALUES (?, ?)" , (word[0], word[1]))

	c.execute("SELECT * FROM counts")
	print(c.fetchall())
	conn.commit()
	conn.close()
	links.close()
	
if __name__ == "__main__":
	main()
