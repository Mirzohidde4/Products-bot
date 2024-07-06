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
from inline import start_btn, product, url, url1, fake, dummy, korzin, savatcha, tastiqlash
from googletrans import Translator 
from datebase import Add_Db, read_db, UpdateSoni, delete_db


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

    data = await state.get_data()
    chat_id = data.get("chat_id")
    
    actions = False
    savat = InlineKeyboardBuilder()
    read = read_db()
    for i in read:
        if i[0] == chat_id:
            actions = True
            tarjima = tr.translate(text=i[1], dest='uz').text
            savat.add(InlineKeyboardButton(text=tarjima, callback_data=f"savatcham_{i[1]}"))

    if actions:
        await call.message.delete()
        savat.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="savatcham_back"))
        savat.adjust(2)        
        await call.message.answer("Sizning savatingiz", reply_markup=savat.as_markup())
    else:
        await call.answer(text="sizning savatingiz bo'sh")


@dp.callback_query(F.data.startswith('savatcham_'))
async def get_product(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    action = call.data.split("_")
    br = action[1]
    await state.update_data(
        {'gap': br}
    )

    if br == "back":
       await call.message.answer_photo(photo='https://gdetraffic.com/img/news_124/shutterstock_1626190641.jpg',
        caption=f"🔝 Siz asosiy menyuga qaytdingiz", reply_markup=start_btn.as_markup())

    data = await state.get_data()
    chat_id = data.get("chat_id")

    read = read_db()
    for i in read:
        if i[0] == chat_id and i[1] == br:
            await call.message.answer_photo(photo=i[2], caption=f"Narx: {i[4]}$\n{i[3]}", reply_markup=savatcha.as_markup())


@dp.callback_query(F.data.startswith("zakaz_"))
async def get_zakaz(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")
    br = action[1]
    data = await state.get_data()
    chat_id = data.get("chat_id")
    gap = data.get("gap")
    savat = InlineKeyboardBuilder()

    if br == "mainback":
       await call.message.delete()
       await call.message.answer_photo(photo='https://gdetraffic.com/img/news_124/shutterstock_1626190641.jpg',
        caption=f"🔝 Siz asosiy menyuga qaytdingiz", reply_markup=start_btn.as_markup())

    elif br == "back":
        await call.message.delete()
        read = read_db()
        for i in read:
            if i[0] == chat_id:
                savat.add(InlineKeyboardButton(text=i[1], callback_data=f"savatcham_{i[1]}"))
        savat.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="savatcham_back"))
        savat.adjust(2)        
        await call.message.answer("Sizning savatingiz", reply_markup=savat.as_markup())        

    elif br == "berish":
        await state.update_data(
            {'chatid': call.from_user.id, 'buy': gap}
        )
        await bot.send_message(chat_id="795303467", text=f"Foydalanuvchi {chat_id} - {gap} buyurtma berdi tasdiqlaysizmi?", reply_markup=tastiqlash.as_markup())
        await call.answer(text="Buyurtmangiz ko'rib chiqilmoqda,\ntez orada habar yuboriladi", show_alert=True)

    elif br == "ochirish":
        await call.message.delete()
        read = read_db()
        for i in read:
            if i[0] == chat_id and i[1] == gap:
                try:
                    delete_db(chat_id=chat_id, title=gap)
                except:
                    await call.answer(text="Xatolik yuz berdi")

        read1 = read_db()            
        for j in read1:
            if j[0] == chat_id:
                savat.add(InlineKeyboardButton(text=j[1], callback_data=f"savatcham_{j[1]}"))
        savat.add(InlineKeyboardButton(text="🔙 Orqaga", callback_data="savatcham_back"))
        savat.adjust(2)        
        await call.answer(text="Mahsulot savatdan o'chirildi")    
        await call.message.answer("Sizning savatingiz", reply_markup=savat.as_markup())        


@dp.callback_query(lambda c: c.data.startswith("tastiqlash_") and c.message.chat.id == 795303467)
async def Tastiqlash(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    action = call.data.split("_")
    br = action[1]
    data1 = await state.get_data()
    chatid = data1.get("chatid")
    buy = data1.get("buy")
    read = read_db()

    if chatid is None:
        await bot.send_message(call.from_user.id, "Xatolik: chatid topilmadi.")
        return
    
    if buy is None:
        await bot.send_message(call.from_user.id, "Xatolik: buy topilmadi.")
        return

    if br == "ha":    
        for i in read:
            if i[0] == chatid and i[1] == buy:
                qod = i[5]
                await bot.send_message(chat_id=f"{chatid}", text=f"{buy} - buyurtmangiz tastiqlandi qod: {qod}")

    elif br == "yoq":
        await bot.send_message(chat_id=f"{chatid}", text=f"{buy} - buyurtmangiz tastiqlanmadi, keyinroq qayta urunib ko'ring")


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
        btn.add(InlineKeyboardButton(text="🔝 Asosiy menyu", callback_data="title_mainback"))
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
        btn.add(InlineKeyboardButton(text="🔝 Asosiy menyu", callback_data="title_mainback"))
        btn.adjust(2)
        await call.message.answer("Mahsulotlar", reply_markup=btn.as_markup())


@dp.callback_query(F.data.startswith("title_"))
async def get_brend(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")
    br = action[1]

    if br == "mainback":
       await call.message.delete()
       await call.message.answer_photo(photo='https://gdetraffic.com/img/news_124/shutterstock_1626190641.jpg',
        caption=f"🔝 Siz asosiy menyuga qaytdingiz", reply_markup=start_btn.as_markup())

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
                            'price': j['price'],
                            'description': coment.text
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
                            'price': i['price'],
                            'description': coment.text
                        }
                    )     


@dp.callback_query(F.data.startswith("savat_"))
async def set_brend(call: CallbackQuery, state: FSMContext):
    action = call.data.split("_")
    br = action[1]
    btn = InlineKeyboardBuilder()

    if br == "mainback":
       await call.message.delete()
       await call.message.answer_photo(photo='https://gdetraffic.com/img/news_124/shutterstock_1626190641.jpg',
        caption=f"🔝 Siz asosiy menyuga qaytdingiz", reply_markup=start_btn.as_markup())

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

    # elif br == 'plus':
    #     data = await state.get_data()
    #     api = data.get("api")
    #     title = data.get("title")
    #     image = data.get("image")
    #     price = data.get("price")
        
    #     if soni[0] >= 50: 
    #         await call.answer(text="Mahsulot soni cheklangan", show_alert=True)
    #     else:
    #         await call.message.delete()
    #         soni[0] = soni[0] + 1
    #         if api == "dummy":
    #             for j in url["products"]:
    #                 if j["title"] == br:
    #                     coment = tr.translate(text=j['description'], dest='uz')
    #                     await call.message.answer_photo(photo=j['images'][0],
    #                         caption=f"narx: {j['price']}$\n{coment.text}", reply_markup=korzin.as_markup())
                        
    #         elif api == "fake":                
    #             for i in url1:
    #                 soz = i['title'].split()
    #                 yangi_soz = ""
    #                 for s in range(3):
    #                     yangi_soz += f"{soz[s]} " 
    #                 if yangi_soz == br:
    #                     coment = tr.translate(text=i['description'], dest='uz')
    #                     await call.message.answer_photo(photo=i['image'],
    #                         caption=f"narx: {i['price']}$\n{coment.text}", reply_markup=korzin.as_markup())            



    elif br == "qoshish":
        data = await state.get_data()
        chat_id = data.get("chat_id")
        title = data.get("title")
        image = data.get("image")
        price = data.get("price")
        description = data.get("description")

        try:
            # read = read_db()
            # print(f"\n\n{chat_id, title}\n\n")
            # for i in read: 
                # if i[0] == chat_id:
                    # print(True + "\n\n\n")
            #         # son = i[4] + 1
            #         # UpdateSoni(soni=son, chat_id=chat_id)
            #         # await call.answer("Mahsulot savatga qo'shildi")
            #         break

                # else:
            Add_Db(chat_id=chat_id, title=title, image=image, description=description, price=price)
            await call.answer("Mahsulot savatga qo'shildi")
                    # break
        except:
            await call.answer("Xatolik yuz berdi", show_alert=True)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")      
        