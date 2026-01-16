import asyncio
from aiogram.types import Message


def human_mb(n: int) -> int:
    return max(1, n // (1024 * 1024))
async def reject_if_too_big(message: Message, file_size: int, max_bytes: int) -> bool:
    if file_size > max_bytes:
        await message.answer(
            "⚠️ <b>Файл слишком большой</b>\n\n"
            f"Максимум: <b>{human_mb(max_bytes)} MB</b>\n"
            f"Твой файл: <b>{human_mb(file_size)} MB</b>\n\n"
            "Попробуй уменьшить файл и отправь снова.",
            parse_mode="HTML"
        )
        return True
    return False
