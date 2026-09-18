import sqlite3

# Kết nối tới database
con = sqlite3.connect('data.db')

# Dump dữ liệu và ghi ra file backup.sql
with open('backup.sql', 'w', encoding='utf-8') as f:
    for line in con.iterdump():
        f.write('%s\n' % line)

con.close()
print("dump database ra file backup.sql")