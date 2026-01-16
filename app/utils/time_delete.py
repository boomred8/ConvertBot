from __future__ import annotations

import time
from typing import Optional

from aiogram import types
from aiogram.fsm.context import FSMContext


async def ensure_session_alive(
    *,
    state: FSMContext,
    user_id: int,
    message: types.Message,
    ttl_seconds: int,
    cleanup_func,
    reply_markup=None,
    mode_name: str = "сессия"
) -> bool:

    data = await state.get_data()
    now = time.time()

    started_at: Optional[float] = data.get("started_at")
    if started_at is None:
        await state.update_data(started_at=now, last_activity=now)
        return True

    if now - started_at > ttl_seconds:
        await state.clear()
        cleanup_func(user_id)

        await message.answer(
            "⌛ <b>Сессия истекла</b>\n\n"
            f"Вы слишком долго не завершали <b>{mode_name}</b>, поэтому я удалил временные файлы.\n"
            "Запустите режим заново и отправьте файлы ещё раз ✅",
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        return False

    await state.update_data(last_activity=now)
    return True