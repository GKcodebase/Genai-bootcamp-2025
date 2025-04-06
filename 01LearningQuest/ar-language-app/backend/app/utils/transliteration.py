from functools import lru_cache

@lru_cache(maxsize=1)
def get_transliteration_map():
    """Malayalam to English transliteration mapping"""
    return {
        'അ': 'a', 'ആ': 'aa', 'ഇ': 'i', 'ഈ': 'ee',
        'ഉ': 'u', 'ഊ': 'oo', 'എ': 'e', 'ഏ': 'ae',
        'ഐ': 'ai', 'ഒ': 'o', 'ഓ': 'oo', 'ഔ': 'au',
        'ക': 'ka', 'ഖ': 'kha', 'ഗ': 'ga', 'ഘ': 'gha',
        'ങ': 'nga', 'ച': 'cha', 'ഛ': 'chha', 'ജ': 'ja',
        'ഝ': 'jha', 'ഞ': 'nya', 'ട': 'ta', 'ഠ': 'tta',
        'ഡ': 'da', 'ഢ': 'dha', 'ണ': 'na', 'ത': 'tha',
        'ഥ': 'thha', 'ദ': 'da', 'ധ': 'dha', 'ന': 'na',
        'പ': 'pa', 'ഫ': 'pha', 'ബ': 'ba', 'ഭ': 'bha',
        'മ': 'ma', 'യ': 'ya', 'ര': 'ra', 'ല': 'la',
        'വ': 'va', 'ശ': 'sha', 'ഷ': 'sha', 'സ': 'sa',
        'ഹ': 'ha', 'ള': 'la', 'ഴ': 'zha', 'റ': 'ra',
        'ം': 'm', '്': '', 'ാ': 'aa', 'ി': 'i',
        'ീ': 'ee', 'ു': 'u', 'ൂ': 'oo', 'െ': 'e',
        'േ': 'ae', 'ൈ': 'ai', 'ൊ': 'o', 'ോ': 'oo',
        'ൗ': 'au'
    }

def transliterate_malayalam(text: str) -> str:
    """Convert Malayalam text to English transliteration"""
    translit_map = get_transliteration_map()
    result = []
    i = 0
    while i < len(text):
        # Try to match two characters first (for combined characters)
        if i + 1 < len(text) and text[i:i+2] in translit_map:
            result.append(translit_map[text[i:i+2]])
            i += 2
        # Then try single character
        elif text[i] in translit_map:
            result.append(translit_map[text[i]])
            i += 1
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)