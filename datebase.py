import sqlite3
from sqlite3 import Error


def create_table():
    try:
        connection= sqlite3.connect('sqlite3.db')

        table = """ CREATE TABLE Products (
                    chat_id BIGINT NOT NULL ,
                    title TEXT NOT NULL,
                    image TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    soni INTEGER NOT NULL
                ); """
        cursor = connection.cursor()
        print("databaza yaratildi")
        cursor.execute(table)
        cursor.close()
    
    except Error as error:
        print("hatolik", error)
    finally:
        if connection:
            connection.close()    
            print("sqlite o'chdi")
# create_table()
            

def Add_Db(chat_id, title, image, price, soni=1):
    try:
        connection = sqlite3.connect('sqlite3.db')
        cursor = connection.cursor()
        
        table = '''
            INSERT INTO Products(chat_id, title, image, price, soni) VALUES( ?, ?, ?, ?, ?)
        '''
        cursor.execute(table, (chat_id, title, image, price, soni))
        connection.commit()
        print("SQLite table saqlandi")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("Sqlite ish foalyatini tugatdi")                        


def read_db():
    try:
        sqliteconnection = sqlite3.connect("sqlite3.db")
        sql_query = """
            SELECT * FROM Products 
        """
    
        cursor = sqliteconnection.cursor()
        cursor.execute(sql_query) 
        A = cursor.fetchall()
        return A

    except Error as error:
        print("xatolik", error)
    finally:
        if sqliteconnection:
            cursor.close()
            sqliteconnection.close()
            print("sqlite faoliyatini tugatdi")
# read_db()            


def UpdateSoni(soni, chat_id):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE Products SET soni = ? WHERE chat_id = ?", (soni, chat_id)
            )
            con.commit()
            print("mahsulot soni yangilandi")
    except sqlite3.Error as err:
        print(f"Yangilashda xatolik: {err}")
