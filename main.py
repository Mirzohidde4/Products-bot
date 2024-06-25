import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.command import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardButton 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TOKEN
from inline import start_btn, product, url, url1, fake, dummy, korzin
from googletrans import Translator 


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
tr = Translator()


@dp.message(CommandStart())
async def smd_start(message: Message):
    user = message.from_user.full_name
    await message.answer_photo(photo='https://gdetraffic.com/img/news_124/shutterstock_1626190641.jpg',
        caption=f"Assalomu alaykum {html.bold(user)}\nOnlayn do'kon botimizga xush kelibsiz!", reply_markup=start_btn.as_markup())


@dp.callback_query(F.data == "mahsulotlar") 
async def products(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Kategoriyalar", reply_markup=product.as_markup())


@dp.callback_query(F.data.startswith("categ_"))
async def brend(call: CallbackQuery):
    action = call.data.split("_")
    br = action[1]
    btn = InlineKeyboardBuilder()

    if br == "back":
       await call.message.delete()
       await call.message.answer_photo(photo='https://gdetraffic.com/img/news_124/shutterstock_1626190641.jpg',
        caption=f"🔝 Siz asosiy menyuga qaytdingiz", reply_markup=start_btn.as_markup())
    
    elif br in set(fake):
        await call.message.delete()
        for i in url1:
            if i["category"] == br:
                tarjima = tr.translate(text=i["title"], dest='uz').text
                soz = tarjima.split()
                
                if br == "women's clothing" or br == "men's clothing":
                    change = ""
                    for f in range(3):
                        change += f"{soz[f]} "
                    btn.add(InlineKeyboardButton(text=change, callback_data=f"title_{change}"))

                elif br == 'electronics' or br == 'jewelery':
                    change = ""
                    for f in range(4):
                        change += f"{soz[f]} "
                    btn.add(InlineKeyboardButton(text=change, callback_data=f"title_{change}"))
        
        btn.add(InlineKeyboardButton(text="🔙 Back", callback_data="title_back"))
        btn.adjust(2)
        await call.message.answer("Mahsulotlar", reply_markup=btn.as_markup())            

    elif br in set(dummy):
        await call.message.delete()
        for i in url['products']:
            if i["category"] == br:
                tarjima = tr.translate(text=i["title"], dest='uz').text
                btn.add(InlineKeyboardButton(text=tarjima, callback_data=f"title_{i["title"]}"))

        btn.add(InlineKeyboardButton(text="🔙 Back", callback_data="title_back"))
        btn.adjust(2)
        await call.message.answer("Mahsulotlar", reply_markup=btn.as_markup())


@dp.callback_query(F.data.startswith("title_"))
async def get_brend(call: CallbackQuery):
    action = call.data.split("_")
    br = action[1]

    if br == "back":
        await call.message.delete()
        await call.message.answer("Kategoriyalar", reply_markup=product.as_markup())
    
    else:
        await call.message.delete()
        for j in url["products"]:
            if j["title"] == br:
                coment = tr.translate(text=j['description'], dest='uz')
                await call.message.answer_photo(photo=j['images'][0],
                    caption=f"narx: {j['price']}$\n{coment.text}", reply_markup=korzin.as_markup())


@dp.callback_query(F.data.startswith("savat_"))
async def get_brend(call: CallbackQuery):
    action = call.data.split("_")
    br = action[1]

    if br == "back":
        await call.message.delete()
        await call.message.answer("Mahsulotlar", reply_markup=product.as_markup())



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")      