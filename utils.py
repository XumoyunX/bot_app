# from io import BytesIO
from typing import Sequence

# import magic
# from mimetypes import guess_extension
from telegram import (
    ReplyKeyboardMarkup as ReplyKeyboardMarkupOrg,
)
from django.db.models import QuerySet, Model
from telegram._keyboardbutton import KeyboardButton
from telegram._utils.types import JSONDict

from constants import BACK, HOME
from django.db.models import Aggregate, CharField, Value

from language import multilanguage


class ReplyKeyboardMarkup(ReplyKeyboardMarkupOrg):
    def __init__(
        self,
        keyboard: Sequence[Sequence[str | KeyboardButton]] = [],
        back: bool = True,
        lang: str="uz",
        # home: bool = True,
        one_time_keyboard: bool | None = True,
        selective: bool | None = None,
        input_field_placeholder: str | None = None,
        is_persistent: bool | None = None,
        *,
        api_kwargs: JSONDict | None = None
    ):
        super().__init__(
            [*keyboard, [multilanguage.get('back',lang) if back else ""],
            #  [HOME if home else ""]
             ],
            True,
            one_time_keyboard,
            selective,
            input_field_placeholder,
            is_persistent,
            api_kwargs=api_kwargs,
        )


def distribute(items, number=2) -> list:
    res = []
    start = 0
    end = number
    for _ in items:
        if items[start:end] == []:
            return res
        res.append(items[start:end])
        start += number
        end += number
    return res
