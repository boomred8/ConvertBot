from aiogram import Router, types, F
from aiogram.filters import Command

import app.keyboards.main_reply as main_reply

# Its functionality will be different in the future

profile_router = Router()

@profile_router.message(F.text == "Профиль 🧑🏻")
async def profile_info(message: types.Message):
    await message.answer(f"Username: {message.from_user.username}\n"
                         f"User ID: {message.from_user.id}\n"
                         f"Premium: {message.from_user.is_premium}\n")


