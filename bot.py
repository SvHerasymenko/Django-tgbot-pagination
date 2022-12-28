import os,time,math,telebot
from loguru import logger
from telebot import types
from django.core.paginator import Paginator
from dborm import get_id,get_name,get_price,get_description,count_products,get_image


logger.add("bot/bot_logs/bot.log", format="{time} {level} {message}", rotation="10MB", compression="zip")

get_id = get_id()
count_products = count_products()

bot = telebot.TeleBot('5656327921:AAGbBfmdkv23Px777q0ES4-7AcQDyCYStSE')

def numer_buttons():
    page = []
    for p in pages.page_range:
        page.append(p)
    return page
count_pages = math.ceil(count_products/10)
pages = Paginator(get_id,10)
page1 = pages.page(1)
    
    

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_product = types.KeyboardButton("Products")
    markup.add(button_product)
    bot.send_message(message.chat.id, f'{message.from_user.first_name}', reply_markup = markup)
    logger.info("function (start) is worked!")

@bot.message_handler(content_types=['text'])
@logger.catch
def productslist(message):
    if message.text == 'Products':
        products = types.InlineKeyboardMarkup()
        first_page = types.InlineKeyboardButton(text="<<", callback_data="page 1")
        last_page = types.InlineKeyboardButton(text=">>", callback_data="page " + str(count_pages))
        for i in pages.page(1):
            products.add(types.InlineKeyboardButton(text = f'{get_name(i)}', callback_data= f'{get_name(i)}'))
        products.add(first_page,
        types.InlineKeyboardButton(text=f'{pages.page(current_page).number}', callback_data=f'{pages.page(current_page).number}'),
        last_page)
        bot.send_message(message.chat.id,"Products",reply_markup=products)
        logger.info("function productlist worked")

    elif message.text:
        bot.delete_message(message.chat.id, message.id)
        logger.info("function productslist worked!")
    else:
        logger.error("!ERROR! function productlist not worked !")

@bot.callback_query_handler(func=lambda call : True)
@logger.catch
def product_description(call):
    global count_pages
    print(call.message)
    description = types.InlineKeyboardMarkup(row_width=7)
    first_page = types.InlineKeyboardButton(text="<<", callback_data="page 1")
    last_page = types.InlineKeyboardButton(text=">>", callback_data=f"page " + str(count_pages))
    for q in get_id:
        if call.data == str(get_name(q)):
            description.add(types.InlineKeyboardButton(text="🔙 Back", callback_data="page "+str(q)))
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_photo(call.message.chat.id, get_image(q),caption=f"{get_name(q)}\n{get_description(q)}\n{get_price(q)}", reply_markup=description)

bot.infinity_polling()