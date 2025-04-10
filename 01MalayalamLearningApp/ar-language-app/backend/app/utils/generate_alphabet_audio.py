from gtts import gTTS
import os
from pathlib import Path

def generate_alphabet_audio():
    # Create audio directory if it doesn't exist
    audio_dir = Path("static/audio/alphabets")
    audio_dir.mkdir(parents=True, exist_ok=True)

    # Malayalam alphabet pronunciations
    alphabets = [
        ("അ", "a"), ("ആ", "aa"), ("ഇ", "i"), ("ഈ", "ii"),
        ("ഉ", "u"), ("ഊ", "uu"), ("ഋ", "ru"), ("എ", "e"),
        ("ഏ", "ee"), ("ഐ", "ai"), ("ഒ", "o"), ("ഓ", "oo"),
        ("ഔ", "au"), ("ക", "ka"), ("ഖ", "kha"), ("ഗ", "ga"),
        ("ഘ", "gha"), ("ങ", "nga"), ("ച", "cha"), ("ഛ", "chha"),
        ("ജ", "ja"), ("ഝ", "jha"), ("ഞ", "nya"), ("ട", "ta"),
        ("ഠ", "tha"), ("ഡ", "da"), ("ഢ", "dha"), ("ണ", "na"),
        ("ത", "tha"), ("ഥ", "thha"), ("ദ", "dha"), ("ധ", "dhha"),
        ("ന", "na"), ("പ", "pa"), ("ഫ", "pha"), ("ബ", "ba"),
        ("ഭ", "bha"), ("മ", "ma"), ("യ", "ya"), ("ര", "ra"),
        ("ല", "la"), ("വ", "va"), ("ശ", "sha"), ("ഷ", "shha"),
        ("സ", "sa"), ("ഹ", "ha"), ("ള", "lla"), ("ഴ", "zha"),
        ("റ", "rra")
    ]

    for malayalam_char, transliteration in alphabets:
        filename = f"{transliteration}.mp3"
        filepath = audio_dir / filename
        
        if not filepath.exists():
            try:
                # Generate audio for the Malayalam character
                tts = gTTS(text=malayalam_char, lang='ml')
                tts.save(str(filepath))
                print(f"Generated audio for {malayalam_char} ({transliteration})")
            except Exception as e:
                print(f"Error generating audio for {malayalam_char}: {str(e)}")

if __name__ == "__main__":
    generate_alphabet_audio()