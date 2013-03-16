import sqlite3
 
conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE filelist (
                  id INTEGER PRIMARY KEY,
                  filepath text
                  ) 
               """)
conn.close()
