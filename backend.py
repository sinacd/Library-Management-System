import sqlite3
import hashlib
from datetime import datetime
from time import strftime

from dateutil.relativedelta import relativedelta


class Backend:
    def __init__(self):
        self.startDB()
        res = self.employeeLogin("admin", "123")
        if res == "user does not exist":
            self.employeeCreate("admin", "123", "admin", "admin")
        # for i in range(10):
        #     self.createIssue(f"{i}", f"{i}")
        # self.createUser(f"user{i}", "john")
        #     self.createBook(f"book{i}", "john randy", 2030, 458730, 25)

        # print(self.search(title=''))

    def startDB(self):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.executescript("""
            create table if not exists book (id integer primary key, title nvarchar, author nvarchar,year integer , isbn nvharchar, shelf integer );
            create table if not exists user (id integer primary key, name nvarchar, family nvarchar,expireTime text  );
            create table if not exists userBook (id integer primary key, userId integer  NOT NULL CONSTRAINT FK_userId REFERENCES user(id),bookId integer  NOT NULL CONSTRAINT FK_bookId REFERENCES book(id),returned integer );
            create table if not exists employee (id integer primary key, userName nvarchar,password nvarchar,name nvarchar,family nvarchar );
            
            
            """)
        conn.commit()
        conn.close()

    def createBook(self, title, author, year, isbn, shelf):
        if year == 'year':
            year = ''
        if isbn == 'isbn':
            isbn = ''
        if shelf == 'shelf':
            shelf = ''
        conn = sqlite3.Connection("library.db")
        cursor = conn.cursor()
        cursor.execute("insert into book values (NULL,?,?,?,?,?)", (title, author, year, isbn, shelf))
        conn.commit()
        conn.close()

    def readBook(self):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("select * from book")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def searchBook(self, title='', author='', year='', isbn='', shelf=''):
        if title == 'title':
            title = ''
        if author == 'author':
            author = ''
        if year == 'year':
            year = ''
        if isbn == 'isbn':
            isbn = ''
        if shelf == 'shelf':
            shelf = ''
        if title == '' and author == '' and year == '' and isbn == '' and shelf == '':
            return self.readBook()
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("select * from book where title like ? or author=? or year=? or isbn=? or shelf=?",
                       ('%' + title + '%', '%' + author + '%', '%' + year + '%', '%' + isbn + '%', '%' + shelf + '%'))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def updateBook(self, id, title, author, year, isbn, shelf):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("update book set title=?,author=?,year=?,isbn=?,shelf=? where id=?",
                       (title, author, year, isbn, shelf, id))
        conn.commit()
        conn.close()

    def deleteBook(self, id):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("delete from book where id = ?", (id,))
        conn.commit()
        conn.close()

    def employeeCreate(self, Username, Password, name="admin", lastName="admin"):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        h = hashlib.new("sha256")
        h.update(Password.encode())
        password = h.hexdigest()
        cursor.execute("insert into employee values (NULL,?,?,?,?)", (Username, password, name, lastName))
        conn.commit()
        conn.close()

    def employeeLogin(self, Username, Password):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        h = hashlib.new("sha256")
        h.update(Password.encode())
        password = h.hexdigest()

        cursor.execute("select * from employee where userName like ? and password=?",
                       (Username, password))
        rows = cursor.fetchall()
        if len(rows) == 0:
            cursor.execute("select userName from employee where userName like ? ",
                           (Username,))
            rows = cursor.fetchall()
            if len(rows) != 0:
                conn.close()
                return "password is wrong"
            else:
                conn.close()
                return "user does not exist"
        conn.close()
        return rows

    def createUser(self, name, family):
        conn = sqlite3.Connection("library.db")
        cursor = conn.cursor()
        now = datetime.now()
        result = now + relativedelta(months=+3)
        result = result.strftime('%Y-%m-%d')
        cursor.execute("insert into user values (NULL,?,?,?)", (name, family, result))
        conn.commit()
        conn.close()

    def readUser(self):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("select * from user")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def searchUser(self, id='', name='', family='rame'):
        if id == 'id':
            id = ''
        if name == 'name':
            name = ' '
        if family == 'family':
            family = ' '
        if id == '' and name == ' ' and family == ' ':
            return self.readUser()
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("select * from user where id = ? or name like ? and family like ? ",
                       (id, '%' + name + '%', '%' + family + '%'))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def updateUser(self, id, name, family):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("update user set name=?,family=? where id=?",
                       (name, family, id))
        conn.commit()
        conn.close()

    def reSubscriptionUser(self, id):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        now = datetime.now()
        result = now + relativedelta(months=+3)
        result = result.strftime('%Y-%m-%d')
        cursor.execute("update user set expireTime=? where id=?",
                       (result, id))
        conn.commit()
        conn.close()

    # ====================================== issue ===============================
    def readIssue(self):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute(
            "select * from userBook INNER JOIN user INNER JOIN book on user.id= userBook.userId and book.id= userBook.bookId")
        rows = cursor.fetchall()
        conn.close()
        rows2 = list()
        for x in range(rows.__len__()):
            rows2.append(
                tuple((rows[x][0], rows[x][1], rows[x][5] + " " + rows[x][6], rows[x][2], rows[x][9], rows[x][3])))
        return rows2

    def searchIssue(self, user_id, book_id):
        if user_id == 'userId':
            user_id = ''
        if book_id == 'bookId':
            book_id = ' '
        if book_id == ' ' and user_id == '':
            return self.readIssue()
        else:
            conn = sqlite3.Connection("./library.db")
            cursor = conn.cursor()
            cursor.execute(
                "select * from userBook INNER JOIN user INNER JOIN book on user.id= userBook.userId and book.id= userBook.bookId where userBook.userId = ? or userBook.bookId like ? ",
                (user_id, "%" + book_id + "%"))
            rows = cursor.fetchall()
            rows2 = list()
            for x in range(rows.__len__()):
                rows2.append(
                    tuple((rows[x][0], rows[x][1], rows[x][5] + " " + rows[x][6], rows[x][2], rows[x][9], rows[x][3])))
            return rows2

    def createIssue(self, user_id, book_id):
        conn = sqlite3.Connection("library.db")
        cursor = conn.cursor()
        now = datetime.now()
        returned = 0
        cursor.execute("insert into userBook values (NULL,?,?,?)", (user_id, book_id, returned))
        conn.commit()
        conn.close()

    def updateIssue(self, id, user_id, book_id):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("update userBook set userId=?,bookId=? where id=?",
                       (user_id, book_id, id))
        conn.commit()
        conn.close()

    def returnedIssue(self, id):
        conn = sqlite3.Connection("./library.db")
        cursor = conn.cursor()
        cursor.execute("update userBook set returned=? where id=?",
                       (1, id))
        conn.commit()
        conn.close()


test = Backend()
# print(test.searchIssue("1", ""))

# conn = sqlite3.Connection("./library.db")
# cursor = conn.cursor()
# cursor.execute("select * , strftime('%Y %m %d', expireTime) from user")
# rows = cursor.fetchall()
# conn.close()
#
# print(rows)
