import requests
from pprint import pprint
from googletrans import Translator
tr = Translator()
import sqlite3
from sqlite3 import Error


dummy = []
fake = []
products = []
trans = []

# url = requests.get('https://dummyjson.com/products').json() 
# for m in url['products']:
#     a = tr.translate(text=m['title'], dest='uz')
#     trans.append(a.text)
#     products.append(m['category'])
#     dummy.append(m['category'])

# url1 = requests.get('https://fakestoreapi.com/products').json()
# for n in url1:
    # a = tr.translate(text=n['title'], dest='uz')
    # trans.append(a.text)
    # b = tr.translate(text=n['category'], dest='uz')
    # fake.append(n['category'])
    # products.append(n['category'])

# # sorted_products = sorted(set(products))    
# pprint(set(fake))
# pprint(trans)


    # soz = n['title'].split()
    # # print(soz)
    # yangi_soz = ""
    # for s in range(3):
    #     yangi_soz += f"{soz[s]} "
    # print(yangi_soz)





# ss = 'men sen ven gen'
# sss = ss.split()
# dd = ""
# for f in range(3):
#     dd += f"{sss[f]} "
# print(dd)



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

# for i in read_db():
#     print(i['title'])