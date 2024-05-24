from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import os
import datetime
import json

from config import BOT_TOKEN
from parser.filter_setting import get_avito_url
import t_bot.app.keyboards as kb

router = Router()
bot = Bot(BOT_TOKEN)

search_filter = {}
with open(r'C:\Users\Administrator\PycharmProjects\Avito_Scrapper\t_bot\app\filters.json', 'r', encoding='utf-8') as file:
    filters = json.load(file)

@router.message(F.text == '/start')
async def step1_1(message: Message):
    await message.answer('Выберите тип недвижимости:', reply_markup=kb.choice_realty_type)


@router.callback_query(lambda callback_query: callback_query.data.startswith('back_to_menu'))
async def menu(callback: CallbackQuery, bot):
    await callback.message.answer(f'Выберите тип недвижимости:.')
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите тип недвижимости:', reply_markup=kb.choice_realty_type)


@router.callback_query(lambda callback_query: callback_query.data.startswith('kvartira'))
async def flat(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.', reply_markup=kb.flat_choice_type_1)


@router.callback_query(lambda callback_query: callback_query.data.startswith('kypit'))
async def flat(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.', reply_markup=kb.flat_choice_type_2_1)


@router.callback_query(lambda callback_query: callback_query.data.startswith('vtorochka_novostroyki'))
async def flat(callback: CallbackQuery, bot):
    prim_url = filters["Тип недвижимости"]["Квартира"]["Купить"]["Вторичка, новостройки"]
    url = get_avito_url(prim_url)
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.')


@router.callback_query(lambda callback_query: callback_query.data.startswith('vtorochka'))
async def flat(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.')


@router.callback_query(lambda callback_query: callback_query.data.startswith('novostroyki'))
async def flat(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.')


@router.callback_query(lambda callback_query: callback_query.data.startswith('snyat'))
async def step_1_2(callback: CallbackQuery, bot):
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите пункт.', reply_markup=kb.flat_choice_type_2_2)


