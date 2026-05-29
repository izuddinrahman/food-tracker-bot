import os
from datetime import datetime, date, timedelta
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


# === USER =====================================================================

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
        "weight_kg": None,
        "height_cm": None,
        "age": None,
        "gender": None,
        "onboarding_complete": False,
    }
    result = supabase.table("food_users").insert(new_user).execute()
    return result.data[0]


def update_user_profile(telegram_id: int, weight_kg: float, height_cm: float,
                        age: int, gender: str):
    """Update user profile and auto-calculate TDEE + calorie target."""
    tdee = calculate_tdee(weight_kg, height_cm, age, gender)
    # Weight loss target: TDEE - 500 cal (~0.5kg/week)
    cal_target = max(1200, tdee - 500)
    # Protein: 1.6g per kg body weight
    protein_target = round(weight_kg * 1.6, 1)

    supabase.table("food_users") \
        .update({
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "age": age,
            "gender": gender,
            "daily_cal_target": cal_target,
            "daily_protein_target": protein_target,
            "onboarding_complete": True,
        }) \
        .eq("telegram_id", telegram_id) \
        .execute()
    return {"tdee": tdee, "cal_target": cal_target, "protein_target": protein_target}


def reset_onboarding(telegram_id: int):
    """Reset onboarding flag so user can re-enter profile info."""
    supabase.table("food_users") \
        .update({"onboarding_complete": False}) \
        .eq("telegram_id", telegram_id) \
        .execute()


def calculate_tdee(weight_kg: float, height_cm: float, age: int,
                   gender: str, activity: str = "sedentary") -> int:
    """
    Mifflin-St Jeor BMR × activity factor.
    Activity: sedentary(1.2), light(1.375), moderate(1.55), active(1.725)
    """
    g = gender.lower().strip()
    if g in ("lelaki", "male", "m", "l"):
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    factors = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
    return round(bmr * factors.get(activity, 1.2))


def save_weight(telegram_id: int, weight_kg: float) -> dict:
    """Log weight + update current in profile."""
    supabase.table("food_users") \
        .update({"weight_kg": weight_kg}) \
        .eq("telegram_id", telegram_id) \
        .execute()
    result = supabase.table("weight_log").insert({
        "telegram_id": telegram_id, "weight_kg": weight_kg
    }).execute()
    return result.data[0] if result.data else {}


def get_weight_history(telegram_id: int, days: int = 30) -> list:
    since = (date.today() - timedelta(days=days)).isoformat()
    result = supabase.table("weight_log") \
        .select("*") \
        .eq("telegram_id", telegram_id) \
        .gte("logged_at", f"{since}T00:00:00") \
        .order("logged_at") \
        .execute()
    return result.data


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
    user = get_user(telegram_id)
    if not user: return False
    current = [t.strip().lower() for t in (user.get("tags") or "").split(",") if t.strip()]
    tl = tag.lower().strip()
    if tl not in current: current.append(tl)
    supabase.table("food_users") \
        .update({"tags": ", ".join(current)}) \
        .eq("telegram_id", telegram_id) \
        .execute()
    return True


def remove_tag_from_user(telegram_id: int, tag: str):
    user = get_user(telegram_id)
    if not user: return False
    current = [t.strip().lower() for t in (user.get("tags") or "").split(",") if t.strip()]
    tl = tag.lower().strip()
    current = [t for t in current if t != tl]
    supabase.table("food_users") \
        .update({"tags": ", ".join(current)}) \
        .eq("telegram_id", telegram_id) \
        .execute()
    return True


# === STREAK ===================================================================

def update_streak(telegram_id: int):
    user = get_user(telegram_id)
    if not user: return
    today = date.today()
    last_log = user.get("last_log_date")
    if last_log:
        ld = date.fromisoformat(str(last_log))
        if ld == today: return
        elif ld == today - timedelta(days=1): new_streak = (user.get("streak_count") or 0) + 1
        else: new_streak = 1
    else:
        new_streak = 1
    supabase.table("food_users") \
        .update({"streak_count": new_streak, "last_log_date": today.isoformat()}) \
        .eq("telegram_id", telegram_id) \
        .execute()


# === MEAL LOG =================================================================

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
    result = supabase.table("food_log") \
        .select("*") \
        .eq("telegram_id", telegram_id) \
        .order("logged_at", desc=True) \
        .limit(1) \
        .execute()
    return result.data[0] if result.data else None


def delete_meal(meal_id: str) -> bool:
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


# === WATER LOG ================================================================

def save_water(telegram_id: int, amount_ml: int) -> dict:
    result = supabase.table("water_log").insert({
        "telegram_id": telegram_id, "amount_ml": amount_ml
    }).execute()
    return result.data[0]


def get_today_water(telegram_id: int) -> int:
    today = date.today().isoformat()
    result = supabase.table("water_log") \
        .select("amount_ml") \
        .eq("telegram_id", telegram_id) \
        .gte("logged_at", f"{today}T00:00:00") \
        .lte("logged_at", f"{today}T23:59:59") \
        .execute()
    return sum(row["amount_ml"] for row in result.data)


# === BROADCAST ================================================================

def save_broadcast_log(sent_by: int, message: str, target_tag: str, recipient_count: int):
    supabase.table("broadcast_log").insert({
        "sent_by": sent_by, "message": message,
        "target_tag": target_tag, "recipient_count": recipient_count,
    }).execute()


# === NUTRITION HELPER =========================================================

def sum_nutrition(meals: list) -> dict:
    return {
        "calories": sum(m.get("calories") or 0 for m in meals),
        "protein_g": sum(m.get("protein_g") or 0 for m in meals),
        "carbs_g": sum(m.get("carbs_g") or 0 for m in meals),
        "fat_g": sum(m.get("fat_g") or 0 for m in meals),
        "fiber_g": sum(m.get("fiber_g") or 0 for m in meals),
        "sodium_mg": sum(m.get("sodium_mg") or 0 for m in meals),
    }
