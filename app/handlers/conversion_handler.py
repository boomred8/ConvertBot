from pathlib import Path
from aiogram.types import FSInputFile, message
from aiogram import Router, types, F
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards.main_reply as main_reply
import app.keyboards.conversion_markup as conversion_markup
from app.conversion import photo_to_pdf, combine_images_to_pdf, squeeze_pdf, doc_to_pdf

conversion_router = Router()

class ConversionStates(StatesGroup):
    waiting_file = State()


@conversion_router.message(F.text == 'Конвертация 📦')
async def choice_convert(message: types.Message,
                         state: FSMContext):
    await state.set_state(ConversionStates.waiting_file)

    await message.answer( "<b>Конвертация файлов</b>\n\n"
                               "Выберите нужный режим конвертации 👇\n"
                               "После выбора просто отправьте файл или фотографии.\n\n"
                               "⏳ Обработка происходит автоматически.",
                               parse_mode="HTML",
                               reply_markup=conversion_markup.inline_convert_markup())


@conversion_router.callback_query(F.data == 'back_to_menu',
                                  ConversionStates.waiting_file)
async def back_to_menu(callback: types.CallbackQuery,
                       state: FSMContext):
    await callback.answer("back to menu")
    await callback.message.answer(f"<b>Вы вернулись в главное меню</b> ⬅️\n\n"
                                  f"Выберите дальнейшее действие.",
                                  parse_mode="HTML",
                                  reply_markup=main_reply.main_keyboard())
    await state.clear()


@conversion_router.callback_query(F.data == 'docx_to_pdf',
                                  ConversionStates.waiting_file)
async def docx_to_pdf(callback: types.CallbackQuery,
                state: FSMContext):
    await callback.answer("function <docx to pdf> is on")
    await state.update_data(convert_type="docx_to_pdf")

    await callback.message.answer("📄 <b>DOCX → PDF</b>\n\n"
                                  "Отправьте документ, и я конвертирую его в PDF.\n"
                                  "❌ Для выхода нажмите «Stop».",
                                  parse_mode="HTML",
                                  reply_markup=conversion_markup.inline_stop_convert_markup())


@conversion_router.callback_query((F.data.in_({'photo_to_pdf', 'combine'})),
                                  ConversionStates.waiting_file)
async def choose_photo_to_pdf(callback: types.CallbackQuery,
                       state: FSMContext):
    if callback.data == 'photo_to_pdf':
        await callback.answer("function <photo to pdf> is on")
        await state.update_data(convert_type="photo_to_pdf")

        await callback.message.answer("🖼️ <b>Фото → PDF</b>\n\n"
                                      "Отправьте изображение, и я превращу его в PDF-файл.\n\n"
                                      "❌ Для выхода нажмите «Stop».",
                                      parse_mode="HTML",
                                      reply_markup=conversion_markup.inline_stop_convert_markup())

    elif callback.data == 'combine':
        await callback.answer("function <combine> is on")
        await state.update_data(convert_type="combine",
                                images=[])
        panel = await callback.message.answer(
            "🗂 <b>Режим объединения активен</b>\n\n"
            "Отправляйте фотографии.\n"
            "Добавлено: <b>0</b>",
            parse_mode="HTML",
            reply_markup=conversion_markup.inline_combine_markup()
        )
        await state.update_data(panel_msg_id=panel.message_id)

@conversion_router.callback_query(F.data == 'squeeze',
                                  ConversionStates.waiting_file)
async def squeeze(callback: types.CallbackQuery,
                  state: FSMContext):
    await callback.answer("function <squeeze> is on")
    await state.update_data(convert_type="squeeze",)

    await callback.message.answer("🗜️ <b>Сжатие PDF</b>\n\n"
                                  "Отправьте PDF-файл, и я постараюсь уменьшить его размер\n"
                                  "без заметной потери качества.\n\n"
                                  "ℹ️ Итоговый размер зависит от содержимого PDF.\n"
                                  "❌ Для выхода нажмите «Stop».",
                                  parse_mode="HTML",
                                  reply_markup=conversion_markup.inline_stop_convert_markup())


@conversion_router.callback_query(F.data == 'stop_to_convert')
async def stop_to_convert(callback: types.CallbackQuery,
                          state: FSMContext):
    await callback.answer("function <stop_to_convert> is on")
    await state.clear()

    await callback.message.answer("⛔ <b>Конвертация остановлена</b>\n\n"
                                  "Вы вернулись в главное меню.\n"
                                  "Можете выбрать другое действие 👇",
                                  parse_mode="HTML",
                                  reply_markup=main_reply.main_keyboard())



@conversion_router.message((F.photo | F.document),
                           ConversionStates.waiting_file)
async def document_processing(message: types.Message,
                              state: FSMContext):
    data = await state.get_data()
    convert_type = data.get("convert_type")

    bot = message.bot
    user_id = message.from_user.id

    base_dir = Path('from_user') / str(user_id)
    input_dir = base_dir / 'input'
    output_dir = base_dir / 'output'

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not convert_type:
        await message.answer("Сначала выберете режим конвертации в меню",
                             reply_markup=main_reply.main_keyboard())
        return

    if convert_type == 'docx_to_pdf' and message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name

        tg_file = await bot.get_file(file_id)
        input_path = input_dir / file_name

        await bot.download_file(tg_file.file_path, destination=input_path)

        output_path = output_dir / (input_path.stem + '.pdf')
        doc_to_pdf(input_path, output_path)

        await message.answer_document(
            types.FSInputFile(output_path),
            caption="PDF готов"
        )
        await state.clear()
        return

    elif convert_type == 'photo_to_pdf':
        if not message.photo:
            await message.answer("Пожалуйста, отправьте именно <b>фото</b>",
                                 parse_mode="HTML")
            return

        photo = message.photo[-1]
        file_id = photo.file_id
        tg_file = await bot.get_file(file_id)

        input_path = input_dir / f"photo_{message.message_id}.jpg"
        await bot.download_file(tg_file.file_path, destination=input_path)

        output_path = output_dir / f"photo_{message.message_id}.pdf"
        photo_to_pdf(input_path, output_path)

        await message.answer_document(
            types.FSInputFile(output_path),
            caption="PDF готов"
        )

        await state.clear()
        return

    elif convert_type == 'combine':
        if not message.photo:
            await message.answer("Пожалуйста, отправьте именно <b>фото</b>",
                                 parse_mode="HTML")
            return

        data = await state.get_data()
        images = data.get("images", [])
        panel_msg_id = data.get("panel_msg_id")

        photo = message.photo[-1]
        tg_file = await bot.get_file(photo.file_id)

        input_path = input_dir / f"combine_{message.message_id}.jpg"
        await bot.download_file(tg_file.file_path, destination=input_path)

        images.append(str(input_path))
        await state.update_data(images=images)

        if panel_msg_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=panel_msg_id,
                text=(
                    "🗂 <b>Режим объединения активен</b>\n\n"
                    f"Отправляйте фотографии.\n"
                    f"Добавлено: <b>{len(images)}</b>"
                ),
                parse_mode="HTML",
                reply_markup=conversion_markup.inline_combine_markup()
            )
        else:
            panel = await message.answer(
                "🗂 <b>Режим объединения активен</b>\n\n"
                "Отправляйте фотографии.\n"
                f"Добавлено: <b>{len(images)}</b>",
                parse_mode="HTML",
                reply_markup=conversion_markup.inline_combine_markup()
            )
            await state.update_data(panel_msg_id=panel.message_id)

        return

    elif convert_type == 'squeeze':
        if not message.document:
            await message.answer("⚠️ Отправьте <b>PDF-файл</b>.", parse_mode="HTML")
            return
        is_pdf = (message.document.file_name or "").lower()
        if not is_pdf.endswith(".pdf"):
            await message.answer("⚠️ Нужен именно <b>.pdf</b> файл.", parse_mode="HTML")
            return

        file_name = message.document.file_name
        file_id = message.document.file_id
        tg_file = await bot.get_file(file_id)

        input_path = input_dir / file_name
        await bot.download_file(tg_file.file_path, destination=input_path)

        output_path = output_dir / f"{Path(file_name).stem}_squeeze.pdf"

        try:
            squeeze_pdf(input_path, output_path)

            # если вдруг стало больше — отправим оригинал
            if output_path.exists() and output_path.stat().st_size >= input_path.stat().st_size:
                send_path = input_path
            else:
                send_path = output_path

            await message.answer_document(
                FSInputFile(send_path),
                caption="✅ Готово: PDF сжат"
            )

            await state.clear()
            return

        except Exception as e:
            await message.answer(
                f"❌ Не удалось сжать PDF.\n"
                f"Причина: <code>{e}</code>",
                parse_mode="HTML"
            )
            return


@conversion_router.callback_query(F.data == "ready_to_combine",
                           ConversionStates.waiting_file)
async def ready_to_combine(callback: types.CallbackQuery,
                           state: FSMContext):
    data = await state.get_data()
    images = data.get("images", [])

    if not images:
        await callback.answer("Нет фотографий", show_alert=True)
        return

    user_id = callback.from_user.id
    base_dir = Path('from_user') / str(user_id)
    output_dir = base_dir / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    out_pdf = output_dir / f"combined_{callback.from_user.id}.pdf"
    combine_images_to_pdf([Path(p) for p in images], out_pdf)

    await callback.message.answer_document(
        FSInputFile(out_pdf),
        caption="✅ PDF готов"
    )
    await state.clear()
    await callback.answer()


@conversion_router.callback_query(F.data == "clear_combine", ConversionStates.waiting_file)
async def clear_combine(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(images=[])
    await callback.answer("Очищено")

    data = await state.get_data()
    panel_msg_id = data.get("panel_msg_id")
    if panel_msg_id:
        await callback.message.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=panel_msg_id,
            text=(
                "🗂 <b>Режим объединения активен</b>\n\n"
                "Отправляйте фотографии.\n"
                "Добавлено: <b>0</b>"
            ),
            parse_mode="HTML",
            reply_markup=conversion_markup.inline_combine_markup()
        )


@conversion_router.callback_query(F.data == "cancel_combine", ConversionStates.waiting_file)
async def cancel_combine(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer("Отменено")

    await callback.message.answer(
        "⛔ <b>Объединение отменено</b>\n\n"
        "Вы вернулись в главное меню.",
        parse_mode="HTML",
        reply_markup=main_reply.main_keyboard()
    )

