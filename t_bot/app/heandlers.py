from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import os
import datetime
import json

from RealtorTools.config import BOT_TOKEN
from RealtorTools.parser.filter_setting import get_avito_url
import RealtorTools.t_bot.app.keyboards as kb

router = Router()
bot = Bot(BOT_TOKEN)

search_filter = {}

# with open(r'C:\Users\Administrator\PycharmProjects\Avito_Scrapper\t_bot\app\filters.json', 'r', encoding='utf-8') as file:
with open(r'C:\Users\User\PycharmProjects\Rieltor\RealtorTools\t_bot\app\filters.json', 'r', encoding='utf-8') as file:
    filters = json.load(file)


@router.message(F.text == '/start')
async def step1_1(message: Message):
    await message.answer('Выберите тип недвижимости:', reply_markup=kb.choice_realty_type)


@router.callback_query(lambda callback_query: callback_query.data.startswith('nazad_v_menu'))
async def menu(callback: CallbackQuery, bot):
    await callback.message.answer(f'Выберите тип недвижимости:.')
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите тип недвижимости:', reply_markup=kb.choice_realty_type)


@router.callback_query(lambda callback_query: callback_query.data.startswith('kvartira'))
async def flat(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.', reply_markup=kb.flat_choice_type_1)


@router.callback_query(lambda callback_query: callback_query.data.startswith('kypit'))
async def flat(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.', reply_markup=kb.flat_choice_type_2_1)


# available_q_room = [
#     'Студия', '1 комната', '2 комнаты', '3 комнаты', '4 комнаты', '5 комнат и более', 'Свободная планировка'
# ]


# @router.callback_query(lambda callback_query: callback_query.data.startswith('vtorochka_novostroyki'))
# @router.message(StateFilter(None), Command("vtorochka_novostroyki"))
# async def flat(message: Message, state: FSMContext):
#     await bot.send_message(
#         chat_id=message.from_user.id, text='Выберите пункт.', reply_markup=kb.make_row_keyboard(available_q_room)
#     )
#     await state.set_state(QRoom.choosing_room)


# @router.message(QRoom.choosing_room, F.text.in_(available_q_room))
# async def quantity_five(message: Message, state: FSMContext):
#     print('запущено')
#     await state.update_data(choosing_room=message.text.lower())
#     await bot.send_message(chat_id=message.from_user.id, text='Выберите пункт.', reply_markup=kb.flat_custom_choice())


# @router.callback_query(lambda callback_query: callback_query.data.startswith('vtorochka_novostroyki'))
# async def flat(callback: CallbackQuery, bot):
#     await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.', reply_markup=kb.flat_custom_choice())


@router.callback_query(lambda callback_query: callback_query.data.startswith('vtorochka'))
async def flat(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.')


@router.callback_query(lambda callback_query: callback_query.data.startswith('novostroyki'))
async def flat(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.')


@router.callback_query(lambda callback_query: callback_query.data.startswith('flat_snyat'))
async def step_1_2(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.', reply_markup=kb.flat_choice_type_2_2)


class QRoom(StatesGroup):
    choosing_room = State()
    price = State()


@router.callback_query(lambda callback_query: callback_query.data.startswith('flat_kypit'))
async def cmd_room(message: Message, state: FSMContext):
    choosing_room = {
                     'Студия': False,
                     '1 комната': False,
                     '2 комнаты': False,
                     '3 комнаты': False,
                     '4 комнаты': False,
                     '5 комнат и более': False,
                     'Свободная планировка': False
                     }
    await state.update_data(choosing_room=choosing_room)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Выберите количество комнат:",
        reply_markup=kb.make_row_keyboard(choosing_room)
    )

    await state.set_state(QRoom.choosing_room)


@router.callback_query(QRoom.choosing_room, lambda callback_query: callback_query.data.startswith('Утвердить выбор'))
async def one_room(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    choosing_room = data['choosing_room']

    options = [key for key, value in choosing_room.items() if value]
    print(options)

    await state.update_data(choosing_room=choosing_room)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(
        text=f"Укажите ценовой диапазон:", reply_markup=kb.get_price
    )
    await state.set_state(QRoom.choosing_room)


@router.callback_query(QRoom.choosing_room)
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    """Универсальный обработчик
        room_choice: кнопка, которую нажал user"""
    data = await state.get_data()
    choosing_room = data['choosing_room']

    room_choice = callback_query.data
    if not choosing_room[room_choice]:
        choosing_room[room_choice] = True
    else:
        choosing_room[room_choice] = False

    await state.update_data(choosing_room=choosing_room)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(
        text="Выберите количестао комнат:", reply_markup=kb.make_row_keyboard(choosing_room)
    )
    await state.set_state(QRoom.choosing_room)


@router.callback_query(QRoom.choosing_room, lambda callback_query: callback_query.data.startswith('min_price'))
async def one_room(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(min_price=message.text)
    await state.set_state(QRoom.price)
    await message.answer("Введите количество 4:")


@router.callback_query(QRoom.choosing_room, lambda callback_query: callback_query.data.startswith('flat_min_price'))
async def one_room(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    choosing_room = data['choosing_room']

    options = [key for key, value in choosing_room.items() if value]
    print(options)

    await state.update_data(choosing_room=choosing_room)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(
        text=f"Укажите ценовой диапазон:", reply_markup=kb.get_price
    )
    await state.set_state(QRoom.choosing_room)


@router.callback_query(QRoom.price)
async def process_callback(callback_query: CallbackQuery, state: FSMContext):
    """Универсальный обработчик
        room_choice: кнопка, которую нажал user"""
    data = await state.get_data()
    choosing_room = data['choosing_room']

    room_choice = callback_query.data
    if not choosing_room[room_choice]:
        choosing_room[room_choice] = True
    else:
        choosing_room[room_choice] = False

    await state.update_data(choosing_room=choosing_room)

    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(
        text="Выберите количестао комнат:", reply_markup=kb.make_row_keyboard(choosing_room)
    )
    await state.set_state(QRoom.choosing_room)


@router.message(QRoom.min_price)
async def min_max_price(message: Message, state: FSMContext):
    await state.set_state(QRoom.min_price)
    data = await state.get_data()
    min_price = data['min_price']

    await state.update_data(min_price=min_price)

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.message.answer(
        text="Укажите значение минимальной цены, или подтвердите:", reply_markup=kb.get_price
    )
    await state.set_state(QRoom.choosing_room)
