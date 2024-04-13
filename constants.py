from telegram.ext.filters import Text
from language import multilanguage


BACK = "🔙 Ortga"
HOME = "🏠 Bosh menu"

EXCLUDE = ~Text(["/start", "/start td2Wmx", *multilanguage.get_all('back')])



LANGUAGES = {
    "O'zbek tili 🇺🇿": "uz",
    "Русский 🇷🇺": "ru",
    "Узбек тили  🇺🇿": "уз"

}



LANGUAGE = "LANGUAGE"

NAME = "NAME"
PHONE_NUMBER = "PHONE_NUMBER"
SHOP_NUMBER = "SHOP_NUMBER"



MENU = "MENU"
AKP_CODE = "AKP_CODE"
