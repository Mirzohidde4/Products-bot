import asyncio, logging
from aiogram import Bot, Dispatcher, F, html
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.command import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton 
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TOKEN
from inline import start_btn, product, url, url1, fake, dummy, korzin
from googletrans import Translator 
from datebase import Add_Db, read_db, UpdateSoni


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
tr = Translator()


@dp.message(CommandStart())
async def smd_start(message: Message, state: FSMContext):
    user = message.from_user.full_name
    chat_id = message.chat.id
    await state.update_data(
        {'chat_id': chat_id}
    )
    await message.answer_photo(photo='https://gdetraffic.com/img/news_124/shutterstock_1626190641.jpg',
        caption=f"Assalomu alaykum {html.bold(user)}\nOnlayn do'kon botimizga xush kelibsiz!", reply_markup=start_btn.as_markup())


@dp.callback_query(F.data == "savatcha") 
async def products(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    chat_id = data.get("chat_id")
    
    savat = InlineKeyboardBuilder()
    read = read_db()
    for i in read:
        if i[0] == chat_id:
            savat.add(InlineKeyboardButton(text=i[1], callback_data=f"savatcha_{i[1]}"))
    savat.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="savatcha_back"))
    savat.adjust(2)        
    await call.message.answer("Sizning savatingiz", reply_markup=savat.as_markup())


@dp.callback_query(F.data == "mahsulotlar") 
async def products(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Kategoriyalar", reply_markup=product.as_markup())


@dp.callback_query(F.data.startswith("categ_"))
async def brend(call: CallbackQuery, state: FSMContext):
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
                back = i['title'].split()
                change = ""
                calback = ""
                for f in range(3):
                    change += f"{soz[f]} "
                    calback += f"{back[f]} "
                btn.add(InlineKeyboardButton(text=change, callback_data=f"title_{calback}"))
    
        await state.update_data(
            {
                'br': br,
                'api': 'fake'
            }
        )
        btn.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="title_back"))
        btn.adjust(2)
        await call.message.answer("Mahsulotlar", reply_markup=btn.as_markup())            

    elif br in set(dummy):
        await call.message.delete()
        for i in url['products']:
            if i["category"] == br:
                tarjima = tr.translate(text=i["title"], dest='uz').text
                btn.add(InlineKeyboardButton(text=tarjima, callback_data=f"title_{i["title"]}"))

        await state.update_data(
            {
                'br': br,
                'api': 'dummy'
            }
        )
        btn.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="title_back"))
        btn.adjust(2)
        await call.message.answer("Mahsulotlar", reply_markup=btn.as_markup())


@dp.callback_query(F.data.startswith("title_"))
async def get_brend(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")
    br = action[1]

    if br == "back":
        await call.message.delete()
        await call.message.answer("Kategoriyalar", reply_markup=product.as_markup())
    
    else:
        await call.message.delete()
        data = await state.get_data()
        api = data.get("api")

        if api == "dummy":
            for j in url["products"]:
                if j["title"] == br:
                    coment = tr.translate(text=j['description'], dest='uz')
                    await call.message.answer_photo(photo=j['images'][0],
                        caption=f"narx: {j['price']}$\n{coment.text}", reply_markup=korzin.as_markup())

                    await state.update_data(
                        {
                            'title': j['title'],
                            'image': j['images'][0],
                            'price': j['price']
                        }
                    )           

        elif api == "fake":                
            for i in url1:
                soz = i['title'].split()
                yangi_soz = ""
                for s in range(3):
                    yangi_soz += f"{soz[s]} " 
                if yangi_soz == br:
                    coment = tr.translate(text=i['description'], dest='uz')
                    await call.message.answer_photo(photo=i['image'],
                        caption=f"narx: {i['price']}$\n{coment.text}", reply_markup=korzin.as_markup())
                    
                    await state.update_data(
                        {
                            'title': yangi_soz,
                            'image': i['image'],
                            'price': i['price']
                        }
                    )     


@dp.callback_query(F.data.startswith("savat_"))
async def get_brend(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")
    br = action[1]
    btn = InlineKeyboardBuilder()

    if br == "back":
        await call.message.delete()
        data = await state.get_data()
        api = data.get("api")
        gap = data.get("br")

        if api == "dummy":
            for i in url['products']:
                if i["category"] == gap:
                    tarjima = tr.translate(text=i["title"], dest='uz').text
                    btn.add(InlineKeyboardButton(text=tarjima, callback_data=f"title_{i["title"]}"))
            btn.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="title_back"))
            btn.adjust(2)
            await call.message.answer("Mahsulotlar", reply_markup=btn.as_markup())

        elif api == "fake":
            for i in url1:
                if i["category"] == gap:
                    tarjima = tr.translate(text=i["title"], dest='uz').text
                    soz = tarjima.split()
                    back = i['title'].split()
                    change = ""
                    calback = ""
                    for f in range(3):
                        change += f"{soz[f]} "
                        calback += f"{back[f]} "
                    btn.add(InlineKeyboardButton(text=change, callback_data=f"title_{calback}"))
    
            btn.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="title_back"))
            btn.adjust(2)
            await call.message.answer("Mahsulotlar", reply_markup=btn.as_markup())   


    elif br == "qoshish":
        data = await state.get_data()
        chat_id = data.get("chat_id")
        title = data.get("title")
        image = data.get("image")
        price = data.get("price")

        try:
            read = read_db()
            print(f"\n\n{chat_id, title}\n\n")
            for i in read: 
                if (str(i[0]) == str(chat_id)):
                    print(True)
                    # son = i[4] + 1
                    # UpdateSoni(soni=son, chat_id=chat_id)
                    # await call.answer("Mahsulot savatga qo'shildi")
                    break

                else:
                    Add_Db(chat_id=chat_id, title=title, image=image, price=price)
                    await call.answer("Mahsulot savatga qo'shildi")
                    break
        except:
            await call.answer("Xatolik yuz berdi", show_alert=True)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")      