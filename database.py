import os
from datetime import datetime, date, timedelta
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


# ─── USER ────────────────────────────────────────────────────────────────────

def get_or_create_user(telegram_id: int, name: str) -> dict:
    result = supabase.table("food_users") \
        .select("*") \
        .eq("telegram_id", telegram_id) \
        .execute()

    if result.data:
        return result.data[0]

    new_user = {
        "telegram_id": telegram_id,
        "name": name,
        "daily_cal_target": 2000,
        "daily_protein_target": 50,
        "tags": "",
        "streak_count": 0,
    }
    result = supabase.table("food_users").insert(new_user).execute()
    return result.data[0]


def get_user(telegram_id: int) -> dict | None:
    result = supabase.table("food_users") \
        .select("*") \
        .eq("telegram_id", telegram_id) \
        .execute()
    return result.data[0] if result.data else None


def get_all_users() -> list:
    result = supabase.table("food_users").select("*").execute()
    return result.data


def get_all_telegram_ids() -> list:
    result = supabase.table("food_users").select("telegram_id").execute()
    return [row["telegram_id"] for row in result.data]


def get_users_by_tag(tag: str) -> list:
    """Dapatkan users yang ada tag tertentu."""
    result = supabase.table("food_users").select("*").execute()
    tag_lower = tag.lower().strip()
    return [
        u for u in result.data
        if tag_lower in [t.strip().lower() for t in (u.get("tags") or "").split(",") if t.strip()]
    ]


def update_user_targets(telegram_id: int, cal_target: int, protein_target: int):
    supabase.table("food_users") \
        .update({"daily_cal_target": cal_target, "daily_protein_target": protein_target}) \
        .eq("telegram_id", telegram_id) \
        .execute()


def add_tag_to_user(telegram_id: int, tag: str):
    """Tambah tag kepada user."""
    user = get_user(telegram_id)
    if not user:
        return False
    current_tags = [t.strip().lower() for t in (user.get("tags") or "").split(",") if t.strip()]
    tag_lower = tag.lower().strip()
    if tag_lower not in current_tags:
        current_tags.append(tag_lower)
    new_tags = ", ".join(current_tags)
    supabase.table("food_users") \
        .update({"tags": new_tags}) \
        .eq("telegram_id", telegram_id) \
        .execute()
    return True


def remove_tag_from_user(telegram_id: int, tag: str):
    """Buang tag dari user."""
    user = get_user(telegram_id)
    if not user:
        return False
    current_tags = [t.strip().lower() for t in (user.get("tags") or "").split(",") if t.strip()]
    tag_lower = tag.lower().strip()
    current_tags = [t for t in current_tags if t != tag_lower]
    new_tags = ", ".join(current_tags)
    supabase.table("food_users") \
        .update({"tags": new_tags}) \
        .eq("telegram_id", telegram_id) \
        .execute()
    return True


# ─── STREAK ──────────────────────────────────────────────────────────────────

def update_streak(telegram_id: int):
    """Update streak selepas meal berjaya dilog."""
    user = get_user(telegram_id)
    if not user:
        return

    today = date.today()
    last_log = user.get("last_log_date")

    if last_log:
        last_log_date = date.fromisoformat(str(last_log))
        if last_log_date == today:
            return  # Dah log hari ni, streak tak berubah
        elif last_log_date == today - timedelta(days=1):
            new_streak = (user.get("streak_count") or 0) + 1
        else:
            new_streak = 1  # Reset
    else:
        new_streak = 1

    supabase.table("food_users") \
        .update({"streak_count": new_streak, "last_log_date": today.isoformat()}) \
        .eq("telegram_id", telegram_id) \
        .execute()


# ─── MEAL LOG ────────────────────────────────────────────────────────────────

def save_meal(telegram_id: int, meal_data: dict) -> dict:
    record = {
        "telegram_id": telegram_id,
        "meal_name": meal_data.get("meal_name", "Unknown"),
        "portion": meal_data.get("portion", "-"),
        "calories": int(meal_data.get("calories", 0)),
        "protein_g": float(meal_data.get("protein_g", 0)),
        "carbs_g": float(meal_data.get("carbs_g", 0)),
        "fat_g": float(meal_data.get("fat_g", 0)),
        "fiber_g": float(meal_data.get("fiber_g", 0)),
        "sodium_mg": float(meal_data.get("sodium_mg", 0)),
        "confidence": meal_data.get("confidence", "medium"),
        "raw_ai_response": meal_data.get("raw_response", ""),
    }
    result = supabase.table("food_log").insert(record).execute()
    update_streak(telegram_id)
    return result.data[0]


def get_last_meal(telegram_id: int) -> dict | None:
    """Dapatkan meal paling terkini."""
    result = supabase.table("food_log") \
        .select("*") \
        .eq("telegram_id", telegram_id) \
        .order("logged_at", desc=True) \
        .limit(1) \
        .execute()
    return result.data[0] if result.data else None


def delete_meal(meal_id: str) -> bool:
    """Padam meal by ID."""
    try:
        supabase.table("food_log").delete().eq("id", meal_id).execute()
        return True
    except Exception:
        return False


def get_today_meals(telegram_id: int) -> list:
    today = date.today().isoformat()
    result = supabase.table("food_log") \
        .select("*") \
        .eq("telegram_id", telegram_id) \
        .gte("logged_at", f"{today}T00:00:00") \
        .lte("logged_at", f"{today}T23:59:59") \
        .order("logged_at") \
        .execute()
    return result.data


def get_week_meals(telegram_id: int) -> list:
    week_ago = (date.today() - timedelta(days=6)).isoformat()
    result = supabase.table("food_log") \
        .select("*") \
        .eq("telegram_id", telegram_id) \
        .gte("logged_at", f"{week_ago}T00:00:00") \
        .order("logged_at") \
        .execute()
    return result.data


# ─── WATER LOG ───────────────────────────────────────────────────────────────

def save_water(telegram_id: int, amount_ml: int) -> dict:
    record = {"telegram_id": telegram_id, "amount_ml": amount_ml}
    result = supabase.table("water_log").insert(record).execute()
    return result.data[0]


def get_today_water(telegram_id: int) -> int:
    """Return jumlah air hari ini dalam ml."""
    today = date.today().isoformat()
    result = supabase.table("water_log") \
        .select("amount_ml") \
        .eq("telegram_id", telegram_id) \
        .gte("logged_at", f"{today}T00:00:00") \
        .lte("logged_at", f"{today}T23:59:59") \
        .execute()
    return sum(row["amount_ml"] for row in result.data)


# ─── BROADCAST LOG ───────────────────────────────────────────────────────────

def save_broadcast_log(sent_by: int, message: str, target_tag: str, recipient_count: int):
    supabase.table("broadcast_log").insert({
        "sent_by": sent_by,
        "message": message,
        "target_tag": target_tag,
        "recipient_count": recipient_count,
    }).execute()


# ─── NUTRITION HELPER ────────────────────────────────────────────────────────

def sum_nutrition(meals: list) -> dict:
    return {
        "calories": sum(m.get("calories") or 0 for m in meals),
        "protein_g": sum(m.get("protein_g") or 0 for m in meals),
        "carbs_g": sum(m.get("carbs_g") or 0 for m in meals),
        "fat_g": sum(m.get("fat_g") or 0 for m in meals),
        "fiber_g": sum(m.get("fiber_g") or 0 for m in meals),
        "sodium_mg": sum(m.get("sodium_mg") or 0 for m in meals),
    }
