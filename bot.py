#importing the librarys
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import os,time,math,asyncio,django
from loguru import logger
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg_store.settings")
django.setup()
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from dborm import get_id,get_name,get_price,get_description,count_products,get_image

#connect logging to the project
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

logger.add("bot/logs/bot.log", format="{time} {level} {message}", rotation="10MB", compression="zip")

get_id = get_id()
count_products = count_products()

#connecting the tg bot token
bot = AsyncTeleBot('')

#creating lists for pagination
count_pages = math.ceil(count_products/10)
pages = Paginator(get_id,10)
page1 = pages.page(1)

#an initial function with the creation of built-in buttons
@bot.message_handler(commands = ['start'])
async def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_product = types.KeyboardButton("Products")
    markup.add(button_product)
    if await bot.send_message(message.chat.id, f'{message.from_user.first_name}', reply_markup = markup):
        logger.info("function (start) is worked!")
    else:
        logger.error("Bot didn`t command start")
        
#A function that displays an image of the product and its description       
@bot.message_handler(content_types=['text'])
@logger.catch
async def productslist(message):
    if message.text == 'Products':
        pagelist =[]
        productlist = []
        first_page = types.InlineKeyboardButton(text="<<", callback_data="1")
        last_page = types.InlineKeyboardButton(text=">>", callback_data=f"{str(count_pages)}")
        for i in  page1:
            pl = []
            pl.append(types.InlineKeyboardButton(text = f'{get_name(i)}', callback_data= f'{get_name(i)}'))
            productlist.append([*pl])
        for p in pages.page_range:
                if 1< p <=3:
                    pagelist.append(types.InlineKeyboardButton(text=f'{p}', callback_data=f'{p}'))
        products=types.InlineKeyboardMarkup([*productlist,[first_page,types.InlineKeyboardButton(text="_1_",callback_data="1"),*pagelist,last_page]])
        await bot.send_message(message.chat.id, text="Products:", reply_markup=products)
        delete_message = await bot.send_message(message.chat.id, text=".",reply_markup=types.ReplyKeyboardRemove(True))
        await bot.delete_message(message.chat.id, delete_message.id)
        logger.info("bot send productskist")
    elif message.text:
        await bot.delete_message(message.chat.id, message.id)
        logger.info("message delete")
    else:
        logger.error("!ERROR! function productlist not worked !")

#Pagination
@bot.callback_query_handler(func=lambda call : True)
@logger.catch
async def product_description(call):
    description = types.InlineKeyboardMarkup()
    first_page = types.InlineKeyboardButton(text="<<", callback_data="1")
    last_page = types.InlineKeyboardButton(text=">>", callback_data=f"{str(count_pages)}")
    pagelist =[]
    productlist = []
    for t in pages.page_range:
        for q in pages.page(t):
            if call.data == str(get_name(q)):
                description.add(types.InlineKeyboardButton(text="🔙 Back", callback_data=f"{str(t)}"))
                if get_image(q) == '':
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f"{get_name(q)}\n{get_description(q)}\n{get_price(q)}", reply_markup=description)
                    logger.info("function product_description worked! | bot edit message")
                else:
                    await bot.delete_message(call.message.chat.id, call.message.id)
                    logger.info("bot delete message")
                    await bot.send_photo(call.message.chat.id, open(f'{get_image(q)}', 'rb'),caption=f"{get_name(q)}\n{get_description(q)}\n{get_price(q)}", reply_markup=description)
                    logger.info("function product_description worked! | bot send message")

    for c_page in pages.page_range:
        if call.data == str(c_page):
            curent_page = pages.page(c_page)  
            for i in curent_page:
                pl = []
                pl.append(types.InlineKeyboardButton(text = f'{get_name(i)}', callback_data= f'{get_name(i)}'))
                productlist.append([*pl])
            for p in pages.page_range:
                if c_page == p:
                    pagelist.append(types.InlineKeyboardButton(text=f'_{p}_', callback_data=f'{p}'))
                if p >= c_page-2 and p<= c_page+2 and c_page !=p:   
                    pagelist.append(types.InlineKeyboardButton(text=f'{p}', callback_data=f'{p}'))
            products1=types.InlineKeyboardMarkup([*productlist,[first_page,*pagelist,last_page]])
            if call.message.photo == None:
                try:await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Products:", reply_markup=products1)
                except:await bot.send_message(call.message.chat.id, text="Products:", reply_markup=products1)
            else:
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                try:await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Products:", reply_markup=products1)
                except:await bot.send_message(call.message.chat.id, text="Products:", reply_markup=products1)
#start tg bot work
while True:
    try:
        logger.info("start bot")
        asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))
    except KeyboardInterrupt:
        logger.info("stopping the application")
        exit()
    except Exception:
        logger.info("Error")
        time.sleep(5)
