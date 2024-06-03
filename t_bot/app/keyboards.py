from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/start')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже')


choice_realty_type = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Квартира', callback_data='kvartira'),
     InlineKeyboardButton(text='Дом', callback_data='dom')],
    [InlineKeyboardButton(text='Земельный участок', callback_data='uchastok'),
     InlineKeyboardButton(text='Гараж и машиноместо', callback_data='garaz_i_macsinomesto')],
    [InlineKeyboardButton(text='Коммерческая недвижимость', callback_data='komercheskaya')],
])


flat_choice_type_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить', callback_data='flat_kypit')],
    [InlineKeyboardButton(text='Снять', callback_data='flat_snyat')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])

flat_choice_type_2_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вторичка, новостройки', callback_data='flat_choice_vtorochka_novostroyki')],
    [InlineKeyboardButton(text='Вторичка', callback_data='flat_choice_vtorochka')],
    [InlineKeyboardButton(text='Новостройки', callback_data='flat_choice_novostroyki')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])

flat_choice_type_2_2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Длительно', callback_data='flat_choice_dlitelno')],
    [InlineKeyboardButton(text='Посуточно', callback_data='flat_choice_posutochno')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])


def make_row_keyboard(choosing_room: dict) -> InlineKeyboardMarkup:
    row = []
    for key, value in choosing_room.items():
        if value:
            row.append([InlineKeyboardButton(text=f'🔵 {key}', callback_data=key)])
        else:
            row.append([InlineKeyboardButton(text=f'🔴 {key}', callback_data=key)])
    row.append([InlineKeyboardButton(text='Утвердить выбор', callback_data='Утвердить выбор')])
    row.append([InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')])

    return InlineKeyboardMarkup(inline_keyboard=row)


get_price = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Указать ценовой диапазон', callback_data='flat_price')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])


home_choice_type_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить', callback_data='kypit_dom')],
    [InlineKeyboardButton(text='Снять', callback_data='snyat_dom')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])


land_choice_type_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить', callback_data='kypit_zemlyu')],
    [InlineKeyboardButton(text='Снять', callback_data='snyat_zemlyu')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])

land_choice_category_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поселений (ИЖС)', callback_data='izs')],
    [InlineKeyboardButton(text='Сельхозназначения (СНТ, ДНП)', callback_data='snt')],
    [InlineKeyboardButton(text='Промназначения', callback_data='prom')],
    [InlineKeyboardButton(text='(ИЖС)+(СНТ, ДНП)', callback_data='izs_snt'),
     InlineKeyboardButton(text='(ИЖС)+Пром', callback_data='izs_prom')],
    [InlineKeyboardButton(text='(СНТ, ДНП)+Пром', callback_data='snt_prom'),
     InlineKeyboardButton(text='(ИЖС)+(СНТ, ДНП)+Пром', callback_data='izs_snt_prom')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])

land_choice_category_2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поселений (ИЖС)', callback_data='izs_2')],
    [InlineKeyboardButton(text='Сельхозназначения (СНТ, ДНП)', callback_data='snt_2')],
    [InlineKeyboardButton(text='Промназначения', callback_data='prom_2')],
    [InlineKeyboardButton(text='(ИЖС)+(СНТ, ДНП)', callback_data='izs_snt_2'),
     InlineKeyboardButton(text='(ИЖС)+Пром', callback_data='izs_prom_2')],
    [InlineKeyboardButton(text='(СНТ, ДНП)+Пром', callback_data='snt_prom_2'),
     InlineKeyboardButton(text='Выбрать всё', callback_data='izs_snt_prom_2')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])


garage_choice_type = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить', callback_data='kypit_garage')],
    [InlineKeyboardButton(text='Снять', callback_data='snyat_garage')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')]
])

garage_choice_type_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Гараж', callback_data='garage')],
    [InlineKeyboardButton(text='Машиноместо', callback_data='mashinomesto')],
    [InlineKeyboardButton(text='Все варианты', callback_data='garage_mashinomesto')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')]
])

garage_choice_type_2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Гараж', callback_data='garage_2')],
    [InlineKeyboardButton(text='Машиноместо', callback_data='mashinomesto_2')],
    [InlineKeyboardButton(text='Все варианты', callback_data='garage_mashinomesto_2')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])


commerce_choice_type = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить', callback_data='kypit_commer')],
    [InlineKeyboardButton(text='Снять', callback_data='snyat_commer')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])


choice_region = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выбрать регион', callback_data='choice_region')],
    [InlineKeyboardButton(text='В главное меню', callback_data='nazad_v_menu')],
])