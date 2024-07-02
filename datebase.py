import sqlite3
from sqlite3 import Error


def create_table():
    try:
        connection= sqlite3.connect('sqlite3.db')

        table = """ CREATE TABLE Products (
                    chat_id BIGINT NOT NULL ,
                    title TEXT NOT NULL,
                    image TEXT NOT NULL,
                    description TEXT NOT NULL,
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
            

def Add_Db(chat_id, title, image, description, price, soni=1):
    try:
        with sqlite3.connect("sqlite3.db") as connection:
            cursor = connection.cursor()
            
            table = '''
                INSERT INTO Products(chat_id, title, image, description, price, soni) VALUES( ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(table, (chat_id, title, image, description, price, soni))
            connection.commit()
            print("SQLite tablega qo'shildi")
            cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("Sqlite ish foalyatini tugatdi")                         
# Add_Db(432423, 'gtgtr', 'https://avatars.mds.yandex.net/i?id=b535fd93db7d3b37ec3ff6c027245af8273a225747e8cdbf-6496990-images-thumbs&n=13', '32')

def read_db():
    try:
        with sqlite3.connect("sqlite3.db") as sqliteconnection:
            cursor = sqliteconnection.cursor()
            sql_query = """
                SELECT * FROM Products 
            """
        
            cursor.execute(sql_query) 
            A = cursor.fetchall()
            print("table oqildi")
            return A

    except Error as error:
        print("xatolik:", error)
    finally:
        if sqliteconnection:
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
            cur.close()

    except sqlite3.Error as err:
        print(f"Yangilashda xatolik: {err}")
    finally:
        if con:
            con.close()
            print("Sqlite ish foalyatini tugatdi")    


def delete_db(chat_id, title):
    try:
        with sqlite3.connect('sqlite3.db') as connection:
            cursor = connection.cursor()

            query = '''
                DELETE FROM Products WHERE (chat_id, title) = (?, ?)
            '''
            cursor.execute(query, (chat_id, title))
            connection.commit()
            print("mahsulot o'chirildi")
            cursor.close()
    
    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if connection:
            connection.close()
            print("Sqlite ish foalyatini tugatdi")
# delete_db(795303467, "Kiwi")