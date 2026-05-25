import anthropic
import base64
import json
import re
import os
from dotenv import load_dotenv

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
        return data

    except json.JSONDecodeError:
        return {"error": "AI tidak dapat parse response. Cuba hantar gambar lain."}
    except Exception as e:
        return {"error": f"Analisis gagal: {str(e)}"}
