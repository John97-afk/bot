import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from telegram import InputMediaPhoto, InputMediaVideo

# ═══════════════════ НАСТРОЙКИ ═══════════════════
BOT_TOKEN = "8732820371:AAE4iCT-TFMvF5sU10twYX4CT-Nx9yzifUA"  # замени на свой
WELCOME_IMAGE_PATH = "media/welcome.jpg"

# ═══════════════════ ДАННЫЕ УСЛУГ И ИГР ═══════════════════

MAIN_SECTIONS = {
    "dance": {
        "title": "Танцы",
        "description": (
            "💃 <b>Танцевальные шоу</b>\n\n"
            "• Русские народные танцы\n"
            "• Шоу-балет\n"
            "• Мастер-классы\n\n"
            "Так же выступаем с любой программой по пожеланию клиента."
        ),
        "media_folder": "media/dance"
    },
    "covers": {
        "title": "Артисты",
        "description": (
            "🎤 <b>Артисты</b>\n\n"
            "• Живой звук на мероприятие\n"
            "• Профессиональные танцоры и музыканты\n"
            "• Широкий репертуар номеров\n\n"
            "Ваши любимые песни на мероприятии, чтобы каждый участник получил незабываемые впечатления."
        ),
        "media_folder": "media/covers"
    },
    "events": {
        "title": "Анимация",
        "description": (
            "🎉 <b>Анимационные программы</b>\n\n"
            "• Детские праздники\n"
            "• Яркие ведущие для любой публики\n"
            "• Организация досуга для деловых программ\n\n"
            "В нашей команде много талантливых профессионалов, которые точно не оставят участников равнодущными!"
        ),
        "media_folder": "media/events"
    },
    "about": {
        "title": "О нас",
        "description": (
            "ℹ️ <b>О нас</b>\n\n"
            "Мы команда профессионалов, которая делает праздники незабываемыми.\n"
            "Работаем в качестве организаторов либо подрядчиков на любом мероприятии.\n\n"
        ),
        "media_folder": "media/about"
    }
}

GAMES_SUB = {
    "sea_battle": {
        "title": "Морской бой",
        "description": (
            "🚢 <b>Гигантский Морской бой</b>\n\n"
            "- Огромное поле 4х2 метра\n"
            "- Командная игра до 50 человек одновременно\n"
            "- Яркий дизайн подойдет для Вашего мероприятия\n\n"
            "Уникальная игра без аналогов в России, самый большой Морской бой для мероприятий. Идеальное решение для летних ивентов!"
        ),
        "media_folder": "media/games/sea_battle"
    },
    "coconut_bowling": {
        "title": "Кокосовый боулинг",
        "description": (
            "🥥 <b>Кокосовый боулинг</b>\n\n"
            "- Экзотическая версия боулинга с кокосами\n"
            "- Две версии дорожек: 2 или 3,5 метра\n"
            "- Декорации из настоящих тропических фруктов\n\n"
            "Яркое дополнение для летнего мероприятия погружает гостей в атмосферу веселья!"
        ),
        "media_folder": "media/games/coconut_bowling"
    },
    "jenga": {
        "title": "Дженга",
        "description": (
            "🗼 <b>Гигантская Дженга</b>\n\n"
            "- Башня высотой до 2х метров\n"
            "- Азарт от игры\n\n"
            "Универсальная активнсть для тимбилдингов, дней рождений или корпоративов!"
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
        [InlineKeyboardButton("🎤 Артисты", callback_data="section_covers")],
        [InlineKeyboardButton("🎉 Анимация", callback_data="section_events")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="section_about")],
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
    """Для обычных услуг (включая 'О нас'): возврат в главное меню."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Вернуться к услугам", callback_data="main_menu")],
        [InlineKeyboardButton("📞 Показать контакты", callback_data="contacts")]
    ])

def build_subgame_keyboard():
    """Для подразделов игр: возврат к списку игр, а не в главное меню."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Вернуться к играм", callback_data="menu_games")],
        [InlineKeyboardButton("📞 Показать контакты", callback_data="contacts")]
    ])

def build_contacts_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Вернуться к услугам", callback_data="main_menu")]
    ])

# ═══════════════════ ОБРАБОТЧИКИ КОМАНД ═══════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "👋 <b>Здравствуйте! Вас приветствует Holiday Event Group!</b>\n\n"
        "Мы организуем общественные и корпоративные мероприятия любого масштаба под ваш бюджет, скорее знакомьтесь с нашим каталогом!"
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
    # Удаляем предыдущее сообщение с кнопками
    try:
        await query.message.delete()
    except:
        pass
    await query.message.reply_text(
        text="<b>Выберите услугу:</b>",
        reply_markup=build_main_menu_keyboard(),
        parse_mode=ParseMode.HTML
    )

async def games_submenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.message.delete()
    except:
        pass
    await query.message.reply_text(
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

    # Удаляем предыдущее сообщение с кнопками
    try:
        await query.message.delete()
    except:
        pass

    # Отправляем медиа из папки услуги (без подписи)
    await send_media_group(update, context, section["media_folder"])

    # Отправляем описание с кнопками (возврат в главное меню)
    await query.message.reply_text(
        text=section["description"],
        reply_markup=build_section_keyboard(),
        parse_mode=ParseMode.HTML
    )

async def subgame_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subgame_id = query.data.replace("subgame_", "")
    subgame = GAMES_SUB.get(subgame_id)

    if not subgame:
        await query.edit_message_text("Игра не найдена.", reply_markup=build_games_submenu_keyboard())
        return

    # Удаляем предыдущее сообщение с кнопками
    try:
        await query.message.delete()
    except:
        pass

    # Отправляем медиа
    await send_media_group(update, context, subgame["media_folder"])

    # Описание с кнопками (возврат к списку игр, а не в главное меню)
    await query.message.reply_text(
        text=subgame["description"],
        reply_markup=build_subgame_keyboard(),
        parse_mode=ParseMode.HTML
    )

async def contacts_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        await query.message.delete()
    except:
        pass
    await query.message.reply_text(
        text=CONTACTS_TEXT,
        reply_markup=build_contacts_keyboard(),
        parse_mode=ParseMode.HTML
    )

# ═══════════════════ ОТПРАВКА МЕДИА ═══════════════════

async def send_media_group(update: Update, context: ContextTypes.DEFAULT_TYPE, folder: str):
    """Отправляет все фото и видео из папки одной группой, без подписей."""
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
            if ext in ('.mp4', '.mov', '.avi', '.mkv'):
                # Для видео указываем размеры, чтобы сохранить пропорции
                media_group.append(InputMediaVideo(
                    media=f,
                    width=1080,   # ширина вертикального видео
                    height=1920   # высота вертикального видео (16:9)
                ))
            else:
                media_group.append(InputMediaPhoto(media=f))
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

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()