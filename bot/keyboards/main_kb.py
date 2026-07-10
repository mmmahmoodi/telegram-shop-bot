from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


def main_menu_kb() -> ReplyKeyboardMarkup:
    """منوی اصلی کاربر"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 خرید محصول")],
            [KeyboardButton(text="💰 کیف پول"), KeyboardButton(text="📦 سوابق خرید")],
            [KeyboardButton(text="👥 زیرمجموعه‌گیری"), KeyboardButton(text="🎫 پشتیبانی")],
            [KeyboardButton(text="📜 قوانین")],
        ],
        resize_keyboard=True
    )


def back_kb() -> InlineKeyboardMarkup:
    """دکمه بازگشت"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 بازگشت به منوی اصلی", callback_data="back_to_main")]
    ])


def categories_kb(categories: list) -> InlineKeyboardMarkup:
    """نمایش لیست دسته‌بندی‌ها"""
    buttons = []
    for cat in categories:
        buttons.append([
            InlineKeyboardButton(
                text=f"📁 {cat['name']}",
                callback_data=f"category_{cat['id']}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 بازگشت", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_kb(products: list) -> InlineKeyboardMarkup:
    """نمایش لیست محصولات یک دسته‌بندی"""
    buttons = []
    for prod in products:
        buttons.append([
            InlineKeyboardButton(
                text=f"{prod['name']} | 💵 {prod['price']:,} تومان",
                callback_data=f"product_{prod['id']}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 بازگشت", callback_data="back_to_categories")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
