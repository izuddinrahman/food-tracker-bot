import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ai_analyzer import analyze_meal
from database import (
    get_or_create_user, get_user, get_all_users,
    get_all_telegram_ids, get_users_by_tag,
    save_meal, get_today_meals, get_last_meal, delete_meal,
    get_week_meals, sum_nutrition, update_user_targets,
    add_tag_to_user, remove_tag_from_user,
    save_water, get_today_water,
    save_broadcast_log,
)
from reports import build_daily_summary, build_weekly_summary

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

ADMIN_IDS = [
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
]


def is_admin(telegram_id: int) -> bool:
    return telegram_id in ADMIN_IDS


# ─── COMMANDS ────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_or_create_user(user.id, user.first_name)
    msg = (
        f"👋 Salam *{user.first_name}*!\n\n"
        "Saya akan bantu track pemakanan & air harian anda.\n\n"
        "📸 *Cara log meal:*\n"
        "Snap gambar makanan dan hantar terus. Boleh tambah nota dalam caption!\n\n"
        "📋 *Commands:*\n"
        "/today — Ringkasan hari ini\n"
        "/week — Ringkasan 7 hari\n"
        "/air [jumlah] — Log air minum\n"
        "/log [nama] [kalori] — Log manual\n"
        "/undo — Padam log terakhir\n"
        "/target — Set target kalori\n"
        "/mytags — Lihat tag anda\n"
        "/help — Bantuan lengkap\n\n"
        "Jom mula! Hantar gambar makanan pertama anda 🍛"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_section = ""
    if is_admin(update.effective_user.id):
        admin_section = (
            "\n👑 *Admin Commands:*\n"
            "/broadcast [mesej] — Blast ke semua users\n"
            "/broadcast #tag [mesej] — Blast ikut tag\n"
            "/tag [user\\_id] [tag] — Tag user\n"
            "/removetag [user\\_id] [tag] — Buang tag\n"
            "/users — Senarai semua users\n"
        )
    msg = (
        "📖 *Panduan Guna Bot*\n\n"
        "📸 *Log Meal* — Snap & hantar gambar\n"
        "   Boleh tambah nota dalam caption!\n"
        "   Contoh caption: 'separuh je makan'\n\n"
        "💧 */air* — Tengok air hari ini\n"
        "   */air 250* — Log 250ml air\n\n"
        "✏️ */log Nasi goreng 450* — Log manual\n\n"
        "↩️ */undo* — Padam meal terakhir\n\n"
        "📊 */today* — Ringkasan hari ini\n"
        "📈 */week* — Trend 7 hari\n\n"
        "🎯 */target 1800 60* — Set kalori & protein\n\n"
        "🏷️ */mytags* — Lihat tag anda\n\n"
        "⏰ Auto summary setiap *9pm* & report mingguan *Ahad 8pm*"
        f"{admin_section}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    get_or_create_user(telegram_id, update.effective_user.first_name)
    await update.message.reply_text("⏳ Menyediakan ringkasan...")
    summary = build_daily_summary(telegram_id)
    await update.message.reply_text(summary, parse_mode="Markdown")


async def cmd_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    get_or_create_user(telegram_id, update.effective_user.first_name)
    await update.message.reply_text("⏳ Menyediakan ringkasan mingguan...")
    summary = build_weekly_summary(telegram_id)
    await update.message.reply_text(summary, parse_mode="Markdown")


async def cmd_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    args = context.args
    if len(args) < 1:
        user = get_user(telegram_id)
        cal = user.get("daily_cal_target", 2000) if user else 2000
        protein = user.get("daily_protein_target", 50) if user else 50
        await update.message.reply_text(
            f"🎯 *Target Semasa:*\n"
            f"🔥 Kalori: {cal} kcal/hari\n"
            f"💪 Protein: {protein}g/hari\n\n"
            f"Untuk tukar: `/target 1800 60`",
            parse_mode="Markdown"
        )
        return
    try:
        cal_target = int(args[0])
        protein_target = int(args[1]) if len(args) > 1 else 50
        update_user_targets(telegram_id, cal_target, protein_target)
        await update.message.reply_text(
            f"✅ Target dikemaskini!\n"
            f"🔥 Kalori: {cal_target} kcal/hari\n"
            f"💪 Protein: {protein_target}g/hari",
            parse_mode="Markdown"
        )
    except ValueError:
        await update.message.reply_text("❌ Format salah. Contoh: `/target 1800 60`")


async def cmd_undo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    last_meal = get_last_meal(telegram_id)
    if not last_meal:
        await update.message.reply_text("❌ Tiada meal untuk dipadam.")
        return
    meal_name = last_meal.get("meal_name", "Unknown")
    meal_cal = last_meal.get("calories", 0)
    meal_id = last_meal.get("id")
    context.user_data["pending_undo"] = meal_id
    await update.message.reply_text(
        f"⚠️ *Confirm padam?*\n\n"
        f"🍽️ {meal_name} ({meal_cal} kal)\n\n"
        f"Taip *YA* untuk confirm padam.\n"
        f"Taip apa-apa lain untuk batal.",
        parse_mode="Markdown"
    )


async def cmd_air(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    args = context.args
    if not args:
        total_ml = get_today_water(telegram_id)
        glasses = total_ml // 250
        target_ml = 2000
        target_glasses = 8
        ratio = min(total_ml / target_ml, 1.0) if target_ml > 0 else 0
        filled = round(ratio * 10)
        bar = "💧" * filled + "○" * (10 - filled)
        pct = round(ratio * 100)
        status = "✅ Target tercapai! Tahniah!" if total_ml >= target_ml else f"Lagi {target_ml - total_ml}ml untuk capai target."
        await update.message.reply_text(
            f"💧 *Air Hari Ini*\n\n"
            f"{bar} {pct}%\n\n"
            f"🥛 {glasses} gelas ({total_ml}ml) / {target_glasses} gelas ({target_ml}ml)\n\n"
            f"{status}\n\n"
            f"Log air: `/air 250` (1 gelas)\n"
            f"Log air: `/air 500` (2 gelas)",
            parse_mode="Markdown"
        )
        return
    try:
        amount = int(args[0])
        if amount <= 0 or amount > 5000:
            await update.message.reply_text("❌ Jumlah air tidak valid (1-5000ml).")
            return
        save_water(telegram_id, amount)
        total_ml = get_today_water(telegram_id)
        glasses = total_ml // 250
        await update.message.reply_text(
            f"💧 *{amount}ml dilog!*\n\n"
            f"Total hari ini: *{total_ml}ml* ({glasses} gelas)\n"
            f"Target: 2000ml (8 gelas)\n\n"
            f"{'✅ Target tercapai!' if total_ml >= 2000 else f'Lagi {2000 - total_ml}ml untuk target.'}",
            parse_mode="Markdown"
        )
    except ValueError:
        await update.message.reply_text("❌ Format: `/air 250` (dalam ml)")


async def cmd_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    get_or_create_user(telegram_id, update.effective_user.first_name)
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "📝 *Log Manual*\n\n"
            "Format: `/log [nama makanan] [kalori]`\n\n"
            "Contoh:\n"
            "`/log Roti canai 300`\n"
            "`/log Milo ais 150`",
            parse_mode="Markdown"
        )
        return
    try:
        calories = int(args[-1])
        meal_name = " ".join(args[:-1])
        meal_data = {
            "meal_name": meal_name,
            "portion": "manual log",
            "calories": calories,
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0,
            "fiber_g": 0,
            "sodium_mg": 0,
            "confidence": "manual",
            "raw_response": "",
        }
        save_meal(telegram_id, meal_data)
        today_meals = get_today_meals(telegram_id)
        totals = sum_nutrition(today_meals)
        user = get_user(telegram_id)
        cal_target = user.get("daily_cal_target", 2000) if user else 2000
        await update.message.reply_text(
            f"✅ *Dilog Manual!*\n\n"
            f"🍽️ {meal_name}\n"
            f"🔥 {calories} kal\n\n"
            f"Total hari ini: *{totals['calories']} / {cal_target} kal*",
            parse_mode="Markdown"
        )
    except ValueError:
        await update.message.reply_text("❌ Format salah. Contoh: `/log Nasi goreng 450`")


async def cmd_mytags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    user = get_user(telegram_id)
    if not user:
        await update.message.reply_text("Sila /start dahulu.")
        return
    tags = user.get("tags", "") or ""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    if not tag_list:
        await update.message.reply_text("🏷️ Anda belum ada tag.\n\nTag ditetapkan oleh admin klinik.")
    else:
        tags_display = " | ".join([f"#{t}" for t in tag_list])
        await update.message.reply_text(f"🏷️ *Tag anda:*\n\n{tags_display}", parse_mode="Markdown")


async def cmd_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin sahaja boleh guna command ini.")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "Format: `/tag [telegram_id] [tag]`\nContoh: `/tag 123456789 diabetes`",
            parse_mode="Markdown"
        )
        return
    try:
        target_id = int(args[0])
        tag = args[1].lower().strip().lstrip("#")
        success = add_tag_to_user(target_id, tag)
        if success:
            await update.message.reply_text(f"✅ Tag `#{tag}` ditambah kepada user `{target_id}`.", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ User `{target_id}` tidak dijumpai.", parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ telegram_id mesti nombor.")


async def cmd_removetag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin sahaja boleh guna command ini.")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Format: `/removetag [telegram_id] [tag]`", parse_mode="Markdown")
        return
    try:
        target_id = int(args[0])
        tag = args[1].lower().strip().lstrip("#")
        remove_tag_from_user(target_id, tag)
        await update.message.reply_text(f"✅ Tag `#{tag}` dibuang dari user `{target_id}`.", parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ telegram_id mesti nombor.")


async def cmd_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin sahaja.")
        return
    users = get_all_users()
    if not users:
        await update.message.reply_text("Tiada users lagi.")
        return
    lines = ""
    for u in users:
        tags = u.get("tags", "") or ""
        tag_display = f" [{tags}]" if tags else ""
        streak = u.get("streak_count", 0)
        lines += f"• {u.get('name', '-')} (`{u['telegram_id']}`){tag_display} — streak: {streak}\n"
    await update.message.reply_text(f"👥 *Senarai Users ({len(users)} orang):*\n\n{lines}", parse_mode="Markdown")


async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin sahaja boleh broadcast.")
        return
    args = context.args
    if not args:
        await update.message.reply_text(
            "📢 *Cara Broadcast:*\n\n"
            "Semua users:\n`/broadcast Klinik tutup esok`\n\n"
            "Ikut tag:\n`/broadcast #diabetes Jangan lupa semak gula`",
            parse_mode="Markdown"
        )
        return
    target_tag = "all"
    message_parts = args[:]
    if args[0].startswith("#"):
        target_tag = args[0].lstrip("#").lower()
        message_parts = args[1:]
    if not message_parts:
        await update.message.reply_text("❌ Mesej kosong.")
        return
    broadcast_message = " ".join(message_parts)
    if target_tag == "all":
        recipients = get_all_telegram_ids()
    else:
        users = get_users_by_tag(target_tag)
        recipients = [u["telegram_id"] for u in users]
    if not recipients:
        await update.message.reply_text(f"❌ Tiada user {'dengan tag #' + target_tag if target_tag != 'all' else ''}.")
        return
    target_label = f"#{target_tag}" if target_tag != "all" else "Semua users"
    context.user_data["pending_broadcast"] = {
        "message": broadcast_message,
        "recipients": recipients,
        "target_tag": target_tag,
        "sender_id": update.effective_user.id,
    }
    await update.message.reply_text(
        f"📢 *Preview Broadcast*\n\n"
        f"🎯 Target: {target_label} ({len(recipients)} orang)\n\n"
        f"📝 Mesej:\n{broadcast_message}\n\n"
        f"Taip *HANTAR* untuk confirm.",
        parse_mode="Markdown"
    )


# ─── PHOTO HANDLER ───────────────────────────────────────────────────────────

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    get_or_create_user(telegram_id, update.effective_user.first_name)
    caption = update.message.caption or ""
    processing_msg = await update.message.reply_text("🔍 Menganalisis makanan... Sila tunggu sebentar.")
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()
        result = analyze_meal(bytes(image_bytes), caption=caption)
        if "error" in result:
            await processing_msg.edit_text(f"❌ {result['error']}")
            return
        save_meal(telegram_id, result)
        today_meals = get_today_meals(telegram_id)
        totals = sum_nutrition(today_meals)
        user = get_user(telegram_id)
        cal_target = user.get("daily_cal_target", 2000) if user else 2000
        streak = user.get("streak_count", 0) if user else 0
        items = result.get("items_detected", [])
        items_str = ", ".join(items) if items else "-"
        conf = result.get("confidence", "medium")
        conf_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(conf, "🟡")
        caption_note = f"\n📝 Nota: _{caption}_" if caption else ""
        reply = (
            f"✅ *Meal Dilog!*\n\n"
            f"🍽️ *{result.get('meal_name', 'Makanan')}*\n"
            f"📏 Porsi: {result.get('portion', '-')}\n"
            f"{conf_emoji} Keyakinan AI: {conf}"
            f"{caption_note}\n\n"
            f"*Nilai Nutrisi:*\n"
            f"🔥 Kalori: *{result.get('calories', 0)} kcal*\n"
            f"💪 Protein: {result.get('protein_g', 0)}g\n"
            f"🍚 Karbohidrat: {result.get('carbs_g', 0)}g\n"
            f"🥑 Lemak: {result.get('fat_g', 0)}g\n"
            f"🌿 Serat: {result.get('fiber_g', 0)}g\n"
            f"🧂 Sodium: {result.get('sodium_mg', 0)}mg\n\n"
            f"📦 Item: {items_str}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 *Total Hari Ini ({len(today_meals)} hidangan):*\n"
            f"🔥 {totals['calories']} / {cal_target} kal\n"
            f"🔥 Streak: {streak} hari\n\n"
            f"Taip /today untuk ringkasan penuh."
        )
        await processing_msg.edit_text(reply, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error handle_photo: {e}")
        await processing_msg.edit_text("❌ Ralat semasa memproses gambar. Cuba hantar semula.")


# ─── TEXT HANDLER ────────────────────────────────────────────────────────────

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    text = update.message.text.strip().upper()

    if text == "YA" and "pending_undo" in context.user_data:
        meal_id = context.user_data.pop("pending_undo")
        success = delete_meal(meal_id)
        if success:
            await update.message.reply_text("✅ Meal berjaya dipadam.")
        else:
            await update.message.reply_text("❌ Gagal padam. Cuba lagi.")
        return

    if text == "HANTAR" and is_admin(telegram_id) and "pending_broadcast" in context.user_data:
        pending = context.user_data.pop("pending_broadcast")
        recipients = pending["recipients"]
        broadcast_message = pending["message"]
        target_tag = pending["target_tag"]
        sender_id = pending["sender_id"]
        status_msg = await update.message.reply_text(f"📤 Menghantar kepada {len(recipients)} orang...")
        success_count = 0
        fail_count = 0
        for uid in recipients:
            try:
                await context.bot.send_message(
                    chat_id=uid,
                    text=f"📢 *Mesej dari Klinik Etika*\n\n{broadcast_message}",
                    parse_mode="Markdown"
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Broadcast fail to {uid}: {e}")
                fail_count += 1
        save_broadcast_log(sender_id, broadcast_message, target_tag, success_count)
        await status_msg.edit_text(
            f"✅ *Broadcast Selesai!*\n\n"
            f"✔️ Berjaya: {success_count} orang\n"
            f"❌ Gagal: {fail_count} orang",
            parse_mode="Markdown"
        )
        return

    if "pending_undo" in context.user_data:
        context.user_data.pop("pending_undo")
        await update.message.reply_text("↩️ Undo dibatalkan.")
        return

    if "pending_broadcast" in context.user_data and is_admin(telegram_id):
        context.user_data.pop("pending_broadcast")
        await update.message.reply_text("📢 Broadcast dibatalkan.")
        return

    await update.message.reply_text(
        "📸 Hantar gambar makanan untuk log meal.\nTaip /help untuk senarai commands.",
        parse_mode="Markdown"
    )


# ─── SCHEDULERS ──────────────────────────────────────────────────────────────

async def send_nightly_summary(app):
    logger.info("Sending nightly summary...")
    user_ids = get_all_telegram_ids()
    for telegram_id in user_ids:
        try:
            meals = get_today_meals(telegram_id)
            if not meals:
                continue
            summary = build_daily_summary(telegram_id)
            await app.bot.send_message(
                chat_id=telegram_id,
                text=f"🌙 *Auto Ringkasan Malam*\n\n{summary}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Error nightly summary {telegram_id}: {e}")


async def send_weekly_report(app):
    logger.info("Sending weekly report...")
    user_ids = get_all_telegram_ids()
    for telegram_id in user_ids:
        try:
            summary = build_weekly_summary(telegram_id)
            await app.bot.send_message(
                chat_id=telegram_id,
                text=f"📅 *Laporan Mingguan*\n\n{summary}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Error weekly report {telegram_id}: {e}")


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    async def post_init(application):
        scheduler = AsyncIOScheduler(timezone="Asia/Kuala_Lumpur")
        scheduler.add_job(send_nightly_summary, "cron", hour=21, minute=0, args=[application])
        scheduler.add_job(send_weekly_report, "cron", day_of_week="sun", hour=20, minute=0, args=[application])
        scheduler.start()
        logger.info("🤖 Food Tracker Bot started!")

    app = Application.builder().token(TELEGRAM_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("today", cmd_today))
    app.add_handler(CommandHandler("week", cmd_week))
    app.add_handler(CommandHandler("target", cmd_target))
    app.add_handler(CommandHandler("undo", cmd_undo))
    app.add_handler(CommandHandler("air", cmd_air))
    app.add_handler(CommandHandler("log", cmd_log))
    app.add_handler(CommandHandler("mytags", cmd_mytags))
    app.add_handler(CommandHandler("broadcast", cmd_broadcast))
    app.add_handler(CommandHandler("tag", cmd_tag))
    app.add_handler(CommandHandler("removetag", cmd_removetag))
    app.add_handler(CommandHandler("users", cmd_users))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
