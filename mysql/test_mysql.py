import pymysql
from database_connector import connection



try:
  cursor = connection.cursor()
  cursor.execute("describe users;")
  print(cursor.fetchall())
finally:
  connection.close()