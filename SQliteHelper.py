import sqlite3


class SQLiteHelper:
    def __init__(self, name = 'None'):
        self.conn = None
        self.cursor = None
        if name:
            self.open(name)
        
    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
            print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)
            print('Failed connecting to database ...')
    
    def create_table(self, query):
        c = self.cursor
        c.execute(query)
        # c.execute("""CREATE TABLE Dict(
        #     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     name TEXT NOT NULL,
        #     year INTEGER,
        #     admin INTEGER
        # )
        # """)
        # id có kiểu int, là khóa chính, và có chế độ tự động tăng chỉ số khi thêm user khác vào (autoincrement)
            # không cần phải dùng biến đếm !!!
        # name có kiểu text, thông thường trong mysql là varchar
            # Theo mặc định, một cột có thể giữ các giá trị NULL. Nếu bạn không muốn một cột mà có một giá trị NULL, 
            # thì bạn cần định nghĩa ràng buộc NOT NULL trên cột này, 
            # để xác định rằng bây giờ NULL là không được chấp nhận bởi cột đó.
            # Một NULL tương tự như không có dữ liệu nào, nó biểu diễn một dữ liệu không biết.
        # admin có hay là không sẽ có kiểu là bool, nhưng sqlite không có bool nên sẽ xài integer với 0 đại diện 
            # cho false và 1 đại diện cho true
    
    #INSERT & UPDATE ~ thêm, sửa dữ liệu
    def edit(self, query):
        c = self.cursor
        c.execute(query)
        self.conn.commit()
            # sau khi thay đổi phải có commit ~ cam kết

    def insert(self, eng, vie, scr):
        c = self.cursor
        c.execute("INSERT INTO DictDB (ENG, VIE, SCR) VALUES (\"%s\", \"%s\", %d)"%(eng, vie, scr))
        self.conn.commit()

    def delete(self, lang, sentence):
        c = self.cursor
        c.execute("DELETE FROM DictDB WHERE %s = \"%s\""%(lang, sentence))
        self.conn.commit()

    def deleteById(self, rowid):
        c = self.cursor
        c.execute("DELETE FROM DictDB WHERE rowid = %d"%(rowid))
        self.conn.commit()

    # LẤY DỮ LIỆU
    def select(self, query): 
        c = self.cursor
        c.execute(query)
        return c.fetchall() # fetchall sẽ trả về các giá trị đã được lấy từ truy vấn
        # lấy dữ liệu không cần commit !!!

    def selectRowIDByEngOrVie(self, lang, sentence):
        c = self.cursor
        c.execute("SELECT rowid FROM DictDB WHERE %s = \"%s\""%(lang, sentence))
        return c.fetchall()

    def select_lang_by_rowid(self, language, rowID):
        c = self.cursor
        c.execute("SELECT %s FROM DictDB WHERE rowid = \"%s\""%(language, str(rowID)))
        return c.fetchall()[0][0]

    def update_lang(self, language, new, old):
        c = self.cursor
        new = new.replace("\"", "\'\'")
        old = old.replace("\"", "\'\'")
        string = "UPDATE DictDB SET %s = \"%s\" WHERE %s = \"%s\""%(language, new, language, old)
        try:
            c.execute(string)
            self.conn.commit()
        except TypeError:
            print(string)
            
    
    def update_score(self, score, ENG):
        c = self.cursor
        string = "UPDATE DictDB SET SCR = \"%s\" WHERE ENG = \"%s\""%(str(score), ENG)
        c.execute(string)
        self.conn.commit()
    
    def get_score(self, ENG):
        c = self.cursor
        string = "SELECT SCR FROM DictDB WHERE ENG = \"%s\""%(ENG)
        c.execute(string)
        return c.fetchall()[0][0]

    def get_rowid_from_sort_score(self):
        c = self.cursor
        string = "SELECT rowid FROM DictDB ORDER BY SCR ASC"
            # ASC tăng dần
            # DESC giảm dần
        c.execute(string)
        return c.fetchall()

# test = SQLiteHelper('./test.db')
#test.create_table()
#test.edit("INSERT INTO users (name, year, admin) VALUES ('Tu', 1997, 1)")
# test.edit("UPDATE users SET name = 'leavin' WHERE name = 'Tu'")
# print(test.select('SELECT * FROM users'))