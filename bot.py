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
        products = types.InlineKeyboardMarkup(row_width=7)
        first_page = types.InlineKeyboardButton(text="<<", callback_data="1")
        last_page = types.InlineKeyboardButton(text=">>", callback_data=f"{str(count_pages)}")
        for i in pages.page(1):
            products.add(types.InlineKeyboardButton(text = f'{get_name(i)}', callback_data= f'{get_name(i)}'))
        if pages.page(1).has_other_pages():
            if (pages.page(2).has_next()):
                if  (pages.page(3).has_next()):
                    products.add(first_page,
                    types.InlineKeyboardButton(text=f'{page1.number}', callback_data=f'{page1.number}'),
                    types.InlineKeyboardButton(text=f'{page1.number+1}', callback_data=f'{page1.number+1}'),
                    types.InlineKeyboardButton(text=f'{page1.number+2}', callback_data=f'{page1.number+2}'),
                    types.InlineKeyboardButton(text=f'{page1.number+3}', callback_data=f'{page1.number+3}'),
                    last_page)
                    bot.send_message(message.chat.id,"Products",reply_markup=products)
                else:
                    products.add(first_page,
                    types.InlineKeyboardButton(text=f'{page1.number}', callback_data=f'{page1.number}'),
                    types.InlineKeyboardButton(text=f'{page1.number+1}', callback_data=f'{page1.number+1}'),
                    types.InlineKeyboardButton(text=f'{page1.number+2}', callback_data=f'{page1.number+2}'),
                    last_page)
                    bot.send_message(message.chat.id,"Products",reply_markup=products)
            else:
                products.add(first_page,
                types.InlineKeyboardButton(text=f'{page1.number}', callback_data=f'{page1.number}'),
                types.InlineKeyboardButton(text=f'{page1.number+1}', callback_data=f'{page1.number+1}'),
                last_page)
                bot.send_message(message.chat.id,"Products",reply_markup=products)
        else:
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
    print(call.data)
    description = types.InlineKeyboardMarkup(row_width=10)
    first_page = types.InlineKeyboardButton(text="<<", callback_data="1")
    last_page = types.InlineKeyboardButton(text=">>", callback_data=f"{str(count_pages)}")
    for t in pages.page_range:
        for q in pages.page(t):
            if call.data == str(get_name(q)):
                description.add(types.InlineKeyboardButton(text="🔙 Back", callback_data=f"{str(t)}"))
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_photo(call.message.chat.id, get_image(q),caption=f"{get_name(q)}\n{get_description(q)}\n{get_price(q)}", reply_markup=description)
                
    for c_page in pages.page_range:
        print(c_page)
        if call.data == str(c_page):
            curent_page = pages.page(c_page)
            print("fneinie,;r,prvp,rp")
            for products in curent_page:
                description.add(types.InlineKeyboardButton(text=f'{get_name(products)}', callback_data=f'{get_name(products)}'))
            try:bot.deleteChatPhoto(call.message.chat.id)
            except:...
            if curent_page.has_next() and curent_page.has_previous():
                if pages.page(c_page+1).has_next() and pages.page(c_page-1).has_previous():
                    if pages.page(c_page+2).has_next() and pages.page(c_page-2).has_previous():
                        description.add(first_page,
                        types.InlineKeyboardButton(text=f'{curent_page.number-3}', callback_data=f'{curent_page.number-3}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number-2}', callback_data=f'{curent_page.number-2}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number-1}', callback_data=f'{curent_page.number-1}'),
                        types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+1}', callback_data=f'{curent_page.number+1}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+2}', callback_data=f'{curent_page.number+2}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+3}', callback_data=f'{curent_page.number+3}'),
                        last_page)
                        try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                        except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)
                    elif pages.page(c_page+3).has_next() and pages.page(c_page-1).has_previous():
                        description.add(first_page,
                        types.InlineKeyboardButton(text=f'{curent_page.number-3}', callback_data=f'{curent_page.number-3}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number-2}', callback_data=f'{curent_page.number-2}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number-1}', callback_data=f'{curent_page.number-1}'),
                        types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+1}', callback_data=f'{curent_page.number+1}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+2}', callback_data=f'{curent_page.number+2}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+3}', callback_data=f'{curent_page.number+3}'),
                        last_page)
                        try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                        except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)
                    else:
                        description.add(first_page,
                        types.InlineKeyboardButton(text=f'{curent_page.number-2}', callback_data=f'{curent_page.number-2}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number-1}', callback_data=f'{curent_page.number-1}'),
                        types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+1}', callback_data=f'{curent_page.number+1}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+2}', callback_data=f'{curent_page.number+2}'),
                        last_page)
                        try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                        except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)
                else:
                    description.add(first_page,
                    types.InlineKeyboardButton(text=f'{curent_page.number-1}', callback_data=f'{curent_page.number-1}'),
                    types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                    types.InlineKeyboardButton(text=f'{curent_page.number+1}', callback_data=f'{curent_page.number+1}'),
                    last_page)
                    try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                    except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)
            elif curent_page.has_next():
                if (pages.page(c_page+1)).has_next():
                    if (pages.page(c_page+2).has_next()):
                        description.add(first_page,
                        types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+1}', callback_data=f'{curent_page.number+1}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+2}', callback_data=f'{curent_page.number+2}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+3}', callback_data=f'{curent_page.number+3}'),
                        last_page)
                        try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                        except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)
                    else:
                        description.add(first_page,
                        types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+1}', callback_data=f'{curent_page.number+1}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number+2}', callback_data=f'{curent_page.number+2}'),
                        last_page)
                        try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                        except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)

                else:
                    description.add(first_page,
                    types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                    types.InlineKeyboardButton(text=f'{curent_page.number+1}', callback_data=f'{curent_page.number+1}'),
                    last_page)
                    try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                    except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)
            elif curent_page.has_previous():
                if (pages.page(c_page-1)).has_previous():
                    if (pages.page(c_page-2).has_previous()):
                        description.add(first_page,
                        types.InlineKeyboardButton(text=f'{curent_page.number-3}', callback_data=f'{curent_page.number-3}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number-2}', callback_data=f'{curent_page.number-2}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number-1}', callback_data=f'{curent_page.number-1}'),
                        types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                        last_page)
                        try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                        except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)
                    else:
                        description.add(first_page,
                        types.InlineKeyboardButton(text=f'{curent_page.number-2}', callback_data=f'{curent_page.number-2}'),
                        types.InlineKeyboardButton(text=f'{curent_page.number-1}', callback_data=f'{curent_page.number-1}'),
                        types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),                       
                        last_page)
                        try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                        except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)

                else:
                    description.add(first_page,
                    types.InlineKeyboardButton(text=f'{curent_page.number-1}', callback_data=f'{curent_page.number-1}'),
                    types.InlineKeyboardButton(text=f'_{curent_page.number}_', callback_data=f'{curent_page.number}'),
                    last_page)
                    try :bot.edit_message_text(chat_id =call.message.chat.id ,message_id=call.message.message_id ,text="Product", reply_markup=description)
                    except:bot.send_message(call.message.chat.id,text="Product", reply_markup=description)

            

bot.infinity_polling()