from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.keyboards.main_kb import main_menu_kb, back_kb
from database.db_worker import add_user, get_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """دستور /start - ثبت کاربر و نمایش منوی اصلی"""
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "بدون نام کاربری",
        first_name=message.from_user.first_name or "کاربر"
    )
    user = await get_user(message.from_user.id)

    welcome_text = (
        f"👋 سلام {message.from_user.first_name} عزیز!\n\n"
        f"🤖 به فروشگاه خودکار خوش آمدی!\n"
        f"💰 موجودی کیف پول: {user['balance']:,.0f} تومان\n\n"
        f"از منوی زیر انتخاب کن 👇"
    )
    await message.answer(welcome_text, reply_markup=main_menu_kb())


@router.message(F.text == "💰 کیف پول")
async def wallet_handler(message: Message):
    """نمایش موجودی کیف پول"""
    user = await get_user(message.from_user.id)
    text = (
        f"💰 **کیف پول شما**\n\n"
        f"موجودی: `{user['balance']:,.0f}` تومان\n\n"
        f"برای افزایش موجودی از دکمه زیر استفاده کنید:"
    )
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 افزایش موجودی (کارت به کارت)", callback_data="increase_balance")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="back_to_main")]
    ])
    await message.answer(text, parse_mode="Markdown", reply_markup=kb)


@router.message(F.text == "📜 قوانین")
async def rules_handler(message: Message):
    """نمایش قوانین فروشگاه"""
    text = (
        "📜 **قوانین فروشگاه**\n\n"
        "1️⃣ تمامی فروش‌ها نهایی بوده و امکان بازگشت وجه وجود ندارد.\n"
        "2️⃣ لطفاً قبل از خرید، توضیحات محصول را کامل بخوانید.\n"
        "3️⃣ در صورت بروز مشکل، از بخش پشتیبانی استفاده کنید.\n"
        "4️⃣ تحویل محصولات دیجیتال به صورت آنی و خودکار انجام می‌شود.\n"
        "5️⃣ سوءاستفاده از سیستم منجر به مسدود شدن حساب می‌شود."
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=back_kb())


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    """بازگشت به منوی اصلی"""
    await callback.message.delete()
    user = await get_user(callback.from_user.id)
    text = (
        f"🏠 **منوی اصلی**\n\n"
        f"💰 موجودی: `{user['balance']:,.0f}` تومان\n\n"
        f"از منوی زیر انتخاب کن 👇"
    )
    await callback.message.answer(text, parse_mode="Markdown", reply_markup=main_menu_kb())
