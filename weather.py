import requests

def get_auto_weather():
    try:
        # 1. IP orqali geolokatsiyani aniqlash (bepul xizmat)
        geo_res = requests.get('https://ipapi.co/json/').json()
        city = geo_res.get('city', 'Tashkent')
        lat = geo_res.get('latitude')
        lon = geo_res.get('longitude')

        # 2. OpenWeatherMap API ga so'rov yuborish
        api_key = "2d1bcb1575a3350e4e514c76fa44edcb"
        # Koordinatalar (lat/lon) orqali aniqroq ma'lumot olamiz
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        
        weather_res = requests.get(url).json()
        
        return {
            "city": city,
            "temp": weather_res['main']['temp'],
            "humidity": weather_res['main']['humidity'],
            "rain": weather_res.get('rain', {}).get('1h', 0)
        }
    except Exception as e:
        print(f"Ob-havoni olishda xato: {e}")
        return None
    