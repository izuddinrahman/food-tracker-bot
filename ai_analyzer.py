import anthropic
import base64
import json
import re
import os
from dotenv import load_dotenv
from malaysian_food_db import search_food, lookup_meal

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def analyze_meal(image_bytes: bytes, caption: str = "") -> dict:
    """
    Hantar gambar meal ke Claude Vision.
    caption — nota tambahan dari user (contoh: 'separuh je makan', 'tanpa nasi')
    Return dict dengan nutrition info.
    """
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    caption_note = f"\nNota dari user: \"{caption}\"" if caption.strip() else ""

    prompt = f"""Kamu adalah pakar nutrisi. Analisis makanan dalam gambar ini.
{caption_note}

Kenal pasti semua makanan yang kelihatan dan anggaran porsi.
Kalau ada nota dari user, ambil kira dalam pengiraan (contoh: kalau user kata 'separuh je', kurangkan kalori separuh).
Kemudian hitung jumlah nilai nutrisi kesemuanya.

Balas HANYA dengan JSON sahaja, tiada teks lain, dalam format berikut:
{{
  "meal_name": "nama ringkas makanan (contoh: Nasi Lemak dengan Ayam)",
  "portion": "anggaran saiz (contoh: 1 pinggan sederhana)",
  "calories": 500,
  "protein_g": 25,
  "carbs_g": 60,
  "fat_g": 18,
  "fiber_g": 3,
  "sodium_mg": 800,
  "confidence": "high",
  "items_detected": ["nasi", "sambal", "ikan bilis", "telur"],
  "notes": "sebarang nota penting tentang makanan ini"
}}

Nilai confidence: "high" (jelas nampak), "medium" (agak jelas), "low" (tidak pasti).
Kalau bukan gambar makanan, balas: {{"error": "Bukan gambar makanan"}}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )

        raw_text = response.content[0].text.strip()
        raw_text = re.sub(r"```json\s*", "", raw_text)
        raw_text = re.sub(r"```\s*", "", raw_text)
        raw_text = raw_text.strip()

        data = json.loads(raw_text)
        data["raw_response"] = raw_text

        # Cross-check with Malaysian food database for accuracy
        data = _cross_check_with_db(data)

        return data

    except json.JSONDecodeError:
        return {"error": "AI tidak dapat parse response. Cuba hantar gambar lain."}
    except Exception as e:
        return {"error": f"Analisis gagal: {str(e)}"}


def _cross_check_with_db(ai_result: dict) -> dict:
    """
    Cross-check AI nutrition estimates with Malaysian food database.
    If we find matching items in our DB, use the more accurate DB values.
    Falls back to AI estimates for unrecognized items.
    """
    items = ai_result.get("items_detected", [])
    if not items:
        return ai_result

    db_totals, unmatched = lookup_meal(items)

    if db_totals:
        # Blend: use DB for matched items, keep AI estimate for unmatched
        match_ratio = len(items) - len(unmatched)
        total_items = len(items)

        if total_items > 0 and match_ratio > 0:
            # Weighted blend: prefer DB when available
            if len(unmatched) == 0:
                # All items matched — fully use DB values
                ai_result["calories"] = db_totals["calories"]
                ai_result["protein_g"] = db_totals["protein_g"]
                ai_result["carbs_g"] = db_totals["carbs_g"]
                ai_result["fat_g"] = db_totals["fat_g"]
                ai_result["fiber_g"] = db_totals["fiber_g"]
                ai_result["sodium_mg"] = db_totals["sodium_mg"]
                ai_result["confidence"] = "high"
                ai_result["notes"] = (ai_result.get("notes", "") +
                    " [✅ Data nutrisi dari pangkalan data makanan Malaysia]").strip()
            else:
                # Partial match — blend DB + AI
                db_weight = match_ratio / total_items
                ai_weight = 1 - db_weight

                ai_result["calories"] = round(db_totals["calories"] * db_weight +
                    ai_result.get("calories", 0) * ai_weight)
                ai_result["protein_g"] = round(db_totals["protein_g"] * db_weight +
                    ai_result.get("protein_g", 0) * ai_weight, 1)
                ai_result["carbs_g"] = round(db_totals["carbs_g"] * db_weight +
                    ai_result.get("carbs_g", 0) * ai_weight, 1)
                ai_result["fat_g"] = round(db_totals["fat_g"] * db_weight +
                    ai_result.get("fat_g", 0) * ai_weight, 1)
                ai_result["fiber_g"] = round(db_totals["fiber_g"] * db_weight +
                    ai_result.get("fiber_g", 0) * ai_weight, 1)
                ai_result["sodium_mg"] = round(db_totals["sodium_mg"] * db_weight +
                    ai_result.get("sodium_mg", 0) * ai_weight)
                ai_result["confidence"] = "high" if db_weight > 0.5 else "medium"
                ai_result["notes"] = (ai_result.get("notes", "") +
                    f" [🔄 {match_ratio}/{total_items} item dipadankan dengan DB]").strip()

    return ai_result
