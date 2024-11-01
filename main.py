# from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile, CallbackQuery
from db import database
import markups as markups
from numb_generator import increment_counter
import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import random
import string
import re

admin_ids = [977050266, 1849857447, 81061749]


# func to save numb
def save(x):
    f = open('log.txt', 'w+')
    f.write(x)
    f.close()

def check_six_digit_number(message):
  """
  Проверяет, содержит ли сообщение шестизначное число.

  Args:
    message: Текст входящего сообщения.

  Returns:
    Шестизначное число из сообщения, если оно найдено, иначе 0.
  """
  match = re.search(r'\b\d{6}\b', message)  # Ищем шестизначное число, окруженное границами слов
  if match:
    return int(match.group(0))  # Преобразуем найденное число в целое
  else:
    return 0  # Возвращаем 0, если число не найдено

# main bot token
token = '7636235626:AAGYrgmpGiILdHavPFDvL2yp4_a_UlIXCRs'
bot = Bot(token=token)

def generate_key():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(6))
    f = open('invite_code.txt', 'w+')
    f.write(result_str)
    f.close

global user_key

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# user database
db = database('database.db')

# Router
start_router = Router()

# generate nubmer predpisaniya
counter = increment_counter()


# class
class idk(StatesGroup):
    user_id = State()
    reg_login = State()
    reg_answ = State()
    bot_use = State()
    bot_pos = State()
    bot_pos_pro = State()
    bot_pos_nopro = State()
    bot_admin = State()
    admin_panel = State()
    admin_delete_user = State()


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    # если юзера нет в бд то запрашиваем пароль (переходим состояние reg_login)
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        db.set_tgtag(message.from_user.id, message.from_user.username)

        str_msg = [
            '<b>Привет</b>, это бот который выдает номер предписания.',
            'Чтобы начать, введите <b>ключ доступа</b>',
        ]
        await state.set_state(idk.reg_login)
        await bot.send_message(message.from_user.id, text='\n'.join(str_msg), parse_mode=ParseMode.HTML)
    # если юзер есть в бд
    else:
        #если регистрация не завершена
        if db.get_signup(message.from_user.id) == "setname":
            str_msg = [
                'Чтобы начать, введите <b>ключ доступа</b>',
            ]
            await state.set_state(idk.reg_login)
            await bot.send_message(message.from_user.id, text='\n'.join(str_msg), parse_mode=ParseMode.HTML)
        else:
            await state.set_state(idk.bot_use)
            await bot.send_message(message.from_user.id, "<b>Вы уже зарегестрированы!</b>", parse_mode=ParseMode.HTML)
            await bot.send_message(message.from_user.id, '<b>Главное меню</b>',
                                   parse_mode=ParseMode.HTML, reply_markup=markups.menu)


# user and reg log
file_l = open('user_log.txt')
file_r = open('reg_log.txt')

# идиотский кастыль
file = open('log.txt')
get_number = file.read()

counter.set_value(int(get_number))


@start_router.message(idk.reg_login)
async def bot_message(message: Message, state: FSMContext):
    if message.chat.type == 'private':
        if db.get_signup(message.from_user.id) == "setname" and not (
                'Справка' in message.text or 'Получить номер предписания' in message.text or '@' in message.text or "/" in message.text):
            user_key = message.text
            file_k = open('invite_code.txt')
            key = file_k.read()
            if user_key == key:
                await bot.send_message(message.from_user.id,
                                       '<b>Отлично</b>, теперь введите <b>ФИО</b>, в формате <b>Иванов Иван Иванович</b>',
                                       parse_mode=ParseMode.HTML)
                await state.set_state(idk.reg_answ)
            else:
                await bot.send_message(message.from_user.id, '<b>Извините, но у вас нет доступа к боту ;(</b>',
                                       parse_mode=ParseMode.HTML)
        elif (
                'Справка' in message.text or 'Получить номер предписания' in message.text or '@' in message.text or "/" in message.text) and db.get_signup(
                message.from_user.id) == "setname":
            await bot.send_message(message.from_user.id, "<b>Извините, но у вас нет доступа к боту ;(</b>",
                                   parse_mode=ParseMode.HTML)

@start_router.message(idk.bot_use)
async def bot_message(message: Message, state: FSMContext):
        if message.text == 'Получить номер предписания' and db.get_signup(message.from_user.id) == "done":
            answer = "Ваш номер предписания: №" + str(counter.new_value())
            save(str(counter.get_value()))
            file_l = open('user_log.txt', "a+", encoding="utf-8")
            file_l.write('Номер:' + str(counter.get_value()) + '  ' + 'Взял:' + db.get_name(
                message.from_user.id) + '  ' + 'Время:' + str(
                datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")) + '\n')
            file_l.close()
            await bot.send_message(message.from_user.id, answer)

        if message.text == 'Справка' and db.get_signup(message.from_user.id) == "done":
            text = [
                '<b>1)</b> Формат предписания по ТК за ИИ:',
                'Номер предписания/Обществ Группа/Номер Договора/Филиал/ГОД-У или О',
                '<i>Пример: 1/ВО/049/КРЯ/2022-У.</i>',
                '',
                '<b>2)</b> Для получения нового номера предписания нажмите кнопку <b>«Получить номер предписания»</b>',
            ]
            await bot.send_message(message.from_user.id, text='\n'.join(text), parse_mode=ParseMode.HTML)

        if message.text == "Заполнить расстановку":
            await state.set_state(idk.bot_pos)
            await bot.send_message(message.from_user.id, "<b>Меню расстановки:</b>", parse_mode=ParseMode.HTML,
                                   reply_markup=markups.pos_menu)

        if message.text == "/restart":
            await bot.send_message(message.from_user.id, "<b>Главное меню:</b>", parse_mode=ParseMode.HTML,
                                   reply_markup=markups.menu)

        if message.text == 'admin':
            if message.from_user.id in admin_ids:
                await bot.send_message(message.from_user.id, "Привет админ!")
                await bot.send_message(message.from_user.id, "<b>Выберите действие:</b>", parse_mode=ParseMode.HTML,
                                       reply_markup=markups.admin_menu)
                await state.set_state(idk.admin_panel)  # Переход в состояние админа
            else:
                await bot.send_message(message.from_user.id, "Недостаточно прав =(")
                await bot.send_message(message.from_user.id, "<b>Главное меню:</b>", parse_mode=ParseMode.HTML,
                                       reply_markup=markups.menu)
                await state.set_state(idk.bot_use)  # Переход в состояние пользователя

@start_router.message(idk.bot_pos)
async def make_choice_bot_pos_menu(message: Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.from_user.id, "<b>Главное меню:</b>", parse_mode=ParseMode.HTML,
                               reply_markup=markups.menu)

        await state.set_state(idk.bot_use)
    if message.text == "Производственный статус":
        await bot.send_message(message.from_user.id, "<b>Производственный статус:</b>", parse_mode=ParseMode.HTML,
                               reply_markup=markups.pro_menu)
        await state.update_data(bot_pos="Производственный")
        await state.set_state(idk.bot_pos_pro)

    if message.text == "Непроизводственный статус":
        await bot.send_message(message.from_user.id, "<b>Непроизводственный статус:</b>", parse_mode=ParseMode.HTML,
                               reply_markup=markups.nopro_menu)
        await state.update_data(bot_pos="Непроизводственный")
        await state.set_state(idk.bot_pos_nopro)


@start_router.message(idk.bot_pos_pro)
async def make_choice_bot_pos_pro_menu(message: Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.from_user.id, "<b>Меню расстановки:</b>", parse_mode=ParseMode.HTML,
                               reply_markup=markups.pos_menu)
        await state.set_state(idk.bot_pos)

@start_router.message(idk.bot_pos_nopro)
async def make_choice_bot_pos_nopro_menu(message: Message, state: FSMContext):
    if message.text == "Назад":
        await bot.send_message(message.from_user.id, "<b>Меню расстановки:</b>", parse_mode=ParseMode.HTML,
                               reply_markup=markups.pos_menu)
        await state.set_state(idk.bot_pos)



@start_router.message(idk.admin_panel)
async def admin_panel(message: Message, state: FSMContext):

        if message.text == 'Удалить номер предписания' and db.get_signup(
                message.from_user.id) == "done" and counter.get_value() > 1:
            counter.delete_value()
            save(str(counter.get_value()))
            file_l = open('user_log.txt', "a+", encoding="utf-8")
            file_l.write('Номер:' + str(counter.get_value() + 1) + '  ' + 'Удалил:' + db.get_name(
                message.from_user.id) + '  ' + 'Время:' + str(
                datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")) + '\n')
            file_l.close()
            await bot.send_message(message.from_user.id,
                                   "Номер предписания удалён, теперь <b>№" + str(counter.get_value()) + "</b>",
                                   parse_mode=ParseMode.HTML)
        elif counter.get_value() == 1 and message.text == 'Удалить номер предписания':
            warning = [
                'Удалить номер предписания невозможно',
                '',
                'Ваш номер предписания: <b>№1</b>',

            ]
            await bot.send_message(message.from_user.id, text='\n'.join(warning), parse_mode=ParseMode.HTML)

        if message.text == "Журнал логов":
            l_u = FSInputFile('user_log.txt')
            await bot.send_document(message.from_user.id, l_u)

        if message.text == "Логи регистрации":
            r_u = FSInputFile('reg_log.txt')
            await bot.send_document(message.from_user.id, r_u)

        if message.text == "Скачать БД":
            db_p = FSInputFile('database.db')
            await bot.send_document(message.from_user.id, db_p)

        # if message.text == "Сбросить номер предписания":
        #     await bot.send_message(message.from_user.id, "<b>Сбросить номер предписания?</b>",
        #                            parse_mode=ParseMode.HTML, reply_markup=markups.ikb_menu)

        if message.text == "Удалить пользователя":
            await bot.send_message(message.from_user.id, "<b>Введите user_id пользователя (из базы данных):</b>",
                                   parse_mode=ParseMode.HTML)
            await state.set_state(idk.user_id)

        if message.text == "Сгенерировать код" and (
                message.from_user.id == 977050266 or message.from_user.id == 1849857447 or message.from_user.id == 81061749):
            generate_key()
            file_k = open('invite_code.txt')
            key = file_k.read()
            await bot.send_message(message.from_user.id, "<b> Сгенерированный код приглашения:</b>" + " " + str(key),
                                   parse_mode=ParseMode.HTML, reply_markup=markups.admin_menu)

        if message.text == "Посмотреть код" and (
                message.from_user.id == 977050266 or message.from_user.id == 1849857447 or message.from_user.id == 81061749):
            file_k = open('invite_code.txt')
            key = file_k.read()
            await bot.send_message(message.from_user.id, "<b> Код приглашения:</b>" + " " + str(key),
                                   parse_mode=ParseMode.HTML, reply_markup=markups.admin_menu)

        if message.text == "Вернуться в главное меню":
            await state.set_state(idk.bot_use)
            await bot.send_message(message.from_user.id, "<b>Главное меню:</b>", parse_mode=ParseMode.HTML,
                                   reply_markup=markups.menu)


@start_router.message(idk.reg_answ)
async def procces_reg(message: Message, state: FSMContext):
    db.set_name(message.from_user.id, message.text)
    db.set_signup(message.from_user.id, "done")
    await bot.send_message(message.from_user.id, "<b>Вы успешно зарегистрировались</b>", parse_mode=ParseMode.HTML,
                           reply_markup=markups.menu)
    file_r = open('reg_log.txt', "a+", encoding="utf-8")
    file_r.write('Успешно зарегистрировался: ' + db.get_name(message.from_user.id) + ' ' + str(
        datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")) + '\n')
    file_r.close()
    await state.set_state(idk.bot_use)


@start_router.message(F.text, idk.user_id)
async def process_id(message: Message, state: FSMContext):
    await state.update_data(user_id = message.text)
    data = await state.get_data()
    global shit
    shit = data.get("user_id")

    if (db.user_exists(shit) == True):
        await bot.send_message(message.from_user.id, "<b>Удалить " + db.get_name(shit) + " ?</b>",
                               parse_mode=ParseMode.HTML, reply_markup=markups.ikb_remove_user)
        await state.set_state(idk.admin_delete_user)
    else:
        await bot.send_message(message.from_user.id, "<b>Такого пользователя не существует!</b> ",
                               parse_mode=ParseMode.HTML, reply_markup=markups.admin_menu)
        await state.set_state(idk.admin_panel)


@start_router.callback_query(F.data == "Удалить пользователя")
async def user_deleted(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, 'Пользователь' + db.get_name(shit) + ' - успешно удален!!',
                           parse_mode=ParseMode.HTML, reply_markup=markups.admin_menu)
    await callback.answer('Пользователь' + db.get_name(shit) + ' - успешно удален!',
                           parse_mode=ParseMode.HTML)
    db.delete_user(shit)
    await state.set_state(idk.admin_panel)

@start_router.callback_query(F.data == "Отмена")
async def user_deleted(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, 'Отмена, пусть ' + db.get_name(shit) + ' остаётся!',
                           parse_mode=ParseMode.HTML, reply_markup=markups.admin_menu)
    await state.set_state(idk.admin_panel)

if __name__ == '__main__':
    asyncio.run(main())
