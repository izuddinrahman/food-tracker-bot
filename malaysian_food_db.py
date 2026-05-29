"""
Malaysian Food Nutrition Database
Curated list of 100+ common Malaysian dishes with accurate nutrition data.
Sources: MOH Malaysia Food Composition Table, MyFCD, USDA, local research.
All values are per typical serving.
"""

MALAYSIAN_FOOD_DB = {
    # =========================================================================
    # NASI & RICE DISHES
    # =========================================================================
    "nasi putih": {
        "serving": "1 pinggan (200g)",
        "calories": 260, "protein_g": 5.4, "carbs_g": 56, "fat_g": 0.6,
        "fiber_g": 0.8, "sodium_mg": 5,
        "tags": ["nasi", "rice", "staple"]
    },
    "nasi lemak biasa": {
        "serving": "1 bungkus (300g)",
        "calories": 400, "protein_g": 12, "carbs_g": 45, "fat_g": 18,
        "fiber_g": 2, "sodium_mg": 700,
        "tags": ["nasi", "lemak", "coconut", "sambal", "ikan bilis"]
    },
    "nasi lemak ayam goreng": {
        "serving": "1 pinggan (350g)",
        "calories": 650, "protein_g": 30, "carbs_g": 50, "fat_g": 35,
        "fiber_g": 2, "sodium_mg": 900,
        "tags": ["nasi", "lemak", "ayam", "fried chicken"]
    },
    "nasi lemak sambal kerang": {
        "serving": "1 pinggan (330g)",
        "calories": 500, "protein_g": 22, "carbs_g": 48, "fat_g": 22,
        "fiber_g": 2, "sodium_mg": 850,
        "tags": ["nasi", "lemak", "kerang", "cockles"]
    },
    "nasi goreng biasa": {
        "serving": "1 pinggan (300g)",
        "calories": 500, "protein_g": 15, "carbs_g": 65, "fat_g": 18,
        "fiber_g": 2, "sodium_mg": 900,
        "tags": ["nasi", "goreng", "fried rice"]
    },
    "nasi goreng kampung": {
        "serving": "1 pinggan (300g)",
        "calories": 480, "protein_g": 16, "carbs_g": 60, "fat_g": 16,
        "fiber_g": 3, "sodium_mg": 850,
        "tags": ["nasi", "goreng", "kampung"]
    },
    "nasi goreng ayam": {
        "serving": "1 pinggan (350g)",
        "calories": 600, "protein_g": 25, "carbs_g": 65, "fat_g": 22,
        "fiber_g": 2, "sodium_mg": 950,
        "tags": ["nasi", "goreng", "ayam", "chicken fried rice"]
    },
    "nasi goreng cina": {
        "serving": "1 pinggan (300g)",
        "calories": 530, "protein_g": 14, "carbs_g": 62, "fat_g": 22,
        "fiber_g": 2, "sodium_mg": 1000,
        "tags": ["nasi", "goreng", "cina", "chinese"]
    },
    "nasi goreng seafood": {
        "serving": "1 pinggan (320g)",
        "calories": 550, "protein_g": 22, "carbs_g": 62, "fat_g": 20,
        "fiber_g": 2, "sodium_mg": 950,
        "tags": ["nasi", "goreng", "seafood", "udang"]
    },
    "nasi goreng daging": {
        "serving": "1 pinggan (330g)",
        "calories": 580, "protein_g": 24, "carbs_g": 62, "fat_g": 22,
        "fiber_g": 2, "sodium_mg": 920,
        "tags": ["nasi", "goreng", "daging", "beef"]
    },
    "nasi goreng pattaya": {
        "serving": "1 pinggan (350g)",
        "calories": 620, "protein_g": 20, "carbs_g": 58, "fat_g": 28,
        "fiber_g": 2, "sodium_mg": 800,
        "tags": ["nasi", "goreng", "pattaya", "telur"]
    },
    "nasi ayam": {
        "serving": "1 pinggan (350g)",
        "calories": 550, "protein_g": 28, "carbs_g": 55, "fat_g": 20,
        "fiber_g": 1, "sodium_mg": 800,
        "tags": ["nasi", "ayam", "chicken rice"]
    },
    "nasi ayam goreng": {
        "serving": "1 pinggan (350g)",
        "calories": 650, "protein_g": 30, "carbs_g": 55, "fat_g": 30,
        "fiber_g": 1, "sodium_mg": 850,
        "tags": ["nasi", "ayam", "fried", "chicken rice"]
    },
    "nasi kandar": {
        "serving": "1 pinggan (400g)",
        "calories": 750, "protein_g": 28, "carbs_g": 70, "fat_g": 35,
        "fiber_g": 3, "sodium_mg": 1200,
        "tags": ["nasi", "kandar", "curry", "banjir"]
    },
    "nasi briyani ayam": {
        "serving": "1 pinggan (380g)",
        "calories": 650, "protein_g": 30, "carbs_g": 70, "fat_g": 24,
        "fiber_g": 2, "sodium_mg": 900,
        "tags": ["nasi", "briyani", "ayam", "indian"]
    },
    "nasi minyak": {
        "serving": "1 pinggan (250g)",
        "calories": 450, "protein_g": 8, "carbs_g": 55, "fat_g": 20,
        "fiber_g": 1, "sodium_mg": 400,
        "tags": ["nasi", "minyak", "wedding", "kenduri"]
    },
    "nasi dagang": {
        "serving": "1 pinggan (300g)",
        "calories": 500, "protein_g": 18, "carbs_g": 60, "fat_g": 18,
        "fiber_g": 2, "sodium_mg": 600,
        "tags": ["nasi", "dagang", "terengganu", "kelantan", "fish"]
    },
    "nasi kerabu": {
        "serving": "1 pinggan (250g)",
        "calories": 350, "protein_g": 15, "carbs_g": 45, "fat_g": 8,
        "fiber_g": 4, "sodium_mg": 500,
        "tags": ["nasi", "kerabu", "salad", "kelantan"]
    },
    "ketupat": {
        "serving": "2 biji (200g)",
        "calories": 280, "protein_g": 5, "carbs_g": 60, "fat_g": 1,
        "fiber_g": 1, "sodium_mg": 10,
        "tags": ["ketupat", "rice cake", "raya"]
    },
    "lemang": {
        "serving": "2 potong (150g)",
        "calories": 350, "protein_g": 4, "carbs_g": 50, "fat_g": 12,
        "fiber_g": 1, "sodium_mg": 200,
        "tags": ["lemang", "bamboo", "glutinous", "raya"]
    },

    # =========================================================================
    # MEE & NOODLES
    # =========================================================================
    "mee goreng mamak": {
        "serving": "1 pinggan (350g)",
        "calories": 580, "protein_g": 15, "carbs_g": 70, "fat_g": 24,
        "fiber_g": 3, "sodium_mg": 1100,
        "tags": ["mee", "goreng", "mamak", "fried noodle"]
    },
    "mee goreng biasa": {
        "serving": "1 pinggan (300g)",
        "calories": 520, "protein_g": 14, "carbs_g": 65, "fat_g": 20,
        "fiber_g": 2, "sodium_mg": 950,
        "tags": ["mee", "goreng", "fried noodle"]
    },
    "mee rebus": {
        "serving": "1 mangkuk (400g)",
        "calories": 480, "protein_g": 16, "carbs_g": 60, "fat_g": 16,
        "fiber_g": 3, "sodium_mg": 1000,
        "tags": ["mee", "rebus", "boiled noodle", "gravy"]
    },
    "mee kari": {
        "serving": "1 mangkuk (400g)",
        "calories": 550, "protein_g": 18, "carbs_g": 55, "fat_g": 24,
        "fiber_g": 3, "sodium_mg": 950,
        "tags": ["mee", "kari", "curry noodle"]
    },
    "mee sup": {
        "serving": "1 mangkuk (400g)",
        "calories": 380, "protein_g": 15, "carbs_g": 50, "fat_g": 10,
        "fiber_g": 2, "sodium_mg": 800,
        "tags": ["mee", "sup", "soup noodle"]
    },
    "kuey teow goreng": {
        "serving": "1 pinggan (300g)",
        "calories": 520, "protein_g": 12, "carbs_g": 60, "fat_g": 24,
        "fiber_g": 2, "sodium_mg": 950,
        "tags": ["kuey teow", "goreng", "fried flat noodle", "char kway teow"]
    },
    "char kuey teow": {
        "serving": "1 pinggan (300g)",
        "calories": 550, "protein_g": 14, "carbs_g": 58, "fat_g": 26,
        "fiber_g": 2, "sodium_mg": 900,
        "tags": ["kuey teow", "char", "fried", "penang", "cockles"]
    },
    "kuey teow sup": {
        "serving": "1 mangkuk (400g)",
        "calories": 350, "protein_g": 14, "carbs_g": 48, "fat_g": 8,
        "fiber_g": 1, "sodium_mg": 750,
        "tags": ["kuey teow", "sup", "soup"]
    },
    "bihun goreng": {
        "serving": "1 pinggan (280g)",
        "calories": 420, "protein_g": 10, "carbs_g": 55, "fat_g": 16,
        "fiber_g": 2, "sodium_mg": 800,
        "tags": ["bihun", "goreng", "rice vermicelli", "fried"]
    },
    "bihun sup": {
        "serving": "1 mangkuk (400g)",
        "calories": 320, "protein_g": 12, "carbs_g": 48, "fat_g": 6,
        "fiber_g": 2, "sodium_mg": 700,
        "tags": ["bihun", "sup", "soup"]
    },
    "laksa penang": {
        "serving": "1 mangkuk (400g)",
        "calories": 420, "protein_g": 18, "carbs_g": 50, "fat_g": 12,
        "fiber_g": 3, "sodium_mg": 850,
        "tags": ["laksa", "penang", "asam", "fish", "noodle"]
    },
    "laksa sarawak": {
        "serving": "1 mangkuk (400g)",
        "calories": 500, "protein_g": 22, "carbs_g": 50, "fat_g": 20,
        "fiber_g": 2, "sodium_mg": 900,
        "tags": ["laksa", "sarawak", "coconut", "curry"]
    },
    "laksa nyonya": {
        "serving": "1 mangkuk (400g)",
        "calories": 550, "protein_g": 20, "carbs_g": 45, "fat_g": 30,
        "fiber_g": 2, "sodium_mg": 850,
        "tags": ["laksa", "nyonya", "lemak", "curry", "coconut"]
    },
    "laksa johor": {
        "serving": "1 pinggan (400g)",
        "calories": 570, "protein_g": 24, "carbs_g": 55, "fat_g": 25,
        "fiber_g": 3, "sodium_mg": 800,
        "tags": ["laksa", "johor", "spaghetti", "fish"]
    },
    "maggi goreng": {
        "serving": "1 pinggan (300g)",
        "calories": 500, "protein_g": 12, "carbs_g": 55, "fat_g": 24,
        "fiber_g": 2, "sodium_mg": 1200,
        "tags": ["maggi", "goreng", "instant noodle", "mamak"]
    },
    "maggi sup": {
        "serving": "1 mangkuk (400g)",
        "calories": 380, "protein_g": 10, "carbs_g": 45, "fat_g": 16,
        "fiber_g": 1, "sodium_mg": 1500,
        "tags": ["maggi", "sup", "instant noodle"]
    },
    "wantan mee": {
        "serving": "1 pinggan (300g)",
        "calories": 450, "protein_g": 16, "carbs_g": 55, "fat_g": 15,
        "fiber_g": 2, "sodium_mg": 800,
        "tags": ["wantan", "mee", "dumpling", "noodle"]
    },
    "spaghetti bolognese": {
        "serving": "1 pinggan (350g)",
        "calories": 550, "protein_g": 22, "carbs_g": 65, "fat_g": 18,
        "fiber_g": 3, "sodium_mg": 700,
        "tags": ["spaghetti", "bolognese", "pasta", "western"]
    },
    "spaghetti carbonara": {
        "serving": "1 pinggan (350g)",
        "calories": 650, "protein_g": 20, "carbs_g": 60, "fat_g": 32,
        "fiber_g": 2, "sodium_mg": 650,
        "tags": ["spaghetti", "carbonara", "pasta", "western"]
    },

    # =========================================================================
    # LAUK & PROTEIN
    # =========================================================================
    "ayam goreng": {
        "serving": "1 ketul (120g)",
        "calories": 320, "protein_g": 28, "carbs_g": 10, "fat_g": 18,
        "fiber_g": 0, "sodium_mg": 400,
        "tags": ["ayam", "goreng", "fried chicken"]
    },
    "ayam goreng kfc": {
        "serving": "1 ketul (dada, 150g)",
        "calories": 390, "protein_g": 32, "carbs_g": 12, "fat_g": 22,
        "fiber_g": 0, "sodium_mg": 750,
        "tags": ["ayam", "goreng", "kfc", "fried chicken", "fast food"]
    },
    "ayam goreng mcd": {
        "serving": "1 ketul (dada, 130g)",
        "calories": 350, "protein_g": 30, "carbs_g": 10, "fat_g": 20,
        "fiber_g": 0, "sodium_mg": 650,
        "tags": ["ayam", "goreng", "mcd", "mcdonalds", "fried chicken"]
    },
    "ayam masak merah": {
        "serving": "1 ketul + kuah (150g)",
        "calories": 300, "protein_g": 26, "carbs_g": 12, "fat_g": 14,
        "fiber_g": 1, "sodium_mg": 500,
        "tags": ["ayam", "masak merah", "tomato"]
    },
    "ayam masak kicap": {
        "serving": "1 ketul + kuah (150g)",
        "calories": 310, "protein_g": 28, "carbs_g": 14, "fat_g": 12,
        "fiber_g": 1, "sodium_mg": 650,
        "tags": ["ayam", "kicap", "soy sauce"]
    },
    "ayam masak lemak cili api": {
        "serving": "1 ketul + kuah (150g)",
        "calories": 340, "protein_g": 27, "carbs_g": 8, "fat_g": 20,
        "fiber_g": 1, "sodium_mg": 450,
        "tags": ["ayam", "lemak", "cili api", "coconut"]
    },
    "rendang ayam": {
        "serving": "1 ketul + kuah (130g)",
        "calories": 350, "protein_g": 26, "carbs_g": 10, "fat_g": 22,
        "fiber_g": 2, "sodium_mg": 550,
        "tags": ["rendang", "ayam", "coconut", "dry curry"]
    },
    "rendang daging": {
        "serving": "2 ketul + kuah (150g)",
        "calories": 420, "protein_g": 30, "carbs_g": 8, "fat_g": 28,
        "fiber_g": 2, "sodium_mg": 500,
        "tags": ["rendang", "daging", "beef", "coconut"]
    },
    "kari ayam": {
        "serving": "1 ketul + kuah (180g)",
        "calories": 320, "protein_g": 25, "carbs_g": 10, "fat_g": 18,
        "fiber_g": 2, "sodium_mg": 600,
        "tags": ["kari", "ayam", "curry chicken"]
    },
    "kari ikan": {
        "serving": "1 ketul + kuah (180g)",
        "calories": 250, "protein_g": 22, "carbs_g": 6, "fat_g": 14,
        "fiber_g": 1, "sodium_mg": 550,
        "tags": ["kari", "ikan", "fish curry"]
    },
    "kari kepala ikan": {
        "serving": "1 mangkuk (300g)",
        "calories": 400, "protein_g": 30, "carbs_g": 10, "fat_g": 24,
        "fiber_g": 2, "sodium_mg": 700,
        "tags": ["kari", "ikan", "fish head", "curry"]
    },
    "ikan goreng": {
        "serving": "1 ekor kecil (100g)",
        "calories": 200, "protein_g": 24, "carbs_g": 2, "fat_g": 10,
        "fiber_g": 0, "sodium_mg": 300,
        "tags": ["ikan", "goreng", "fried fish"]
    },
    "ikan bakar": {
        "serving": "1 ekor (150g)",
        "calories": 220, "protein_g": 30, "carbs_g": 2, "fat_g": 10,
        "fiber_g": 0, "sodium_mg": 350,
        "tags": ["ikan", "bakar", "grilled fish"]
    },
    "sambal ikan bilis": {
        "serving": "3 sudu besar (50g)",
        "calories": 150, "protein_g": 12, "carbs_g": 10, "fat_g": 6,
        "fiber_g": 1, "sodium_mg": 500,
        "tags": ["sambal", "ikan bilis", "anchovy"]
    },
    "sambal udang": {
        "serving": "3 sudu besar (60g)",
        "calories": 180, "protein_g": 14, "carbs_g": 8, "fat_g": 8,
        "fiber_g": 1, "sodium_mg": 450,
        "tags": ["sambal", "udang", "shrimp", "prawn"]
    },
    "sambal sotong": {
        "serving": "3 sudu besar (60g)",
        "calories": 160, "protein_g": 15, "carbs_g": 6, "fat_g": 6,
        "fiber_g": 1, "sodium_mg": 480,
        "tags": ["sambal", "sotong", "squid"]
    },
    "telur goreng": {
        "serving": "1 biji (55g)",
        "calories": 120, "protein_g": 7, "carbs_g": 1, "fat_g": 10,
        "fiber_g": 0, "sodium_mg": 150,
        "tags": ["telur", "goreng", "fried egg"]
    },
    "telur dadar": {
        "serving": "1 keping (100g dari 2 biji)",
        "calories": 220, "protein_g": 14, "carbs_g": 3, "fat_g": 16,
        "fiber_g": 0, "sodium_mg": 300,
        "tags": ["telur", "dadar", "omelette"]
    },
    "telur rebus": {
        "serving": "1 biji (50g)",
        "calories": 78, "protein_g": 6, "carbs_g": 1, "fat_g": 5,
        "fiber_g": 0, "sodium_mg": 62,
        "tags": ["telur", "rebus", "boiled egg"]
    },
    "sate ayam": {
        "serving": "10 cucuk (200g)",
        "calories": 450, "protein_g": 35, "carbs_g": 20, "fat_g": 22,
        "fiber_g": 1, "sodium_mg": 600,
        "tags": ["sate", "ayam", "satay", "chicken"]
    },
    "sate daging": {
        "serving": "10 cucuk (200g)",
        "calories": 500, "protein_g": 38, "carbs_g": 18, "fat_g": 28,
        "fiber_g": 1, "sodium_mg": 580,
        "tags": ["sate", "daging", "satay", "beef"]
    },
    "sup ayam": {
        "serving": "1 mangkuk (300g)",
        "calories": 200, "protein_g": 20, "carbs_g": 10, "fat_g": 8,
        "fiber_g": 2, "sodium_mg": 700,
        "tags": ["sup", "ayam", "chicken soup"]
    },
    "sup tulang": {
        "serving": "1 mangkuk (350g)",
        "calories": 280, "protein_g": 22, "carbs_g": 10, "fat_g": 14,
        "fiber_g": 1, "sodium_mg": 750,
        "tags": ["sup", "tulang", "bone soup"]
    },
    "daging masak kicap": {
        "serving": "4 ketul + kuah (120g)",
        "calories": 280, "protein_g": 24, "carbs_g": 10, "fat_g": 14,
        "fiber_g": 0, "sodium_mg": 600,
        "tags": ["daging", "kicap", "beef", "soy sauce"]
    },
    "tauhu goreng": {
        "serving": "2 keping (80g)",
        "calories": 140, "protein_g": 10, "carbs_g": 6, "fat_g": 8,
        "fiber_g": 1, "sodium_mg": 200,
        "tags": ["tauhu", "goreng", "tofu", "fried"]
    },
    "tempe goreng": {
        "serving": "2 keping (60g)",
        "calories": 140, "protein_g": 10, "carbs_g": 8, "fat_g": 7,
        "fiber_g": 2, "sodium_mg": 180,
        "tags": ["tempe", "goreng", "fried"]
    },

    # =========================================================================
    # ROTI & BREAD
    # =========================================================================
    "roti canai": {
        "serving": "1 keping (80g)",
        "calories": 300, "protein_g": 7, "carbs_g": 40, "fat_g": 11,
        "fiber_g": 1, "sodium_mg": 400,
        "tags": ["roti", "canai", "flatbread", "mamak"]
    },
    "roti canai banjir": {
        "serving": "1 keping + kuah (150g)",
        "calories": 420, "protein_g": 12, "carbs_g": 45, "fat_g": 20,
        "fiber_g": 1, "sodium_mg": 700,
        "tags": ["roti", "canai", "banjir", "curry", "gravy"]
    },
    "roti telur": {
        "serving": "1 keping (120g)",
        "calories": 380, "protein_g": 14, "carbs_g": 38, "fat_g": 16,
        "fiber_g": 1, "sodium_mg": 420,
        "tags": ["roti", "telur", "egg"]
    },
    "roti sardin": {
        "serving": "1 keping (130g)",
        "calories": 400, "protein_g": 16, "carbs_g": 40, "fat_g": 18,
        "fiber_g": 1, "sodium_mg": 500,
        "tags": ["roti", "sardin"]
    },
    "roti tisu": {
        "serving": "1 keping (100g)",
        "calories": 380, "protein_g": 5, "carbs_g": 45, "fat_g": 18,
        "fiber_g": 0, "sodium_mg": 350,
        "tags": ["roti", "tisu", "crispy"]
    },
    "roti bakar": {
        "serving": "2 keping + butter (80g)",
        "calories": 250, "protein_g": 6, "carbs_g": 30, "fat_g": 12,
        "fiber_g": 1, "sodium_mg": 300,
        "tags": ["roti", "bakar", "toast", "kopitiam"]
    },
    "roti john": {
        "serving": "1 biji (200g)",
        "calories": 500, "protein_g": 18, "carbs_g": 45, "fat_g": 24,
        "fiber_g": 2, "sodium_mg": 650,
        "tags": ["roti", "john", "sandwich", "egg"]
    },
    "capati": {
        "serving": "1 keping (50g)",
        "calories": 150, "protein_g": 4, "carbs_g": 28, "fat_g": 2,
        "fiber_g": 2, "sodium_mg": 100,
        "tags": ["capati", "chapati", "indian", "flatbread"]
    },
    "tosai": {
        "serving": "1 keping (80g)",
        "calories": 160, "protein_g": 4, "carbs_g": 32, "fat_g": 1,
        "fiber_g": 1, "sodium_mg": 200,
        "tags": ["tosai", "dosa", "indian", "fermented"]
    },
    "tosai masala": {
        "serving": "1 keping (150g)",
        "calories": 280, "protein_g": 6, "carbs_g": 40, "fat_g": 8,
        "fiber_g": 3, "sodium_mg": 350,
        "tags": ["tosai", "masala", "potato"]
    },
    "naan": {
        "serving": "1 keping (100g)",
        "calories": 300, "protein_g": 9, "carbs_g": 48, "fat_g": 6,
        "fiber_g": 2, "sodium_mg": 350,
        "tags": ["naan", "indian", "bread"]
    },
    "roti kaya": {
        "serving": "2 keping (80g)",
        "calories": 280, "protein_g": 5, "carbs_g": 40, "fat_g": 10,
        "fiber_g": 1, "sodium_mg": 250,
        "tags": ["roti", "kaya", "toast", "coconut jam", "kopitiam"]
    },

    # =========================================================================
    # KUIH & SNACKS
    # =========================================================================
    "karipap": {
        "serving": "1 biji (50g)",
        "calories": 150, "protein_g": 3, "carbs_g": 16, "fat_g": 8,
        "fiber_g": 1, "sodium_mg": 200,
        "tags": ["karipap", "curry puff"]
    },
    "kuih lapis": {
        "serving": "2 keping (40g)",
        "calories": 100, "protein_g": 1, "carbs_g": 22, "fat_g": 1,
        "fiber_g": 0, "sodium_mg": 50,
        "tags": ["kuih", "lapis", "steamed"]
    },
    "onde-onde": {
        "serving": "3 biji (60g)",
        "calories": 180, "protein_g": 2, "carbs_g": 28, "fat_g": 6,
        "fiber_g": 1, "sodium_mg": 30,
        "tags": ["onde", "onde-onde", "keledek", "gula melaka"]
    },
    "kuih seri muka": {
        "serving": "1 potong (60g)",
        "calories": 160, "protein_g": 3, "carbs_g": 22, "fat_g": 6,
        "fiber_g": 1, "sodium_mg": 50,
        "tags": ["kuih", "seri muka", "glutinous", "coconut"]
    },
    "cucur udang": {
        "serving": "3 biji (90g)",
        "calories": 250, "protein_g": 6, "carbs_g": 28, "fat_g": 12,
        "fiber_g": 1, "sodium_mg": 350,
        "tags": ["cucur", "udang", "fritter", "prawn"]
    },
    "pisang goreng": {
        "serving": "2 biji (80g)",
        "calories": 200, "protein_g": 2, "carbs_g": 28, "fat_g": 8,
        "fiber_g": 2, "sodium_mg": 100,
        "tags": ["pisang", "goreng", "banana fritter"]
    },
    "cekodok": {
        "serving": "3 biji (80g)",
        "calories": 220, "protein_g": 3, "carbs_g": 30, "fat_g": 8,
        "fiber_g": 2, "sodium_mg": 150,
        "tags": ["cekodok", "jemput-jemput", "banana ball"]
    },
    "keropok lekor": {
        "serving": "5 ketul (100g)",
        "calories": 200, "protein_g": 10, "carbs_g": 22, "fat_g": 6,
        "fiber_g": 0, "sodium_mg": 400,
        "tags": ["keropok", "lekor", "fish cracker", "terengganu"]
    },
    "popia goreng": {
        "serving": "2 biji (100g)",
        "calories": 220, "protein_g": 5, "carbs_g": 22, "fat_g": 12,
        "fiber_g": 2, "sodium_mg": 300,
        "tags": ["popia", "goreng", "spring roll"]
    },
    "murtabak": {
        "serving": "1 keping (200g)",
        "calories": 550, "protein_g": 18, "carbs_g": 45, "fat_g": 30,
        "fiber_g": 2, "sodium_mg": 700,
        "tags": ["murtabak", "stuffed flatbread", "mamak"]
    },

    # =========================================================================
    # DRINKS
    # =========================================================================
    "teh tarik": {
        "serving": "1 gelas (250ml)",
        "calories": 120, "protein_g": 3, "carbs_g": 16, "fat_g": 4,
        "fiber_g": 0, "sodium_mg": 50,
        "tags": ["teh", "tarik", "tea", "milk", "mamak"]
    },
    "teh o": {
        "serving": "1 cawan (200ml)",
        "calories": 5, "protein_g": 0, "carbs_g": 1, "fat_g": 0,
        "fiber_g": 0, "sodium_mg": 5,
        "tags": ["teh", "o", "tea", "sugarless"]
    },
    "teh o ais": {
        "serving": "1 gelas (300ml)",
        "calories": 80, "protein_g": 0, "carbs_g": 20, "fat_g": 0,
        "fiber_g": 0, "sodium_mg": 10,
        "tags": ["teh", "o", "ais", "iced tea", "sweet"]
    },
    "teh ais": {
        "serving": "1 gelas (300ml)",
        "calories": 140, "protein_g": 3, "carbs_g": 18, "fat_g": 4,
        "fiber_g": 0, "sodium_mg": 50,
        "tags": ["teh", "ais", "iced milk tea"]
    },
    "kopi o": {
        "serving": "1 cawan (200ml)",
        "calories": 5, "protein_g": 0, "carbs_g": 1, "fat_g": 0,
        "fiber_g": 0, "sodium_mg": 5,
        "tags": ["kopi", "o", "black coffee"]
    },
    "kopi susu": {
        "serving": "1 cawan (200ml)",
        "calories": 100, "protein_g": 3, "carbs_g": 10, "fat_g": 4,
        "fiber_g": 0, "sodium_mg": 50,
        "tags": ["kopi", "susu", "coffee", "milk"]
    },
    "kopi ais": {
        "serving": "1 gelas (300ml)",
        "calories": 150, "protein_g": 3, "carbs_g": 18, "fat_g": 5,
        "fiber_g": 0, "sodium_mg": 50,
        "tags": ["kopi", "ais", "iced coffee"]
    },
    "milo ais": {
        "serving": "1 gelas (300ml)",
        "calories": 200, "protein_g": 5, "carbs_g": 30, "fat_g": 5,
        "fiber_g": 1, "sodium_mg": 80,
        "tags": ["milo", "ais", "chocolate malt"]
    },
    "milo panas": {
        "serving": "1 cawan (200ml)",
        "calories": 180, "protein_g": 5, "carbs_g": 28, "fat_g": 4,
        "fiber_g": 1, "sodium_mg": 70,
        "tags": ["milo", "panas", "hot chocolate", "malt"]
    },
    "sirap bandung": {
        "serving": "1 gelas (300ml)",
        "calories": 180, "protein_g": 2, "carbs_g": 30, "fat_g": 4,
        "fiber_g": 0, "sodium_mg": 40,
        "tags": ["sirap", "bandung", "rose syrup", "milk"]
    },
    "sirap limau": {
        "serving": "1 gelas (300ml)",
        "calories": 120, "protein_g": 0, "carbs_g": 30, "fat_g": 0,
        "fiber_g": 0, "sodium_mg": 20,
        "tags": ["sirap", "limau", "lime", "syrup"]
    },
    "air kelapa": {
        "serving": "1 biji (300ml)",
        "calories": 60, "protein_g": 1, "carbs_g": 14, "fat_g": 0,
        "fiber_g": 1, "sodium_mg": 100,
        "tags": ["air", "kelapa", "coconut water"]
    },
    "jus tembikai": {
        "serving": "1 gelas (300ml, tanpa gula)",
        "calories": 90, "protein_g": 1, "carbs_g": 22, "fat_g": 0,
        "fiber_g": 1, "sodium_mg": 5,
        "tags": ["jus", "tembikai", "watermelon"]
    },
    "jus oren": {
        "serving": "1 gelas (250ml)",
        "calories": 110, "protein_g": 2, "carbs_g": 25, "fat_g": 0,
        "fiber_g": 1, "sodium_mg": 5,
        "tags": ["jus", "oren", "orange juice"]
    },

    # =========================================================================
    # FAST FOOD (MALAYSIA)
    # =========================================================================
    "burger biasa": {
        "serving": "1 biji (ramly style, 150g)",
        "calories": 400, "protein_g": 18, "carbs_g": 35, "fat_g": 20,
        "fiber_g": 1, "sodium_mg": 650,
        "tags": ["burger", "ramly", "fast food"]
    },
    "burger double": {
        "serving": "1 biji (200g)",
        "calories": 600, "protein_g": 35, "carbs_g": 38, "fat_g": 32,
        "fiber_g": 1, "sodium_mg": 850,
        "tags": ["burger", "double", "ramly"]
    },
    "french fries": {
        "serving": "1 hidangan besar (150g)",
        "calories": 450, "protein_g": 5, "carbs_g": 50, "fat_g": 24,
        "fiber_g": 4, "sodium_mg": 350,
        "tags": ["fries", "kentang", "goreng", "fast food"]
    },
    "pizza 1 slice": {
        "serving": "1 keping (120g)",
        "calories": 300, "protein_g": 12, "carbs_g": 35, "fat_g": 12,
        "fiber_g": 1, "sodium_mg": 600,
        "tags": ["pizza", "fast food"]
    },
    "nugget ayam": {
        "serving": "6 ketul (100g)",
        "calories": 280, "protein_g": 14, "carbs_g": 15, "fat_g": 16,
        "fiber_g": 1, "sodium_mg": 450,
        "tags": ["nugget", "ayam", "chicken nugget"]
    },

    # =========================================================================
    # DESSERTS
    # =========================================================================
    "ais kacang": {
        "serving": "1 mangkuk (300g)",
        "calories": 280, "protein_g": 4, "carbs_g": 50, "fat_g": 5,
        "fiber_g": 2, "sodium_mg": 50,
        "tags": ["ais", "kacang", "abc", "ice", "dessert"]
    },
    "cendol": {
        "serving": "1 mangkuk (300g)",
        "calories": 250, "protein_g": 2, "carbs_g": 45, "fat_g": 6,
        "fiber_g": 1, "sodium_mg": 30,
        "tags": ["cendol", "coconut", "gula melaka", "dessert"]
    },
    "bubur cha cha": {
        "serving": "1 mangkuk (250g)",
        "calories": 300, "protein_g": 4, "carbs_g": 40, "fat_g": 12,
        "fiber_g": 3, "sodium_mg": 100,
        "tags": ["bubur", "cha cha", "coconut", "dessert"]
    },
    "pulut mangga": {
        "serving": "1 hidangan (200g)",
        "calories": 350, "protein_g": 4, "carbs_g": 50, "fat_g": 14,
        "fiber_g": 2, "sodium_mg": 50,
        "tags": ["pulut", "mangga", "mango sticky rice"]
    },
    "apam balik": {
        "serving": "1 keping (120g)",
        "calories": 350, "protein_g": 8, "carbs_g": 40, "fat_g": 16,
        "fiber_g": 1, "sodium_mg": 150,
        "tags": ["apam", "balik", "pancake", "peanut"]
    },
    "donat": {
        "serving": "1 biji (50g)",
        "calories": 200, "protein_g": 3, "carbs_g": 25, "fat_g": 10,
        "fiber_g": 1, "sodium_mg": 100,
        "tags": ["donat", "donut", "fried dough"]
    },

    # =========================================================================
    # VEGETABLES & SIDES
    # =========================================================================
    "sayur campur goreng": {
        "serving": "1 pinggan kecil (100g)",
        "calories": 80, "protein_g": 3, "carbs_g": 10, "fat_g": 3,
        "fiber_g": 3, "sodium_mg": 300,
        "tags": ["sayur", "goreng", "vegetables", "stir fry"]
    },
    "kangkung goreng belacan": {
        "serving": "1 pinggan kecil (100g)",
        "calories": 100, "protein_g": 3, "carbs_g": 8, "fat_g": 5,
        "fiber_g": 2, "sodium_mg": 400,
        "tags": ["kangkung", "belacan", "water spinach"]
    },
    "ulam": {
        "serving": "1 pinggan kecil (80g)",
        "calories": 30, "protein_g": 2, "carbs_g": 6, "fat_g": 0,
        "fiber_g": 3, "sodium_mg": 20,
        "tags": ["ulam", "raw vegetables", "salad"]
    },
    "acar": {
        "serving": "2 sudu besar (30g)",
        "calories": 40, "protein_g": 0, "carbs_g": 8, "fat_g": 1,
        "fiber_g": 1, "sodium_mg": 100,
        "tags": ["acar", "pickle"]
    },
    "sambal belacan": {
        "serving": "1 sudu besar (15g)",
        "calories": 30, "protein_g": 1, "carbs_g": 4, "fat_g": 1,
        "fiber_g": 0, "sodium_mg": 200,
        "tags": ["sambal", "belacan", "shrimp paste chili"]
    },
}


def search_food(query: str) -> dict | None:
    """Cari makanan dalam database. Return dict atau None kalau tak jumpa."""
    q = query.lower().strip()

    # Direct match
    if q in MALAYSIAN_FOOD_DB:
        return MALAYSIAN_FOOD_DB[q]

    # Partial match on keys
    for key in MALAYSIAN_FOOD_DB:
        if q in key or key in q:
            return MALAYSIAN_FOOD_DB[key]

    # Tag search
    q_words = set(q.split())
    for key, data in MALAYSIAN_FOOD_DB.items():
        tags = " ".join(data.get("tags", []))
        if any(word in tags for word in q_words):
            return MALAYSIAN_FOOD_DB[key]

    return None


def lookup_meal(items: list) -> tuple[dict, list]:
    """
    Match list of food items detected by AI to DB.
    Returns (combined_nutrition, unmatched_items).
    """
    total = {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0,
             "fiber_g": 0, "sodium_mg": 0}
    matched = []
    unmatched = []

    for item in items:
        result = search_food(item)
        if result:
            for key in total:
                total[key] += result.get(key, 0)
            matched.append(item)
        else:
            unmatched.append(item)

    if not matched:
        return None, unmatched

    return total, unmatched
