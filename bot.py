import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from telegram import InputMediaPhoto, InputMediaVideo

# ═══════════════════ НАСТРОЙКИ ═══════════════════
BOT_TOKEN = "8732820371:AAE4iCT-TFMvF5sU10twYX4CT-Nx9yzifUA"

WELCOME_IMAGE_PATH = "media/welcome.jpg"

# ═══════════════════ ДАННЫЕ УСЛУГ И ИГР ═══════════════════

MAIN_SECTIONS = {
    "dance": {
        "title": "Танцы",
        "description": (
            "💃 <b>Танцевальные шоу</b>\n\n"
            "• Научим танцевать даже твою тёщу\n"
            "• Мы учились для этого в шараге\n"
            "• Профессиональный стриптиз + приват\n\n"
            "Оплата только наличкой!"
        ),
        "media_folder": "media/dance"
    },
    "covers": {
        "title": "Кавер-группы",
        "description": (
            "🎤 <b>Кавер-группы</b>\n\n"
            "• Живой звук на мероприятие\n"
            "• Бас ебашет, бабка пляшет\n"
            "• Слезливые песни про твою бывшую\n\n"
            "Обязательно наличие водки на площадке для выступающих."
        ),
        "media_folder": "media/covers"
    },
    "events": {
        "title": "Организация мероприятий",
        "description": (
            "🎉 <b>Организация мероприятий</b>\n\n"
            "• Похороны и поминки\n"
            "• Допросы и пытки\n"
            "• Подбор площадки\n\n"
            "Быстро и без крови."
        ),
        "media_folder": "media/events"
    }
}

GAMES_SUB = {
    "sea_battle": {
        "title": "Морской бой",
        "description": (
            "🚢 <b>Морской бой</b>\n\n"
            "Огромное поле, живые корабли, командная игра.\n"
            "Описание заменишь под себя."
        ),
        "media_folder": "media/games/sea_battle"
    },
    "coconut_bowling": {
        "title": "Кокосовый боулинг",
        "description": (
            "🥥 <b>Кокосовый боулинг</b>\n\n"
            "Экзотическая версия боулинга с кокосами.\n"
            "Описание заменишь под себя."
        ),
        "media_folder": "media/games/coconut_bowling"
    },
    "jenga": {
        "title": "Дженга",
        "description": (
            "🗼 <b>Дженга</b>\n\n"
            "Гигантская башня, азарт и ловкость.\n"
            "Описание заменишь под себя."
        ),
        "media_folder": "media/games/jenga"
    }
}

CONTACTS_TEXT = (
    "📞 <b>Контакты организаторов</b>\n\n"
    "<b>Телефоны:</b>\n"
    "+7 (985) 147-42-36\n"
    "+7 (968) 365-38-03\n"
    "<b>Telegram:</b>\n"
    "@glazkov_work\n"
    "@anutanuuuta\n"
)

# ═══════════════════ КЛАВИАТУРЫ ═══════════════════

def build_welcome_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Перейти к услугам", callback_data="main_menu")]
    ])

def build_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🦑 Гигантские игры", callback_data="menu_games")],
        [InlineKeyboardButton("💃 Танцы", callback_data="section_dance")],
        [InlineKeyboardButton("🎤 Кавер-группы", callback_data="section_covers")],
        [InlineKeyboardButton("🎉 Организация мероприятий", callback_data="section_events")],
        [InlineKeyboardButton("📞 Показать контакты", callback_data="contacts")]
    ])

def build_games_submenu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚢 Морской бой", callback_data="subgame_sea_battle")],
        [InlineKeyboardButton("🥥 Кокосовый боулинг", callback_data="subgame_coconut_bowling")],
        [InlineKeyboardButton("🗼 Дженга", callback_data="subgame_jenga")],
        [InlineKeyboardButton("🔙 Вернуться к услугам", callback_data="main_menu")],
        [InlineKeyboardButton("📞 Показать контакты", callback_data="contacts")]
    ])

def build_section_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Вернуться к услугам", callback_data="main_menu")],
        [InlineKeyboardButton("📞 Показать контакты", callback_data="contacts")]
    ])

def build_contacts_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Вернуться к услугам", callback_data="main_menu")]
    ])

# ═══════════════════ ОБРАБОТЧИКИ КОМАНД ═══════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "👋 <b>Солнце светит а негры еще не пашут? Не беда!!</b>\n\n"
        "С креативным подрядчиком Кейтеринг ИП А.Э. Даже самые ленивые негры начнут ебащить как не в себя!."
    )
    if os.path.isfile(WELCOME_IMAGE_PATH):
        with open(WELCOME_IMAGE_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                reply_markup=build_welcome_keyboard(),
                parse_mode=ParseMode.HTML
            )
    else:
        await update.message.reply_text(
            text=caption,
            reply_markup=build_welcome_keyboard(),
            parse_mode=ParseMode.HTML
        )

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Отправляем новое сообщение вместо редактирования старого с фото
    await query.message.reply_text(
        text="<b>Выберите услугу:</b>",
        reply_markup=build_main_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )
async def games_submenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="<b>Гигантские игры — выберите игру:</b>",
        reply_markup=build_games_submenu_keyboard(),
        parse_mode=ParseMode.HTML
    )

async def section_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    section_id = query.data.replace("section_", "")
    section = MAIN_SECTIONS.get(section_id)

    if not section:
        await query.edit_message_text("Раздел не найден.", reply_markup=build_main_menu_keyboard())
        return

    # Сначала медиа БЕЗ подписи
    await send_media_group(update, context, section["media_folder"])

    # Потом описание с кнопками
    await query.message.reply_text(
        text=section["description"],
        reply_markup=build_section_keyboard(),
        parse_mode=ParseMode.HTML
    )

    await send_media_group(update, context, section["media_folder"], description=section["description"])

async def subgame_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subgame_id = query.data.replace("subgame_", "")
    subgame = GAMES_SUB.get(subgame_id)

    if not subgame:
        await query.edit_message_text("Игра не найдена.", reply_markup=build_games_submenu_keyboard())
        return

    # Сначала медиа БЕЗ подписи
    await send_media_group(update, context, subgame["media_folder"])

    # Потом описание с кнопками
    await query.message.reply_text(
        text=subgame["description"],
        reply_markup=build_section_keyboard(),
        parse_mode=ParseMode.HTML
    )

    await send_media_group(update, context, subgame["media_folder"], description=subgame["description"])

async def contacts_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=CONTACTS_TEXT,
        reply_markup=build_contacts_keyboard(),
        parse_mode=ParseMode.HTML
    )

# ═══════════════════ ОТПРАВКА МЕДИА ═══════════════════

async def send_media_group(update: Update, context: ContextTypes.DEFAULT_TYPE, folder: str):
    """Отправляет все медиа из папки одной группой, без подписей."""
    if not os.path.isdir(folder):
        return

    files = sorted(os.listdir(folder))
    media_files = []
    for f in files:
        if f.startswith('.'):
            continue
        ext = os.path.splitext(f)[1].lower()
        if ext in ('.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp',
                   '.mp4', '.mov', '.avi', '.mkv'):
            media_files.append(f)

    if not media_files:
        return

    media_group = []
    file_handles = []

    for filename in media_files:
        filepath = os.path.join(folder, filename)
        ext = os.path.splitext(filename)[1].lower()
        try:
            f = open(filepath, 'rb')
            file_handles.append(f)
            if ext in ('.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp'):
                media_group.append(InputMediaPhoto(media=f))
            else:
                media_group.append(InputMediaVideo(media=f))
        except Exception as e:
            print(f"Не удалось открыть {filename}: {e}")

    if media_group:
        try:
            await context.bot.send_media_group(
                chat_id=update.effective_chat.id,
                media=media_group
            )
        except Exception as e:
            print(f"Ошибка при отправке медиа: {e}")
        finally:
            for f in file_handles:
                f.close()

# ═══════════════════ ЗАПУСК БОТА ═══════════════════

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(games_submenu_callback, pattern="^menu_games$"))
    app.add_handler(CallbackQueryHandler(section_callback, pattern="^section_"))
    app.add_handler(CallbackQueryHandler(subgame_callback, pattern="^subgame_"))
    app.add_handler(CallbackQueryHandler(contacts_callback, pattern="^contacts$"))

    # Для Railway используем polling (проще и надёжнее на бесплатном тарифе)
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()