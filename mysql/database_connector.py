import pymysql


























## config connection
timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="mysql-5812e2f-nb-project.a.aivencloud.com",
  password="AVNS_P6TvtoPOiyyg02KDeB9",
  read_timeout=timeout,
  port=28602,
  user="avnadmin",
  write_timeout=timeout,
)


