from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Alphabet

def seed_alphabets():
    db = SessionLocal()
    try:
        # Check if alphabets already exist
        if db.query(Alphabet).first():
            print("Alphabets already seeded")
            return

        alphabets = [
            {"malayalam_char": "അ", "english_transliteration": "a", "audio_url": "/static/audio/alphabets/a.mp3"},
            {"malayalam_char": "ആ", "english_transliteration": "aa", "audio_url": "/static/audio/alphabets/aa.mp3"},
            {"malayalam_char": "ഇ", "english_transliteration": "i", "audio_url": "/static/audio/alphabets/i.mp3"},
            {"malayalam_char": "ഈ", "english_transliteration": "ii", "audio_url": "/static/audio/alphabets/ii.mp3"},
            {"malayalam_char": "ഉ", "english_transliteration": "u", "audio_url": "/static/audio/alphabets/u.mp3"},
            {"malayalam_char": "ഊ", "english_transliteration": "uu", "audio_url": "/static/audio/alphabets/uu.mp3"},
            {"malayalam_char": "ഋ", "english_transliteration": "ru", "audio_url": "/static/audio/alphabets/ru.mp3"},
            {"malayalam_char": "എ", "english_transliteration": "e", "audio_url": "/static/audio/alphabets/e.mp3"},
            {"malayalam_char": "ഏ", "english_transliteration": "ee", "audio_url": "/static/audio/alphabets/ee.mp3"},
            {"malayalam_char": "ഐ", "english_transliteration": "ai", "audio_url": "/static/audio/alphabets/ai.mp3"},
            {"malayalam_char": "ഒ", "english_transliteration": "o", "audio_url": "/static/audio/alphabets/o.mp3"},
            {"malayalam_char": "ഓ", "english_transliteration": "oo", "audio_url": "/static/audio/alphabets/oo.mp3"},
            {"malayalam_char": "ഔ", "english_transliteration": "au", "audio_url": "/static/audio/alphabets/au.mp3"},
            {"malayalam_char": "ക", "english_transliteration": "ka", "audio_url": "/static/audio/alphabets/ka.mp3"},
            {"malayalam_char": "ഖ", "english_transliteration": "kha", "audio_url": "/static/audio/alphabets/kha.mp3"},
            {"malayalam_char": "ഗ", "english_transliteration": "ga", "audio_url": "/static/audio/alphabets/ga.mp3"},
            {"malayalam_char": "ഘ", "english_transliteration": "gha", "audio_url": "/static/audio/alphabets/gha.mp3"},
            {"malayalam_char": "ങ", "english_transliteration": "nga", "audio_url": "/static/audio/alphabets/nga.mp3"},
            {"malayalam_char": "ച", "english_transliteration": "cha", "audio_url": "/static/audio/alphabets/cha.mp3"},
            {"malayalam_char": "ഛ", "english_transliteration": "chha", "audio_url": "/staticaudio/alphabets/chha.mp3"},
            {"malayalam_char": "ജ", "english_transliteration": "ja", "audio_url": "/static/audio/alphabets/ja.mp3"},
            {"malayalam_char": "ഝ", "english_transliteration": "jha", "audio_url": "/static/audio/alphabets/jha.mp3"},
            {"malayalam_char": "ഞ", "english_transliteration": "nya", "audio_url": "/static/audio/alphabets/nya.mp3"},
            {"malayalam_char": "ട", "english_transliteration": "ta", "audio_url": "/static/audio/alphabets/ta.mp3"},
            {"malayalam_char": "ഠ", "english_transliteration": "tha", "audio_url": "/static/audio/alphabets/tha.mp3"},
            {"malayalam_char": "ഡ", "english_transliteration": "da", "audio_url": "/static/audio/alphabets/da.mp3"},
            {"malayalam_char": "ഢ", "english_transliteration": "dha", "audio_url": "/static/audio/alphabets/dha.mp3"},
            {"malayalam_char": "ണ", "english_transliteration": "na", "audio_url": "/static/audio/alphabets/na.mp3"},
            {"malayalam_char": "ത", "english_transliteration": "tha", "audio_url": "/static/audio/alphabets/tha.mp3"},
            {"malayalam_char": "ഥ", "english_transliteration": "thha", "audio_url": "/static/audio/alphabets/thha.mp3"},
            {"malayalam_char": "ദ", "english_transliteration": "dha", "audio_url": "/static/audio/alphabets/dha.mp3"},
            {"malayalam_char": "ധ", "english_transliteration": "dhha", "audio_url": "/static/audio/alphabets/dhha.mp3"},
            {"malayalam_char": "ന", "english_transliteration": "na", "audio_url": "/static/audio/alphabets/na.mp3"},
            {"malayalam_char": "പ", "english_transliteration": "pa", "audio_url": "/static/audio/alphabets/pa.mp3"},
            {"malayalam_char": "ഫ", "english_transliteration": "pha", "audio_url": "/static/audio/alphabets/pha.mp3"},
            {"malayalam_char": "ബ", "english_transliteration": "ba", "audio_url": "/static/audio/alphabets/ba.mp3"},
            {"malayalam_char": "ഭ", "english_transliteration": "bha", "audio_url": "/static/audio/alphabets/bha.mp3"},
            {"malayalam_char": "മ", "english_transliteration": "ma", "audio_url": "/static/audio/alphabets/ma.mp3"},
            {"malayalam_char": "യ", "english_transliteration": "ya", "audio_url": "/static/audio/alphabets/ya.mp3"},
            {"malayalam_char": "ര", "english_transliteration": "ra", "audio_url": "/static/audio/alphabets/ra.mp3"},
            {"malayalam_char": "ല", "english_transliteration": "la", "audio_url": "/static/audio/alphabets/la.mp3"},
            {"malayalam_char": "വ", "english_transliteration": "va", "audio_url": "/static/audio/alphabets/va.mp3"},
            {"malayalam_char": "ശ", "english_transliteration": "sha", "audio_url": "/static/audio/alphabets/sha.mp3"},
            {"malayalam_char": "ഷ", "english_transliteration": "shha", "audio_url": "/static/audio/alphabets/shha.mp3"},
            {"malayalam_char": "സ", "english_transliteration": "sa", "audio_url": "/static/audio/alphabets/sa.mp3"},
            {"malayalam_char": "ഹ", "english_transliteration": "ha", "audio_url": "/static/audio/alphabets/ha.mp3"},
            {"malayalam_char": "ള", "english_transliteration": "lla", "audio_url": "/static/audio/alphabets/lla.mp3"},
            {"malayalam_char": "ഴ", "english_transliteration": "zha", "audio_url": "/static/audio/alphabets/zha.mp3"},
            {"malayalam_char": "റ", "english_transliteration": "rra", "audio_url": "/static/audio/alphabets/rra.mp3"},
        ]
        
        for alpha in alphabets:
            db.add(Alphabet(**alpha))
        db.commit()
        print("Successfully seeded alphabets")
    finally:
        db.close()

if __name__ == "__main__":
    seed_alphabets()