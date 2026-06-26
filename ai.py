from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")

SYSTEM_PROMPT = """
Siz "Hosil Tavsiya Tizimi" uchun sun'iy intellekt yordamchi botsiz.
Siz faqat qishloq xo'jaligi va ekin tanlash bo'yicha maslahat berasiz:
- Ekin tavsiya qilish
- Tuproq tarkibi (Azot N, Fosfor P, Kaliy K)
- pH darajasi
- Harorat, namlik, yog'ingarchilik
- Hosildorlikni oshirish
Qoidalar:
- Javoblaringiz qisqa, aniq va tushunarli bo'lsin
- Faqat shu mavzudan chiqmaslik
- Har doim sababini qisqacha tushuntirish
- Amaliy maslahat berish (o'g'it, sug'orish)
"""

# BU YERDA: image_file=None qo'shildi. Bu app.py dagi xatoni yo'qotadi.
def get_ai_response(user_input: str, image_file=None) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content

# Test
if __name__ == "__main__":
    test_response = get_ai_response("Salom, maslahat ber!")
    print(test_response)

