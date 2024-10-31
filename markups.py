from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#global buttons
button_exit = KeyboardButton(text='Вернуться в главное меню')
button_back = KeyboardButton(text='Назад')

#main menu
#buttons
button_get = KeyboardButton(text='Получить номер предписания')
button_pos = KeyboardButton(text='Заполнить расстановку')
button_inf = KeyboardButton(text='Справка')

menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [button_get],  # Создаем список, содержащий одну кнопку
    [button_pos],  # Создаем список, содержащий вторую кнопку
    [button_inf]   # Создаем список, содержащий третью кнопку
])

#pos menu
button_pro = KeyboardButton(text='Производственный статус')
button_nopro = KeyboardButton(text='Непроизводственный статус')

pos_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [button_pro],
    [button_nopro],
    [button_back]
])

#pro_menu - начало заполнения производственного статуса
button_yestarday = KeyboardButton(text='Заполнить как за предыдущий день')
button_select_obj = KeyboardButton(text='Выбрать объект')

pro_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [button_yestarday],
    [button_select_obj],
    [button_back]
])

#viborii_menu
button_igi = KeyboardButton(text='ИГИ')
button_igdi = KeyboardButton(text='ИГДИ')
button_igmi = KeyboardButton(text='ИГМИ')
button_iei = KeyboardButton(text='ИЭИ')

viborii_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [button_igi],
    [button_igdi],
    [button_igmi],
    [button_iei],
    [button_back]
])

#nopro_menu - начало заполнения непроизводственного статуса
button_otpusk = KeyboardButton(text='Отпуск')
button_bolnica = KeyboardButton(text='Больничный')
button_learning = KeyboardButton(text='Обучение')
button_office = KeyboardButton(text='Работа в офисе')

nopro_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [button_yestarday],
    [button_otpusk],
    [button_bolnica],
    [button_learning],
    [button_office],
    [button_back]
])




#admin menu
button_delete = KeyboardButton(text='Удалить номер предписания')
button_log = KeyboardButton(text='Журнал логов')
button_db = KeyboardButton(text='Скачать БД')
button_del = KeyboardButton(text='Удалить пользователя')
button_null = KeyboardButton(text='Сбросить номер предписания')
button_reg = KeyboardButton(text='Логи регистрации')
button_generate = KeyboardButton(text='Сгенерировать код')
button_check = KeyboardButton(text='Посмотреть код')

#inline_buttons
ikb_delete = InlineKeyboardButton(text='Подтвердить',callback_data='Подтвердить')
ikb_cancel = InlineKeyboardButton(text='Отмена',callback_data='Отмена')

ikb_remove = InlineKeyboardButton(text='Удалить пользователя',callback_data='Удалить пользователя')

#menus setup
admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [button_delete, button_del],
    [button_db, button_log],
    [button_check, button_reg],
    [button_generate],
    [button_exit]
])

#ikb_menu = InlineKeyboardMarkup(row_width= 2).add(ikb_cancel,ikb_delete)
ikb_menu = InlineKeyboardMarkup(row_width= 2, inline_keyboard=[
    [ikb_cancel, ikb_delete]  # Создаем список, содержащий две кнопки
])
#ikb_remove_user = InlineKeyboardMarkup(row_width= 2).add(ikb_cancel,ikb_remove)
ikb_remove_user = InlineKeyboardMarkup(row_width= 2, inline_keyboard=[
    [ikb_cancel, ikb_remove]  # Создаем список, содержащий две кнопки
])