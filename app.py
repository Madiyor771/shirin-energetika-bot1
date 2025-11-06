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
openai.api_key = os.getenv('OPENAI_API_KEY')

# To'liq dars jadvali ma'lumotlari
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
    "avm1-25b": {
        "monday": [
            "Ma'naviyat soati Xusanov S",
            "Ingliz tili Abdulatipova SAbdullaeva M 410411",
            "Kompyuter arxitekturasi va ofis jihozlariga teknik xizmat korsatish Shonazarov J106",
            "Jismonly Tarbiya Azimjonov S"
        ],
        "tuesday": [
            "Ingliz tili Abdulatipova S Abdullaeva M 410/411",
            "Rus tili Xayitboyeva M 401",
            "Fizika Shobutayeva D 201",
            ""
        ],
        "wednesday": [
            "TARIX Ne'majionov I 407",
            "INGLIZ TILI Abdulatipova S/Abdullayeva 410/411",
            "INFORMATIKA Abloquilov A/Shukurov A 213/203",
            ""
        ],
        "thursday": [
            "Kompyuter arkitekturasi Ofis jihozlariga teknik xizmat ko'rsatish O'A Xusanov S",
            "Matematika Shukurova G 408",
            "Informatika Abloqulovi Shukurov 203/213",
            "CH.Q.B.T Yoldoshov F 102"
        ],
        "friday": [
            "Ona tili Sayfulaeva B 409",
            "Jismoniy tarbiya Azimjonov S",
            "Ingliz tili Abdulatipova Sabdullaeva M 410411",
            ""
        ]
    },
    "avm1-25rus": {
        "monday": [
            "Ma'naviyat soati Xamidova R",
            "Ingliz tili Xamidova R Mamatqulova M 414315",
            "Tarix Nemajonov I 407",
            "Elektr stansiya uskunalarini ta mirlash Xudoyqulov X 204"
        ],
        "tuesday": [
            "Matematika Shukurova G 408",
            "Arxitektura personal kompyuter Shonazarov J 106",
            "Ingliz tili Xamidova R Malpatsion o'q M 414/315",
            ""
        ],
        "wednesday": [
            "O'QUV AMALIYOT SHONAZAROV J 106",
            "O'QUV AMALIYOT SHONAZAROV J 106",
            "INGLIZ TILI Xayitova B /Tolibjonova M 403/413",
            ""
        ],
        "thursday": [
            "Inglis tili Yamidova Mamatqulova 414315",
            "Teknikaviy Chizmachilik Xudoyqulov X 204",
            "Ing tili Xayitova B/Tolibjonova M 403/413",
            "Matematika Shukurova G 408"
        ],
        "friday": [
            "CH.Q.B.T Yoldoshov F 102",
            "Fizika Shobutayeva D 201",
            "Inglis tili Xamidova Mamatqulova 414315",
            ""
        ]
    },
    "avm2-24": {
        "monday": [
            "Ma'naviyat soati Xayitova B",
            "Web dasturlash Xidirov A 215",
            "Ingliz tili Xayitova B Tolibjonova M 403413",
            "Informatika Abloqulov A Shukurov A 203213"
        ],
        "tuesday": [
            "Fizika Shobutayeva D 201",
            "CH.Q.B.T Yoldoshov F 206",
            "Kompyuter tizimlarining dasturiy ta'minoti Xusanov S 213",
            "Matematika Shukurova G 408"
        ],
        "wednesday": [
            "D.X.A Djumaboyeva D 206",
            "ONA TILI O'rinboyev F 404",
            "Axborot xavfsizligi Xusanov S 215",
            ""
        ],
        "thursday": [
            "Dasturlash asoslari Xidirov A 215",
            "Tarix Nematjonov I 407",
            "Biznes Asoslari Ashurov Usrolov J 409",
            ""
        ],
        "friday": [
            "Web dasturlash Xidirov A",
            "Shaxsiy kompyuter arxitekturasi va ofis jihozlariga texnik xizmat ko'rsatish O'A Ablogulov A 214",
            "Ochoobi programma Shonazarov J 106",
            ""
        ]
    },
    "avm2-24rus": {
        "monday": [
            "Ma'naviyat soati Shonazarov J",
            "Informatika Abloqulov A Shonazarov J 214106",
            "Rus tili Xayitboyeva M 202 2 korpus",
            "Ona tili O'rinboyev F 404"
        ],
        "tuesday": [
            "Ingliz tili Xayitova B Tolibjonova M 403/413",
            "Biznes asoslari Isroilov J Ashurov S 409",
            "Dasturlash asoslari Shonazarov J 106",
            "Rus tili Xayitboyeva M 401"
        ],
        "wednesday": [
            "JISMONIY TARBIYA AZIMJONOV S",
            "MATEMATIKA Shukurova G 408",
            "TARIX Ne'majionov I 407",
            ""
        ],
        "thursday": [
            "D.H.A Djumaboyeva D 106",
            "Информатичоная Безопасност Shonazarov J 106",
            "Программа Обеспечение Shonazarov J 106",
            "Ona tili O'rinboyev F Sayfullaeva B 404/409"
        ],
        "friday": [
            "Web programma Shonazarov J 106",
            "Web programma Shonazarov J 106",
            "Elektr stansiya uskunalarini ta mirlash Xudoyqulov X 204",
            "Matematika Shukurova G/408"
        ]
    },
    "esu1-25": {
        "monday": [
            "Ma'naviyat soati Xidirov A",
            "Elektr stansiya uskunalarini ta mirlash Xudoyqulov X 204",
            "Mehnat Muhofazasi O'sarov Sh",
            "Ma'naviyat soati Mamatqulova M"
        ],
        "tuesday": [
            "Rus tili Xayitboyeva M 401",
            "Jismoniy tarbiya Azimjonov S",
            "Konstruksion materiallar Xudoyqulov X 204",
            ""
        ],
        "wednesday": [
            "CH.Q.B.T Yoldoshov F 102",
            "Konstruksion materialar Xudoyquilov X 204",
            "MATEMATIKA Shukurova G 408",
            ""
        ],
        "thursday": [
            "Elektr stansiya uskunalariini tamirlash Xudoyqulov X 204",
            "Ing tili Xayitova B/Tolibjonova M 403/413",
            "Elektr texnika Isrollov Z 206",
            ""
        ],
        "friday": [
            "Ing tili Xayitova B/Tolibjonova M 403413",
            "Tarix Nematjonov I 407",
            "",
            ""
        ]
    },
    "qtem1-25": {
        "monday": [
            "Qayta tiklanuvchi energiya manbalarini yig'ish o'matish va ishga tushirish ishlari O'A 206",
            "Qayta tiklanuvchi energiya manbalarini yig'ish o'matish va ishga tushirish ishlari O'A 206",
            "CH.Q.B.T Yo'ldoshov F",
            ""
        ],
        "tuesday": [
            "Qayta tiklanuvchi energiya manbalarini yig'ish o'rnatish va ishga tushirish ishlari O'A",
            "Yig'ish o'rnatish va ishga tushirish ishlari O'A",
            "Ingliz tili Xayitova B Tolibjonova M 403/413",
            ""
        ],
        "wednesday": [
            "",
            "",
            "",
            ""
        ],
        "thursday": [
            "Qayta tiklanuvchi energiya manbalari qurilmalariini yig'ish o'rnatish va ishga tushirish O'A",
            "Metrologiya va Standardlashtirish va Sertifikatlashtirish Egamberdiyev S 107",
            "Inglis tili Yamidova Mamatqulova 414315",
            ""
        ],
        "friday": [
            "Q.T.E.M.T.X.KO'R Toshtemirov A",
            "Bio va Geotermal energetika Xudoyqulov X 204",
            "Q.T.E.A.M.E.A.E.Q Isroilov Z 106",
            ""
        ]
    },
    "em1-25": {
        "monday": [
            "Ma'naviyat soati Nematjonov I",
            "Ingliz tili Xayitova B Tolibjonova M 403413",
            "Elektr texnika Isrollov Z 206",
            "Rus tili Xayitboyeva M 102"
        ],
        "tuesday": [
            "Amaliy chizma Xudoyqulov X 204",
            "Tarix Nematjonov I 407",
            "Informatika Ablogulov Shukurov 203/213",
            "Fizika Shobutayeva D 201"
        ],
        "wednesday": [
            "ONA TILI O'rinboyev F 404",
            "MEHNAT MUHOFAZASI O'sarov SH 102",
            "",
            ""
        ],
        "thursday": [
            "Elektr texnika materialar Isrollov Z 206",
            "Ing tili Abdulatipova S Mamatqulova M 411315",
            "Tarbiya Nematjonov I 407",
            ""
        ],
        "friday": [
            "Inormatika Ablogulov A Shukurov A 213214",
            "Rus tili Xayitboyeva M 102",
            "Elektr stansiya elektr tarmoqlari Isroilov Z 206",
            ""
        ]
    },
    "p1-25": {
        "monday": [
            "Ma'naviyat soati Isroilov J",
            "Elektr texnika Isrollov Z 206",
            "Texnikaviy Chizmachili Kudoyqulov X 204",
            "Ingliz tili Abdulatipova S Mamatqulova M 410315"
        ],
        "tuesday": [
            "Rus tili Xayitboyeva M 401",
            "Amaliy chizma Xudoyqulov X 204",
            "",
            ""
        ],
        "wednesday": [
            "O'quv Amaliyot Matqosimov A 107",
            "",
            "MEHNAT MUHOFAZASI O'sarov SH 102",
            ""
        ],
        "thursday": [
            "Ona tili O'rinboyev F 404",
            "",
            "",
            ""
        ],
        "friday": [
            "Avtomatik va yarim avtomatik payvandlash texnologiyasi Egamberdiyev S",
            "Matematika Shukurova G 408",
            "Tarix Nematjonov I 407",
            ""
        ]
    },
    "at1-25": {
        "monday": [
            "Ma'naviyat soati Yangilov T",
            "Ona tili O'rinboyev F 404",
            "",
            "Ingliz tili Abdulatipova S Mamatqulova M 410315"
        ],
        "tuesday": [
            "Tarix Nematjonov I 407",
            "Avtomobil tuzilishi Yangilov T 102",
            "Informatika Ablogulov Shukurov 203/213",
            "Ona tili O'rinboyev F 401"
        ],
        "wednesday": [
            "INGLIZ TILI Abdulatipova S Mamataudova M 410/315 FIZIKA Shobotayeva D 201",
            "",
            "",
            ""
        ],
        "thursday": [
            "Fizika Shobutaeva D 204",
            "",
            "",
            ""
        ],
        "friday": [
            "Avtomobil shassisi texnik xizmat ko'rsatish O'A Qochqor G' 103",
            "",
            "",
            ""
        ]
    },
    "esu2-24": {
        "monday": [
            "Ma'naviyat soati Shukurova G",
            "Tarix Nemajonov I 407",
            "Informatika Abloqulov A Shukurov A 214213",
            "Tarix Nematjonov I 407"
        ],
        "tuesday": [
            "Jismoniy tarbiya Azimjonov S",
            "Ona tili O'rinboyev F 404",
            "Biznes asoslari Isroilov J Ashurov S 409",
            ""
        ],
        "wednesday": [
            "O'QUV AMALYOT I Promqulov M 214",
            "INFORMATIKA Abloquilov A/Shukurov A 213/203",
            "BIZNES ASOSLARI ASHUROV ISROILOV 409",
            ""
        ],
        "thursday": [
            "Ing tili Xayitova B/Tolibjonova M 403/413",
            "Fizika Shobutayeva D 201",
            "Elektr stansiya uskunalariini ta'mirlash Xudoyqulov X 204",
            ""
        ],
        "friday": [
            "Tarbiya Djumaboyeva D 204",
            "Elektr stansiya gozon jihozlarini tamirlash Xudoyqulov X 204",
            "Ch.Q.B.T Yoldoshov F 213",
            ""
        ]
    },
    "em2-24": {
        "monday": [
            "Ma'naviyat soati Abloqulov A",
            "Matematika Shukurova G 408",
            "Biznes asoslari Ashurov S Isroilov J 409",
            ""
        ],
        "tuesday": [
            "Biznes asoslari Isroilov J Ashurov S 409",
            "Matematika Shukurova G 408",
            "Ona tili O'rinboyev F 404",
            ""
        ],
        "wednesday": [
            "INGLIZ TILI Xayitova B /Tolibjonova M 403/413",
            "INGLIZ TILI Xayitova B /Tolibjonova M 403/413",
            "ONA TILI O'rinboyev F 404",
            ""
        ],
        "thursday": [
            "Elektr stansiya va elekr tarmoqlariga teknik xizmat ko'rsatish O'A Jamolov S",
            "",
            "",
            ""
        ],
        "friday": [
            "Elektr stansiya va elektr tarmoqlari Isroilov Z 206",
            "Bino inshotlarning elektr taminoti Isroilov Z 206",
            "Rus tili Xayitboyeva M 102",
            ""
        ]
    },
    "p2-24": {
        "monday": [
            "Ma'naviyat soati O'rinboyev F",
            "Plastik quvurlar pay vandlash texnologiyasi Egamberdiyev S 107",
            "Matematika Shukurova G 408",
            ""
        ],
        "tuesday": [
            "Plastik quvurlar payvandlash texnologiyasi O'A Egamberdiyev S 107",
            "Fizika Shobutayeva D 201",
            "Avtomobil uzatmalar qutisiga texnik xizmat ko'rsatish Yangilov T 102",
            ""
        ],
        "wednesday": [
            "BIZNES ASOSLARI ASHUROV ISROILOV 409",
            "",
            "JISMNONIY TARBIYA AZIMJONOV S",
            ""
        ],
        "thursday": [
            "Informatika Abloqulovi Shukurov 203/213",
            "Ona tili O'rinboyev F 404",
            "Payvand birikmalari defektopiyasi Egamberdiyev S 107",
            ""
        ],
        "friday": [
            "Tarix Nematjonov I 407",
            "Plastik quvurlar payvandlash texologiyasi Egamberdiyev S 107",
            "Jismoniy Tarbiya Azimjonov S",
            ""
        ]
    },
    "at2-24": {
        "monday": [
            "Ma'naviyat soati Shukurov Alish",
            "Biznes asoslarj Isroilov J Ashurov S 409",
            "CH.Q.B.T Yoldshov F 102",
            "Ingliz tili Xayitova B Tolibjonova"
        ],
        "tuesday": [
            "Informatika Ablogulov Shukurov 203/213",
            "Matematika Shukurova G 408",
            "Ona tili O'rinboyev F 401",
            ""
        ],
        "wednesday": [
            "AVTOMOIBILLARNI YOQILG'I BILAN TAMINLASH O'A Xolnazarov G' 103",
            "",
            "",
            ""
        ],
        "thursday": [
            "Informatika Abloqulovi Shukurov 203/213",
            "Ona tili O'rinboyev F 404",
            "Matematika Shukurova G 408",
            ""
        ],
        "friday": [
            "Ona tili O'rinboyev F 404",
            "Ona tili O'rinboyev F 404",
            "",
            ""
        ]
    }
}

# O'qituvchilar ma'lumotlari
TEACHERS_DATA = [
    {
        "name": "Rashidov Anvar",
        "position": "Direktor", 
        "specialty": "Energetika",
        "experience": "25 yil",
        "subjects": ["Energetika asoslari", "Elektr stansiyalari"]
    },
    {
        "name": "Ismailova Gulnora",
        "position": "O'qituvchi",
        "specialty": "Elektr texnikasi", 
        "experience": "15 yil",
        "subjects": ["Elektr texnikasi", "Elektr mashinalari"]
    },
    {
        "name": "Yusupov Bahodir",
        "position": "O'qituvchi", 
        "specialty": "Axborot texnologiyalari",
        "experience": "20 yil",
        "subjects": ["Web dasturlash", "Kompyuter tarmoqlari"]
    },
    {
        "name": "Tursunova Zulfiya",
        "position": "O'qituvchi",
        "specialty": "Payvandlash texnologiyasi", 
        "experience": "18 yil",
        "subjects": ["Payvandlash texnologiyasi", "Materialshunoslik"]
    }
]

@app.route('/')
def home():
    return jsonify({
        "message": "Shirin Energetika Texnikumi AI Bot API",
        "status": "running",
        "version": "1.0",
        "endpoints": {
            "/chat": "AI chat endpoint (POST)",
            "/schedule": "Dars jadvali (GET)", 
            "/schedule/<group>": "Maxsus guruh jadvali (GET)",
            "/teachers": "O'qituvchilar ro'yxati (GET)",
            "/health": "Server holati (GET)"
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
                    
                    DARS JADVALI: Barcha guruhlar uchun dars jadvali mavjud
                    O'QITUVCHILAR: Malakali ustozlar
                    ALOQA: Sirdaryo viloyati, Shirin shahri
                    
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

# Oxirgi qatorni o'zgartiring:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
