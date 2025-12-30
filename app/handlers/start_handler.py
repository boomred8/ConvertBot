from aiogram import Router, types
from aiogram.filters import Command

import app.keyboards.main_reply as main_reply
router_start = Router()

@router_start.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer(f"Привет, <b>{message.from_user.username}</b>", parse_mode="HTML", reply_markup=main_reply.main_keyboard())