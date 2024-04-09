from anyio.streams import file
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from myapp.models import User
from .globals import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    chat_id = update.message.chat_id
    keyboard = [
        [KeyboardButton("O'zbekcha"), KeyboardButton('Русский')]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True)

    language_code = update.effective_user.language_code.lower()
    if language_code in languages:
        lang = languages[language_code]
    else:
        lang = languages['name_uz']
    # text = f"{lang['uz']}: {lang['ru']}"
    # text = f"{lang['start_text']}: {lang['end_text']}"
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    user = User.objects.filter(chat_id=chat_id)
    user = user.first()
    if not user.lang:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Tilni tanlang!", reply_markup=reply_markup)

    else:

        user = User.objects.filter(chat_id=chat_id).first()
        if user and user.phone:
            # Phone number is already available, ask for the AKP
            context.user_data["state"] = "akp"
            await update.message.reply_html(
                text="<b>AKP raqamni kriting!!</b>" if "<b>ПСР нажмите на номер!</b>" else "<b>ПСР нажмите на номер!</b>"
            )
        else:

            await update.message.reply_html(
                text="Assalomu alaykum <b>Trade & Alu-Magnit&Yasar</b> ro'yxatga olish botiga xush kelibsiz!\n\n<b>Iltimos ism-familiyangizni kiriting</b>  <i>(masalan: Anvarov Qodir)</i>"
            )
            context.user_data["state"] = "name"
        await update.message.reply_html(text="Xato")


async def myapp(update: Update, context: ContextTypes):
    try:
        chat_id = update.message.from_user.id
    except:
        chat_id = update.callback_query.message.chat_id
    msg = update.message.text
    state = context.user_data.get('state', 0)
    if state == "name":
        button = [[KeyboardButton("Yuborish", request_contact=True)]]
        btnn = ReplyKeyboardMarkup(button, resize_keyboard=True)
        my_model_instance, created = User.objects.get_or_create(
            chat_id=chat_id)
        my_model_instance.name = msg
        my_model_instance.save()
        if " " in msg:
            await update.message.reply_html("Telefon raqamingizni <b>kiriting</b> ✍️ yoki <b>yuboring</b>",
                                            reply_markup=btnn)
            context.user_data['state'] = 'phone'
            context.user_data['data'] = {"name": msg}

        else:
            await update.message.reply_html(
                "Iltimos ism familiyangizni to'liq kiriting! <i>(masalan: Anvarov Qodir)</i>")

    elif state == "phone":
        if msg[1:].isdigit() and len(msg) in [13, 9] or msg[0] == "+":
            my_model_instance, created = User.objects.get_or_create(
                chat_id=chat_id)
            my_model_instance.phone = msg
            my_model_instance.save()
            await update.message.reply_html(text="<b>Dukonni soni kirting!!</b>",
                                            reply_markup=ReplyKeyboardRemove())

            context.user_data['state'] = 'shop_code'
            context.user_data['data'] = {"name": msg}

        else:
            await update.message.reply_html(
                text="<b>Telefon raqamingizni to'g'ri kiriting</b> <i>(masalan: +998998281026)</i>")

    elif state == "shop_code":

        my_model_instance, created = User.objects.get_or_create(
            chat_id=chat_id)
        my_model_instance.shop_number = msg
        my_model_instance.save()

        await update.message.reply_html(
            text="<b>AKP raqamni kirting!!</b>")
        context.user_data['state'] = 'akp'
        context.user_data['data'] = {"name": msg}

    elif state == "akp":
        chat_id = update.message.chat_id
        user = User.objects.filter(chat_id=chat_id).first()
        if len(msg) == 8:
            if msg in open("myapp/management/commands/text_01.txt").read():

                print("1 ball")
                user = User.objects.filter(chat_id=chat_id).first()
                my_model_instance, created = User.objects.get_or_create(
                    chat_id=chat_id)
                my_model_instance.akp = msg
                a = 1
                my_model_instance.ball += a
                my_model_instance.save()

                # file malumotni o'chrish
                file_path = "myapp/management/commands/text_01.txt"
                data_to_delete = msg
                with open(file_path, "r", encoding="cp1251") as file:
                    file_contents = file.read()
                modified_contents = file_contents.replace(data_to_delete, "")
                with open(file_path, "w", encoding="cp1251") as file:
                    file.write(modified_contents)
                keyboard = [
                    [
                        KeyboardButton("Ball")
                    ]
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard)

                await update.message.reply_html(
                    text=f"<b>AKP kodi saqlandi</b>\n\n----------\n\nSizning Balingiz: {my_model_instance.ball}\n\n----------\n\n", reply_markup=reply_markup)

            elif msg in open("myapp/management/commands/text_03.txt").read():
                print("3 ball")
                my_model_instance, created = User.objects.get_or_create(
                    chat_id=chat_id)
                my_model_instance.akp = msg
                a = 3
                my_model_instance.ball += a
                my_model_instance.save()

                # file malumotni o'chrish
                file_path = "myapp/management/commands/text_03.txt"
                data_to_delete = msg
                with open(file_path, "r", encoding="cp1251") as file:
                    file_contents = file.read()
                modified_contents = file_contents.replace(data_to_delete, "")
                with open(file_path, "w", encoding="cp1251") as file:
                    file.write(modified_contents)

                await update.message.reply_html(
                    text="<b>AKP kodi saqlandi</b>")

            elif msg in open("myapp/management/commands/text_05.txt").read():
                print("5 ball")
                my_model_instance, created = User.objects.get_or_create(
                    chat_id=chat_id)
                my_model_instance.akp = msg
                a = 5
                my_model_instance.ball += a
                my_model_instance.save()

                # file malumotni o'chrish
                file_path = "myapp/management/commands/text_05.txt"
                data_to_delete = msg
                with open(file_path, "r", encoding="cp1251") as file:
                    file_contents = file.read()
                modified_contents = file_contents.replace(data_to_delete, "")
                with open(file_path, "w", encoding="cp1251") as file:
                    file.write(modified_contents)

                await update.message.reply_html(
                    text="<b>AKP kodi saqlandi</b>")

            elif msg in open("myapp/management/commands/text_10.txt").read():
                print("10 ball")
                my_model_instance, created = User.objects.get_or_create(
                    chat_id=chat_id)
                my_model_instance.akp = msg
                a = 10
                my_model_instance.ball += a
                my_model_instance.save()

                # file malumotni o'chrish
                file_path = "myapp/management/commands/text_10.txt"
                data_to_delete = msg
                with open(file_path, "r", encoding="cp1251") as file:
                    file_contents = file.read()
                modified_contents = file_contents.replace(data_to_delete, "")
                with open(file_path, "w", encoding="cp1251") as file:
                    file.write(modified_contents)

                await update.message.reply_html(
                    text="<b>AKP kodi saqlandi</b>")
            elif msg in open("myapp/management/commands/text_25.txt").read():
                print("25 ball")
                my_model_instance, created = User.objects.get_or_create(
                    chat_id=chat_id)
                my_model_instance.akp = msg
                a = 25
                my_model_instance.ball += a
                my_model_instance.save()

                # file malumotni o'chrish
                file_path = "myapp/management/commands/text_25.txt"
                data_to_delete = msg
                with open(file_path, "r", encoding="cp1251") as file:
                    file_contents = file.read()
                modified_contents = file_contents.replace(data_to_delete, "")
                with open(file_path, "w", encoding="cp1251") as file:
                    file.write(modified_contents)

                await update.message.reply_html(
                    text="<b>AKP kodi saqlandi</b>")

            elif msg in open("myapp/management/commands/text_50.txt").read():
                print("50 ball")
                my_model_instance, created = User.objects.get_or_create(
                    chat_id=chat_id)
                my_model_instance.akp = msg
                a = 50
                my_model_instance.ball += a
                my_model_instance.save()

                # file malumotni o'chrish
                file_path = "myapp/management/commands/text_50.txt"
                data_to_delete = msg
                with open(file_path, "r", encoding="cp1251") as file:
                    file_contents = file.read()
                modified_contents = file_contents.replace(data_to_delete, "")
                with open(file_path, "w", encoding="cp1251") as file:
                    file.write(modified_contents)

                await update.message.reply_html(
                    text="<b>AKP kodi saqlandi</b>")

            elif msg in open("myapp/management/commands/text_100.txt").read():
                print("100 ball")
                my_model_instance, created = User.objects.get_or_create(
                    chat_id=chat_id)
                my_model_instance.akp = msg
                a = 100
                my_model_instance.ball += a
                my_model_instance.save()

                # file malumotni o'chrish
                file_path = "myapp/management/commands/text_100.txt"
                data_to_delete = msg
                with open(file_path, "r", encoding="cp1251") as file:
                    file_contents = file.read()
                modified_contents = file_contents.replace(data_to_delete, "")
                with open(file_path, "w", encoding="cp1251") as file:
                    file.write(modified_contents)

                await update.message.reply_html(
                    text="<b>AKP kodi saqlandi</b>")

            else:
                await update.message.reply_html(
                    text="<b>AKP kodi xato boshqatdan tekshiring!!</b>")

        elif msg == "Ball":
            my_model_instance, created = User.objects.get_or_create(
                chat_id=chat_id)
            my_model_instance.akp = msg
            keyboard = [
                [
                    KeyboardButton("Ball")
                ]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            await update.message.reply_html(
                text=f"<b>Sizning Balingiz:</b>{my_model_instance.ball}",
                reply_markup=reply_markup)

        else:
            await update.message.reply_html(
                text="<b>AKP kodi xato 8 ta son tekshiring!!</b>")

        context.user_data['state'] = 'lang'
        context.user_data['data'] = {"name": msg}


app = ApplicationBuilder().token(
    "5324045923:AAFUBC5cNbCMtdLiIq-PHY_sa-5Wx3O8des").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, myapp)),

keyboard = [
    [KeyboardButton('Uzbekcha'), KeyboardButton('Русский')]
]
reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


app.run_polling()
