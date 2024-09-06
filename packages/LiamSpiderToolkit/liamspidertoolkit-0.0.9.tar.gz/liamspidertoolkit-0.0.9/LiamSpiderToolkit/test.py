import sqlite3
import Spader_nover_jiami_to_sqliit
conn = sqlite3.connect('novels.db')
cursor = conn.cursor()
sql = 'insert into novels (novel_name, novel) values (?, ?)'
cursor.execute(sql, ('novel_name', 'novel'))

a = cursor.execute('select * from novels')
for i in a:
    print(i)

conn.commit()
print('Save to db success!')
