import telebot
import backend
import time
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup

#Telegram Token
bot = telebot.TeleBot("5520432534:AAEraDR4mukk_wd5_jPLN_fHCA0J5Hke5zY")

#Global Variables
menu_list = {"0":"Current Courses","1":"Completed Courses","2":"Grade","3":"Payment","4":"Donation"}

def Menu_Keyboard():
    button = InlineKeyboardMarkup()
    # for value in menu_list.items():
    button.add(InlineKeyboardButton(text="Current Courses",callback_data="Current Courses"),
                    InlineKeyboardButton(text="Completed Courses",callback_data="Completed Courses"),
                    # InlineKeyboardButton(text="Grade",callback_data="grade"),
                    # InlineKeyboardButton(text="Payment",callback_data="payment"),
                    InlineKeyboardButton(text="Donation",callback_data="Donation"))
    return button

def Current_Course_Keyboard(tele_id):
    current_course_list  = {}
    current_course_list = backend.CurrentCourse(tele_id)
    button = InlineKeyboardMarkup()
    for key,value in current_course_list.items():
        button.add(InlineKeyboardButton(text=value,
                                        callback_data="Current_Courses_lists" + value))
    button.add(InlineKeyboardButton(text="Back",callback_data="back_menu"))
    return button

def Completed_Course_Keyboard(tele_id):
    completed_course_list = {}
    completed_course_list = backend.CompletedCourse(tele_id)
    button = InlineKeyboardMarkup()
    for key,value in completed_course_list.items():
        button.add(InlineKeyboardButton(text=value,
                                        callback_data="Completed_Courses_lists" + value))
    button.add(InlineKeyboardButton(text="Back",
                                          callback_data="back_menu"))
    return button

def back_menu():
    button = InlineKeyboardMarkup()
    button.add(InlineKeyboardButton(text="back",
                                    callback_data="back_menu"))
    return button

def back_Current_Course():
    button = InlineKeyboardMarkup()
    button.add(InlineKeyboardButton(text="back",
                                    callback_data="back_current_course"))
    return button

def back_Completed_Course():
    button = InlineKeyboardMarkup()
    button.add(InlineKeyboardButton(text="back",
                                    callback_data="back_completed_course"))
    return button

#/Send Commands Methods
@bot.message_handler(commands=['start'])
def send_welcome(message):
            bot.send_message(chat_id=message.chat.id,
                        text="Enter User Name and Password \n with this format \n ihrcs-45632-13 123456 \n UserName Password")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    button = InlineKeyboardMarkup()
    button = Menu_Keyboard()
    backend.session_control(str(message.from_user.id),str(message.text))
    bot.send_message(chat_id=message.chat.id,
                        text="Here are the values of stringList",
                        reply_markup=button,
                        parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    call_data = call.data
    if call_data.startswith('Current'):
        if call_data.startswith('Current Courses'):
            button = InlineKeyboardMarkup()
            button = Current_Course_Keyboard(str(call.message.chat.id))
            bot.send_message(call.message.chat.id,"/n/n    Your Current Courses",
                        reply_markup=button,
                        parse_mode='HTML')
        if call_data.startswith('Current_Courses_lists'):
            button = InlineKeyboardMarkup()
            button = back_Current_Course()
            single_course = {}
            single_course = backend.single_current_course(str(call.data),str(call.message.chat.id))
            total_mark = single_course[-1]
            single_course.pop()
            course_name_splited = str(call.data)
            course_name = course_name_splited[21:]  + " \n \n"
            single_course_len =len(single_course)
            single_course_list = []
            if single_course_len > 1:
                for i in range(1,single_course_len,1):
                    single_course_list.append(single_course[i][1]+"-----"+single_course[i][2]+"-----"+str(single_course[i][3]).strip("\n").strip("'"))
                    tmp_result = str(single_course_list).replace(",","\n").strip("[").strip("]")
                tmp_2_result = str(tmp_result).replace("'","")
                result = tmp_2_result + " \n \n" + str(total_mark).replace("'","").strip("[").strip("]")
                bot.send_message(call.message.chat.id,
                                course_name + 
                                result,
                                reply_markup=button)
            else:
                total = "Total course mark  0% "
                bot.send_message(call.message.chat.id,
                                course_name + 
                                total,reply_markup=back_Current_Course())
    if call_data.startswith('Completed'):
        if call_data.startswith('Completed Courses'):
            button = InlineKeyboardMarkup()
            button = Completed_Course_Keyboard(str(call.message.chat.id))
            bot.send_message(call.message.chat.id,"/n/n    Your Completed Courses",
                        reply_markup=button,
                        parse_mode='HTML')
        if call_data.startswith('Completed_Courses_lists'):
            button = InlineKeyboardMarkup()
            button = back_Completed_Course()
            single_course = {}
            single_course = backend.single_completed_course(str(call.data),str(call.message.chat.id))
            total_mark = single_course[-1]
            single_course.pop()
            course_name_splited = str(call.data)
            course_name = course_name_splited[23:] + " \n \n"
            single_course_len =len(single_course)
            single_course_list = []
            if single_course_len > 1:
                for i in range(1,single_course_len,1):
                    single_course_list.append(single_course[i][1]+"-----"+single_course[i][2]+"-----"+str(single_course[i][3]).strip("\n").strip("'"))
                    tmp_result = str(single_course_list).replace(",","\n").strip("[").strip("]")
                tmp_2_result = str(tmp_result).replace("'","")
                result = tmp_2_result + " \n \n" + str(total_mark).replace("'","").strip("[").strip("]")
                bot.send_message(call.message.chat.id,
                                course_name +
                                result,
                                reply_markup=button)
            else:
                total = "Total course mark  0% "
                bot.send_message(call.message.chat.id,
                                course_name + 
                                total,reply_markup=back_Completed_Course())
    if call_data == "Donation":
        bot.send_message(call.message.chat.id,"cbebirr,telebirr,hellocash : `0967229563` ",
                     reply_markup=back_menu(),
                     parse_mode='HTML')
    if call_data == "back_menu":
        bot.send_message(call.message.chat.id,"Here are the values of stringList",
                     reply_markup=Menu_Keyboard(),
                     parse_mode='HTML')
    if call_data == "back_current_course":
        button = InlineKeyboardMarkup()
        button = Current_Course_Keyboard(call.message.chat.id)
        bot.send_message(call.message.chat.id,"Here are the values of stringList",
                     reply_markup=button,
                     parse_mode='HTML')
    if call_data == "back_completed_course":
        button = InlineKeyboardMarkup()
        button = Completed_Course_Keyboard(call.message.chat.id)
        bot.send_message(call.message.chat.id,"Here are the values of stringList",
                     reply_markup=button,
                     parse_mode='HTML')

while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)