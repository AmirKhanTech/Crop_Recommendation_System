import edge_tts
import subprocess
import base64
import os


def get_audio_html(text: str, voice: str = "uz-UZ-MadinaNeural") -> str:
    audio_path = "ai_response.mp3"
    subprocess.run([
        "edge-tts",
        f"--voice={voice}",
        f"--text={text}",
        f"--write-media={audio_path}"
    ])
    with open(audio_path, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode()
    os.remove(audio_path)
    return f"""
    <audio controls autoplay style="width:100%; margin-top:10px; border-radius:12px;">
        <source src="data:audio/mp3;base64,{audio_data}" type="audio/mp3">
    </audio>
    """


# Test
if __name__ == "__main__":
    html = get_audio_html("Salom, bu ovozli test!")
    print("Muvaffaqiyatli ishladi!" if html else "Xato!")