from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Frontend bilan aloqa uchun

# OpenAI API kaliti
openai.api_key = os.getenv('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')

# Dars jadvali ma'lumotlari
SCHEDULE_DATA = {
    "avm1-25a": {
        "monday": [
            "Ma'naviyat soati Abdulatipova S",
            "Rus tili Xayitboyeva M 102",
            "Ona tili O'rinboyev F 404", 
            "Matematika Shukurova G 408"
        ],
        "tuesday": [
            "Tarbiya Djumaboyeva D 206",
            "Kompyuter arxitekturasi Ofis jihozlariga tex xiz Xusanov S 213",
            "Web dasturlash Xidirov A 215",
            "Ingliz tili Xayitboyeva R Abdulatipova S 414/411"
        ],
        "wednesday": [
            "MATEMATIKA Shukurova G 408",
            "TARIX Ne'majionov I 407", 
            "INGLIZ TILI Xamidova R/ Abdulatipova S 414/411",
            "MATEMATIKA Shukurova G 408"
        ],
        "thursday": [
            "Matematika Shukurova G 408",
            "Informatika Abloqulovi Shukurov 203/213",
            "CH.Q.B.T Yoldoshov F 102",
            "Ingliz tili Yamidova/Abdulatipova S 414411"
        ],
        "friday": [
            "Ing tili Xamidova R/Abdulatipova M 414411",
            "Ing tili Xamidova R/Abdulatipova M 414411", 
            "Fizika Shobutayeva D 201",
            ""
        ]
    },
    # ... barcha guruhlarni shu yerda qo'shing
}

# O'qituvchilar ma'lumotlari
TEACHERS_DATA = [
    {
        "name": "Rashidov Anvar",
        "position": "Direktor", 
        "specialty": "Energetika",
        "experience": "25 yil"
    },
    {
        "name": "Ismailova Gulnora",
        "position": "O'qituvchi",
        "specialty": "Elektr texnikasi", 
        "experience": "15 yil"
    }
]

@app.route('/')
def home():
    return jsonify({
        "message": "Shirin Energetika Texnikumi AI Bot API",
        "status": "running",
        "endpoints": {
            "/chat": "AI chat endpoint (POST)",
            "/schedule": "Dars jadvali (GET)",
            "/teachers": "O'qituvchilar ro'yxati (GET)" 
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Xabar bo'sh"}), 400
        
        # GPT-3 dan javob olish
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": """Siz Shirin Energetika Texnikumi yordamchi botsiz. 
                    Quyidagi ma'lumotlar asosida javob bering:
                    
                    DARS JADVALI:
                    - AVM-1-25A: Dushanba - Ma'naviyat, Rus tili, Ona tili, Matematika
                    - Boshqa guruhlar ham mavjud
                    
                    O'QITUVCHILAR:
                    - Rashidov Anvar (Direktor, Energetika, 25 yil tajriba)
                    - Ismailova Gulnora (Elektr texnikasi, 15 yil tajriba)
                    
                    ALOQA:
                    - Manzil: Sirdaryo viloyati, Shirin shahri
                    - Tel: +998 67 123 45 67
                    - Email: info@shirinenergetika.uz
                    
                    O'zbek tilida, do'stona va aniq javob bering."""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        bot_reply = response.choices[0].message.content
        
        return jsonify({
            "reply": bot_reply,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Xatolik yuz berdi: {str(e)}",
            "reply": "Kechirasiz, texnik xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
        }), 500

@app.route('/schedule', methods=['GET'])
def get_schedule():
    """Barcha dars jadvalini olish"""
    return jsonify(SCHEDULE_DATA)

@app.route('/schedule/<group>', methods=['GET'])
def get_group_schedule(group):
    """Maxsus guruhning dars jadvali"""
    if group in SCHEDULE_DATA:
        return jsonify(SCHEDULE_DATA[group])
    else:
        return jsonify({"error": "Guruh topilmadi"}), 404

@app.route('/teachers', methods=['GET']) 
def get_teachers():
    """O'qituvchilar ro'yxati"""
    return jsonify(TEACHERS_DATA)

@app.route('/health', methods=['GET'])
def health_check():
    """Server holatini tekshirish"""
    return jsonify({"status": "healthy", "service": "Shirin Energetika API"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
