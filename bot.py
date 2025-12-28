"""
SheerID Telegram Bot dengan School Selection
"""

import os
import logging
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

import config
from sheerid_verifier import SheerIDVerifier

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WAITING_URL, CHOOSE_SCHOOL_METHOD, WAITING_SCHOOL_SEARCH, SELECT_FROM_SEARCH = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /start - meminta verification URL"""
    await update.message.reply_text(
        "🎓 *SheerID Student Verification Bot*\n\n"
        "Kirimkan URL verifikasi SheerID Anda:\n"
        "_(Format: https://services.sheerid.com/verify/...?verificationId=...)_",
        parse_mode='Markdown'
    )
    return WAITING_URL


async def receive_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menerima URL dan parse verification ID"""
    url = update.message.text.strip()
    
    verification_id = SheerIDVerifier.parse_verification_id(url)
    
    if not verification_id:
        await update.message.reply_text(
            "❌ URL tidak valid!\n\n"
            "Pastikan URL mengandung parameter `verificationId`"
        )
        return WAITING_URL
    
    # Simpan verification_id ke context
    context.user_data['verification_id'] = verification_id
    
    await update.message.reply_text(
        f"✅ Verification ID: `{verification_id}`\n\n"
        "Pilih metode pemilihan universitas:",
        parse_mode='Markdown',
        reply_markup=school_selection_keyboard()
    )
    
    return CHOOSE_SCHOOL_METHOD


def school_selection_keyboard():
    """Keyboard untuk memilih metode school selection"""
    keyboard = [
        [InlineKeyboardButton("📋 Gunakan List Preset", callback_data="use_preset")],
        [InlineKeyboardButton("🔍 Cari Universitas Sendiri", callback_data="search_manual")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def use_preset_schools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tampilkan list preset schools dari config.py"""
    query = update.callback_query
    await query.answer()
    
    # Buat keyboard dengan list universitas (max 100 per page untuk Telegram limits)
    keyboard = []
    sorted_schools = sorted(config.SCHOOLS.items(), key=lambda x: x[1]['name'])
    
    for school_id, school_data in sorted_schools[:30]:  # Limit 30 untuk demo
        button_text = f"{school_data['name'][:40]}... ({school_data['state']})"
        keyboard.append([InlineKeyboardButton(
            button_text, 
            callback_data=f"school_preset_{school_id}"
        )])
    
    keyboard.append([InlineKeyboardButton("◀️ Kembali", callback_data="back_to_method")])
    
    await query.edit_message_text(
        "📚 *Pilih Universitas dari List:*\n"
        "_(Menampilkan 30 universitas top)_",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    return CHOOSE_SCHOOL_METHOD


async def search_manual_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompt user untuk memasukkan nama universitas"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔍 *Cari Universitas*\n\n"
        "Ketik nama universitas yang ingin Anda cari:\n"
        "_(Contoh: Harvard, MIT, Stanford)_",
        parse_mode='Markdown'
    )
    
    return WAITING_SCHOOL_SEARCH


async def search_schools_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cari universitas via SheerID API"""
    search_query = update.message.text.strip()
    
    if len(search_query) < 3:
        await update.message.reply_text(
            "❌ Nama terlalu pendek! Minimal 3 karakter."
        )
        return WAITING_SCHOOL_SEARCH
    
    await update.message.reply_text(f"🔍 Mencari universitas: *{search_query}*...", parse_mode='Markdown')
    
    try:
        # Query ke SheerID Organization Search API
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                config.ORGSEARCH_API_URL,
                params={
                    'country': 'US',
                    'type': 'UNIVERSITY',
                    'name': search_query
                }
            )
            
            if response.status_code != 200:
                await update.message.reply_text("❌ Gagal mencari universitas. Coba lagi.")
                return WAITING_SCHOOL_SEARCH
            
            results = response.json()
            
            # Filter hanya UNIVERSITY dan country US
            filtered_results = [
                school for school in results 
                if school.get('type') == 'UNIVERSITY' and school.get('country') == 'US'
            ]
            
            if not filtered_results:
                await update.message.reply_text(
                    f"❌ Tidak ada universitas US untuk '*{search_query}*'\n\n"
                    "Coba kata kunci lain atau gunakan list preset.",
                    parse_mode='Markdown'
                )
                return WAITING_SCHOOL_SEARCH
            
            # Simpan hasil search ke context
            context.user_data['search_results'] = filtered_results[:10]  # Limit 10 hasil
            
            # Buat keyboard dengan hasil search
            keyboard = []
            for idx, school in enumerate(filtered_results[:10]):
                button_text = f"{school['name'][:40]}... ({school.get('city', 'N/A')}, {school.get('state', 'N/A')})"
                keyboard.append([InlineKeyboardButton(
                    button_text,
                    callback_data=f"school_search_{idx}"
                )])
            
            keyboard.append([InlineKeyboardButton("🔄 Cari Lagi", callback_data="search_manual")])
            keyboard.append([InlineKeyboardButton("◀️ Kembali", callback_data="back_to_method")])
            
            await update.message.reply_text(
                f"🎯 *Hasil Pencarian* ({len(filtered_results[:10])} universitas):\n\n"
                "Pilih universitas yang sesuai:",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            
            return SELECT_FROM_SEARCH
            
    except Exception as e:
        logger.error(f"Error searching schools: {e}")
        await update.message.reply_text(
            "❌ Terjadi kesalahan saat mencari universitas.\n"
            "Coba lagi atau gunakan list preset."
        )
        return WAITING_SCHOOL_SEARCH


async def select_preset_school(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pemilihan school dari preset list"""
    query = update.callback_query
    await query.answer()
    
    school_id = query.data.replace("school_preset_", "")
    school = config.SCHOOLS[school_id]
    
    # Simpan school data lengkap ke context
    context.user_data['selected_school'] = {
        'dict_key': school_id,
        'id': school['id'],
        'idExtended': school['idExtended'],
        'name': school['name'],
        'domain': school['domain'],
        'from_search': False
    }
    
    await start_verification(query, context)
    return ConversationHandler.END


async def select_search_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pemilihan school dari hasil search"""
    query = update.callback_query
    await query.answer()
    
    idx = int(query.data.replace("school_search_", ""))
    school = context.user_data['search_results'][idx]
    
    # Simpan school data dari API
    context.user_data['selected_school'] = {
        'dict_key': None,
        'id': school['id'],
        'idExtended': str(school['id']),
        'name': school['name'],
        'domain': school.get('domain', 'university.edu'),
        'from_search': True
    }
    
    await start_verification(query, context)
    return ConversationHandler.END


async def start_verification(query, context: ContextTypes.DEFAULT_TYPE):
    """Mulai proses verifikasi SheerID"""
    verification_id = context.user_data['verification_id']
    school = context.user_data['selected_school']
    
    await query.edit_message_text(
        f"⏳ *Memproses Verifikasi...*\n\n"
        f"🎓 Universitas: {school['name']}\n"
        f"🔑 Verification ID: `{verification_id}`\n\n"
        f"_Mohon tunggu, proses ini memakan waktu 10-30 detik..._",
        parse_mode='Markdown'
    )
    
    try:
        # Jalankan verifikasi
        verifier = SheerIDVerifier(verification_id)
        result = verifier.verify(school_data=school)
        
        if result['success']:
            # Ambil data student info dari result
            student_info = result.get('student_info', {})
            
            # Format message dengan info lengkap
            message = (
                f"✅ *Verifikasi Berhasil!*\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 *INFORMASI MAHASISWA*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"👤 *Nama Lengkap:*\n"
                f"   `{student_info.get('first_name', 'N/A')} {student_info.get('last_name', 'N/A')}`\n\n"
                f"🎓 *Universitas:*\n"
                f"   `{student_info.get('school_name', school['name'])}`\n\n"
                f"📅 *Tanggal Lahir:*\n"
                f"   `{student_info.get('birth_date', 'N/A')}`\n\n"
                f"📧 *Email:*\n"
                f"   `{student_info.get('email', 'N/A')}`\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔑 *Verification ID:*\n"
                f"   `{verification_id}`\n\n"
                f"📋 *Status:*\n"
                f"   {result['message']}\n"
            )
            
            # Tambahkan redirect URL jika ada
            if result.get('redirect_url'):
                message += f"\n🌐 *Redirect URL:*\n   {result.get('redirect_url')}"
            
            await query.edit_message_text(
                message,
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                f"❌ *Verifikasi Gagal!*\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"Error: {result['message']}\n\n"
                f"🔑 Verification ID: `{verification_id}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Gunakan /start untuk mencoba lagi.",
                parse_mode='Markdown'
            )
    
    except Exception as e:
        logger.error(f"Verification error: {e}")
        await query.edit_message_text(
            f"❌ *Error saat verifikasi!*\n\n"
            f"Detail: {str(e)}\n\n"
            f"Gunakan /start untuk mencoba lagi.",
            parse_mode='Markdown'
        )


async def back_to_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kembali ke menu pemilihan metode"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "Pilih metode pemilihan universitas:",
        reply_markup=school_selection_keyboard()
    )
    
    return CHOOSE_SCHOOL_METHOD


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text(
        "❌ Proses dibatalkan.\n\n"
        "Gunakan /start untuk memulai lagi."
    )
    return ConversationHandler.END


def main():
    """Main function untuk run bot"""
    # Ambil token dari environment variable
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found in environment variables!")
        logger.error("Set BOT_TOKEN in Render dashboard: Dashboard > Environment")
        return
    
    logger.info(f"🤖 Starting bot with token: {BOT_TOKEN[:10]}...")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_URL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_url)
            ],
            CHOOSE_SCHOOL_METHOD: [
                CallbackQueryHandler(use_preset_schools, pattern="^use_preset$"),
                CallbackQueryHandler(search_manual_prompt, pattern="^search_manual$"),
                CallbackQueryHandler(select_preset_school, pattern="^school_preset_"),
                CallbackQueryHandler(back_to_method, pattern="^back_to_method$")
            ],
            WAITING_SCHOOL_SEARCH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, search_schools_api)
            ],
            SELECT_FROM_SEARCH: [
                CallbackQueryHandler(select_search_result, pattern="^school_search_"),
                CallbackQueryHandler(search_manual_prompt, pattern="^search_manual$"),
                CallbackQueryHandler(back_to_method, pattern="^back_to_method$")
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(conv_handler)
    
    logger.info("✅ Bot started successfully on Render!")
    logger.info("🌐 Waiting for Telegram updates...")
    
    # Run bot dengan polling
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == '__main__':
    main()
