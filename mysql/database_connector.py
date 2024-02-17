import pymysql



## config connection
timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="your.database.host.name",
  password="password",
  read_timeout=timeout,
  port=port,
  user="avnadmin",
  write_timeout=timeout,
)


