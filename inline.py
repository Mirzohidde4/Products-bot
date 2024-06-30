from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from googletrans import Translator 
import requests
tr = Translator()


main_btn = {
   '🛒 Savat': "savatcha",
   "🛍 Mahsulotlar": "mahsulotlar"
}
start_btn = InlineKeyboardBuilder()
for i, j in main_btn.items():
    start_btn.add(InlineKeyboardButton(text=i, callback_data=j))
start_btn.add(InlineKeyboardButton(text="👤 Admin", url="https://t.me/xudoybergan0v"))
start_btn.adjust(2)
 

dummy = []
fake = []
products = []

url = requests.get('https://dummyjson.com/products').json() 
for m in url['products']:
    products.append(m['category'])
    dummy.append(m['category'])

url1 = requests.get('https://fakestoreapi.com/products').json()
for n in url1:
    products.append(n['category'])
    fake.append(n['category'])


sorted_products = sorted(set(products))
kategoriyalar = []
for kategoriya in sorted_products:   
    tarjima = tr.translate(text=kategoriya, dest='uz')
    kategoriyalar.append(tarjima.text)

product = InlineKeyboardBuilder()
for mahsulot in range(len(sorted_products)):
    product.add(InlineKeyboardButton(text=kategoriyalar[mahsulot], callback_data=f"categ_{sorted_products[mahsulot]}"))
product.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="categ_back"))
product.adjust(2)


korzin = InlineKeyboardBuilder()
korzin.add(InlineKeyboardButton(text="➕ Savatga qo`shish", callback_data="savat_qoshish"))
korzin.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="savat_back"))
korzin.adjust(2)