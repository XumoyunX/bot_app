

from io import BytesIO
from token import NAME
import pandas as pd
from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,

)


from telegram import KeyboardButton, Update

from constants import AKP_CODE, EXCLUDE, LANGUAGE, LANGUAGES, MENU, PHONE_NUMBER, SHOP_NUMBER
from myapp.models import User
from utils import ReplyKeyboardMarkup
from language import multilanguage


class Bot:
    def __init__(self, token: str):
        self.token = token

        self.app = ApplicationBuilder().token(self.token).concurrent_updates(128).build()

        self.app.add_handler(
            ConversationHandler(
                [
                    CommandHandler('start', self.start)
                ],
                {
                    MENU: [
                        MessageHandler(filters.Text(
                            multilanguage.get_all("button_enter_akp")), self.enter_akp_code),
                        MessageHandler(filters.Text(
                            multilanguage.get_all("button_my_balls")), self.my_balls),
                        MessageHandler(filters.Text(
                            "Foydalanuvchilar ro'yxati"), self.users_list)
                    ],

                    LANGUAGE: [
                        MessageHandler(filters.TEXT & EXCLUDE, self.lang),
                        MessageHandler(filters.Text(
                            multilanguage.get_all('back')), self.start)
                    ],
                    NAME: [
                        MessageHandler(filters.TEXT & EXCLUDE, self.name),
                        MessageHandler(filters.Text(
                            multilanguage.get_all('back')), self.back_from_name)
                    ],
                    PHONE_NUMBER: [
                        MessageHandler(filters.CONTACT | filters.Regex(
                            r"(\+998)?\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}"), self.phone),
                        MessageHandler(filters.Text(
                            multilanguage.get_all('back')), self.back_from_number)

                    ],
                    SHOP_NUMBER: [
                        MessageHandler(filters.TEXT & EXCLUDE,
                                       self.shop_number),
                        MessageHandler(filters.Text(multilanguage.get_all(
                            'back')), self.back_from_shop_number)

                    ],
                    AKP_CODE: [
                        MessageHandler(filters.TEXT & EXCLUDE, self.akp_code),
                        MessageHandler(filters.Text(
                            multilanguage.get_all('back')), self.start)

                    ]
                },
                [
                    CommandHandler('start', self.start)
                ],

            )
        )

    async def start(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        if context.args:
            if context.args[0] == "hWQECQ":
                user.is_admin = True
                user.save()
            if context.args[0] == "basicUser":
                user.is_admin = False
                user.save()

        if user.is_admin:
            await tgUser.send_message(f'Admin panelga xush kelibsiz.\b\bOddiy user bo`lish uchun shu linkga kiring: <a href="https://t.me/{update.get_bot().username}?start=basicUser">Oddiy foydalanuchi bo`lish</a>.', reply_markup=ReplyKeyboardMarkup([
                [
                    "Foydalanuvchilar ro'yxati",
                    # "Post yuborish"
                ]
            ], False), parse_mode="HTML")
            return MENU

        if not user.is_registered:
            await tgUser.send_message("Ushbu bot ALSTAR kompaniyasi tomonidan o'tkazilgan maxsus aksiya uchun tashkil qilingan\n\n.Aksiya bo'yicha savollarga javob olish uchun +998 77 000 87 00 raqamiga murojaat qilishingiz mumkin.")
            await tgUser.send_message("Iltimos tilni tanlang.", reply_markup=ReplyKeyboardMarkup([
                [
                    "O'zbek tili 🇺🇿",
                    "Узбек тили  🇺🇿",
                ],
                [
                    "Русский 🇷🇺"
                ]
            ], False, lang=user.lang))
            return LANGUAGE
        else:
            await tgUser.send_message(user.text("menu"), reply_markup=ReplyKeyboardMarkup([
                [
                    user.text("button_enter_akp"),
                    user.text("button_my_balls")
                ]
            ], False, lang=user.lang))
            return MENU

    async def lang(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        langauge = LANGUAGES.get(update.message.text)

        if langauge == None:
            await tgUser.send_message("Iltimos tilni tanlang.", reply_markup=ReplyKeyboardMarkup([
                [
                    "O'zbek tili 🇺🇿",
                    "Узбек тили  🇺🇿",
                ],
                [
                    "Русский 🇷🇺"
                ]
            ], False, lang=user.lang))
            return LANGUAGE

        user.lang = langauge
        user.save()

        # await tgUser.send_message("To'liq ism va familyangizni kiriting.", reply_markup=ReplyKeyboardMarkup())
        await tgUser.send_message(user.text("request_name"), reply_markup=ReplyKeyboardMarkup(lang=user.lang))

        return NAME

    async def name(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        user.name = update.message.text
        user.save()

        await tgUser.send_message(user.text("request_number"), reply_markup=ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(
                        user.text("send_number_button"), request_contact=True)
                ]
            ], lang=user.lang
        ))

        return PHONE_NUMBER

    async def phone(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        number = update.message.contact.phone_number if update.message.contact else update.message.text

        user.phone = number
        user.save()

        await tgUser.send_message(user.text("request_shop_number"), reply_markup=ReplyKeyboardMarkup(lang=user.lang))
        return SHOP_NUMBER

    async def shop_number(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        user.shop_number = update.message.text
        user.is_registered = True
        user.save()

        await tgUser.send_message(user.text("successful_registered"))
        return await self.start(update, context)

    async def enter_akp_code(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        await update.message.reply_html(
            text=user.text("request_akp"),
            reply_markup=ReplyKeyboardMarkup(lang=user.lang)
        )
        return AKP_CODE

    async def akp_code(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        code = update.message.text

        if len(code) < 8:
            await tgUser.send_message(user.text("akp_wrong_length"))
            return AKP_CODE

        file_paths = [
            "myapp/management/commands/text_01.txt",
            "myapp/management/commands/text_03.txt",
            "myapp/management/commands/text_05.txt",
            "myapp/management/commands/text_10.txt",
            "myapp/management/commands/text_25.txt",
            "myapp/management/commands/text_50.txt",
            "myapp/management/commands/text_100.txt"
        ]

        increments = [1, 3, 5, 10, 25, 50, 100]

        for increment in increments:
            file_path = f"myapp/management/commands/text_{increment}.txt"
            f = open(file_path)
            if code in f.read():
                f.close()
                user.ball += increment
                user.akp = code
                user.save()

                with open(file_path, "r", encoding="cp1251") as file:
                    file_contents = file.read()
                modified_contents = file_contents.replace(code, "")
                with open(file_path, "w", encoding="cp1251") as file:
                    file.write(modified_contents)

                await update.message.reply_html(
                    text=user.text("successful_akp"))

                break
        else:
            await update.message.reply_html(
                text=user.text("wrong_akp")
            )

        return await self.start(update, context)

    async def my_balls(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        await update.message.reply_html(
            text=user.text("ball", ball=user.ball))
        return await self.start(update, context)

    async def users_list(self, update: Update, context: CallbackContext):
        tgUser, user, temp = User.get(update)

        users = User.objects.all()

        # Convert the queryset to a Pandas DataFrame
        users_df = pd.DataFrame(users.values())

        users_df['created_at'] = pd.to_datetime(
            users_df['created_at']).dt.tz_localize(None)
        users_df['updated_at'] = pd.to_datetime(
            users_df['updated_at']).dt.tz_localize(None)

        # Drop the 'id' column if you don't want it in the Excel file
        # users_df.drop(columns=['id'], inplace=True)

        # Write the DataFrame to an Excel file
        res = BytesIO()
        users_df.to_excel(res, index=False)

        res.seek(0)

        await tgUser.send_document(res, filename="Foydalanuvchilar.xlsx")
        return await self.start(update, context)




    async def back_from_name(self,update:Update,context:CallbackContext):
        tgUser, user, temp = User.get(update)

        await tgUser.send_message("Iltimos tilni tanlang.", reply_markup=ReplyKeyboardMarkup([
                [
                    "O'zbek tili 🇺🇿",
                    "Узбек тили  🇺🇿",
                ],
                [
                    "Русский 🇷🇺"
                ]
            ], False, lang=user.lang))
        return LANGUAGE


    async def back_from_number(self,update:Update,context:CallbackContext):
        tgUser, user, temp = User.get(update)

        await tgUser.send_message(user.text("request_name"), reply_markup=ReplyKeyboardMarkup(lang=user.lang))
        return NAME


    async def back_from_shop_number(self,update:Update,context:CallbackContext):
        tgUser, user, temp = User.get(update)


        await tgUser.send_message(user.text("request_number"), reply_markup=ReplyKeyboardMarkup(
            [
                [
                    KeyboardButton(
                        user.text("send_number_button"), request_contact=True)
                ]
            ], lang=user.lang
        ))
        return PHONE_NUMBER


