from database import get_today_meals, get_week_meals, get_user, sum_nutrition, get_today_water
from datetime import datetime, date


def progress_bar(current: float, target: float, length: int = 10) -> str:
    if target <= 0:
        return "▱" * length
    ratio = min(current / target, 1.0)
    filled = round(ratio * length)
    bar = "▰" * filled + "▱" * (length - filled)
    pct = round(ratio * 100)
    return f"{bar} {pct}%"


def water_bar(current_ml: int, target_ml: int = 2000, length: int = 10) -> str:
    glasses_current = current_ml / 250
    glasses_target = target_ml / 250
    return progress_bar(glasses_current, glasses_target, length)


def format_time(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%I:%M %p")
    except Exception:
        return "-"


def streak_emoji(streak: int) -> str:
    if streak >= 30:
        return "🏆"
    elif streak >= 14:
        return "🔥"
    elif streak >= 7:
        return "⚡"
    elif streak >= 3:
        return "✨"
    return "🌱"


def build_daily_summary(telegram_id: int) -> str:
    user = get_user(telegram_id)
    meals = get_today_meals(telegram_id)
    water_ml = get_today_water(telegram_id)
    today = date.today().strftime("%d %B %Y")

    streak = user.get("streak_count", 0) if user else 0
    s_emoji = streak_emoji(streak)

    if not meals:
        return (
            f"📋 *Ringkasan {today}*\n\n"
            "Tiada meal dilog hari ini.\n"
            "Snap gambar makanan anda untuk mula track! 📸"
        )

    totals = sum_nutrition(meals)
    cal_target = user.get("daily_cal_target", 2000) if user else 2000
    protein_target = user.get("daily_protein_target", 50) if user else 50

    cal_bar = progress_bar(totals["calories"], cal_target)
    protein_bar = progress_bar(totals["protein_g"], protein_target)
    w_bar = water_bar(water_ml)

    water_glasses = water_ml // 250
    water_target_glasses = 8

    meal_lines = ""
    for i, m in enumerate(meals, 1):
        t = format_time(m.get("logged_at", ""))
        meal_lines += f"  {i}. {m.get('meal_name', '-')} ({t}) — {m.get('calories', 0)} kal\n"

    sodium_warning = ""
    if totals["sodium_mg"] > 2000:
        sodium_warning = "\n⚠️ *Amaran:* Sodium tinggi hari ini! Kurangkan garam.\n"

    summary = (
        f"📊 *Ringkasan Pemakanan*\n"
        f"📅 {today}\n"
        f"{s_emoji} Streak: *{streak} hari berturut*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔥 *Kalori:* {totals['calories']} / {cal_target} kcal\n"
        f"{cal_bar}\n\n"
        f"💪 *Protein:* {totals['protein_g']:.1f}g / {protein_target}g\n"
        f"{protein_bar}\n\n"
        f"💧 *Air:* {water_glasses} / {water_target_glasses} gelas ({water_ml}ml)\n"
        f"{w_bar}\n\n"
        f"🍚 *Karbohidrat:* {totals['carbs_g']:.1f}g\n"
        f"🥑 *Lemak:* {totals['fat_g']:.1f}g\n"
        f"🌿 *Serat:* {totals['fiber_g']:.1f}g\n"
        f"🧂 *Sodium:* {totals['sodium_mg']:.0f}mg\n"
        f"{sodium_warning}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🍽️ *Meal Log ({len(meals)} hidangan):*\n"
        f"{meal_lines}"
    )
    return summary


def build_weekly_summary(telegram_id: int) -> str:
    meals = get_week_meals(telegram_id)
    user = get_user(telegram_id)
    streak = user.get("streak_count", 0) if user else 0

    if not meals:
        return "Tiada data untuk 7 hari lepas. Mula log meal anda! 📸"

    by_date = {}
    for m in meals:
        d = m["logged_at"][:10]
        by_date.setdefault(d, []).append(m)

    lines = ""
    for d, day_meals in sorted(by_date.items()):
        totals = sum_nutrition(day_meals)
        day_label = datetime.strptime(d, "%Y-%m-%d").strftime("%a, %d %b")
        lines += f"  {day_label}: {totals['calories']} kal | P:{totals['protein_g']:.0f}g\n"

    all_totals = sum_nutrition(meals)
    days = len(by_date)
    avg_cal = round(all_totals["calories"] / days) if days > 0 else 0
    avg_protein = round(all_totals["protein_g"] / days, 1) if days > 0 else 0
    s_emoji = streak_emoji(streak)

    summary = (
        f"📈 *Ringkasan 7 Hari*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📆 *Hari Dilog:* {days}/7\n"
        f"{s_emoji} *Streak Semasa:* {streak} hari\n"
        f"🔥 *Avg Kalori/hari:* {avg_cal} kcal\n"
        f"💪 *Avg Protein/hari:* {avg_protein}g\n\n"
        f"*Detail harian:*\n{lines}"
    )
    return summary
