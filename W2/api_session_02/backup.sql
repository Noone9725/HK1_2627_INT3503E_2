BEGIN TRANSACTION;
CREATE TABLE books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        price REAL,
                        isbn TEXT
                      );
INSERT INTO "books" VALUES(1,'Clean Code','R. Martin',25.5,NULL);
INSERT INTO "books" VALUES(2,'Clean Architecture','R. Martin',28.0,NULL);
INSERT INTO "books" VALUES(3,'1984','Orwell',15.0,NULL);
CREATE TABLE orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL
                      );
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('books',3);
COMMIT;
