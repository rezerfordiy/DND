import sqlite3

conn = sqlite3.connect('test.db')

query = "SELECT * FROM 'tarot_cards'"
cursor = conn.cursor()
cursor.execute(query)
data = (cursor.fetchall())
cards = []
for i in data:
    cards.append({"id": i[0], 
                  "name": i[1],
                  "arcana": i[2],
                  "suit": i[3]
                  })

for i in cards:
    print(i)
conn.close()


for i in cards:
    if i['suit'] == 'Старший аркан':
        i['d20'] = i['id']