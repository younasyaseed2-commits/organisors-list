MALAYALAM_MAP = {
    "അ": "a",
    "ആ": "aa",
    "ഇ": "i",
    "ഈ": "ee",
    "ഉ": "u",
    "ഊ": "oo",
    "എ": "e",
    "ഏ": "e",
    "ഐ": "ai",
    "ഒ": "o",
    "ഓ": "o",
    "ഔ": "au",
    "ക": "ka",
    "ഖ": "kha",
    "ഗ": "ga",
    "ഘ": "gha",
    "ങ": "nga",
    "ച": "cha",
    "ഛ": "cha",
    "ജ": "ja",
    "ഝ": "jha",
    "ഞ": "nja",
    "ട": "ta",
    "ഠ": "tha",
    "ഡ": "da",
    "ഢ": "dha",
    "ണ": "na",
    "ത": "tha",
    "ഥ": "tha",
    "ദ": "da",
    "ധ": "dha",
    "ന": "na",
    "പ": "pa",
    "ഫ": "fa",
    "ബ": "ba",
    "ഭ": "bha",
    "മ": "ma",
    "യ": "ya",
    "ര": "ra",
    "റ": "ra",
    "ല": "la",
    "ള": "la",
    "ഴ": "zha",
    "വ": "va",
    "ശ": "sha",
    "ഷ": "sha",
    "സ": "sa",
    "ഹ": "ha",
    "ാ": "a",
    "ി": "i",
    "ീ": "ee",
    "ു": "u",
    "ൂ": "oo",
    "െ": "e",
    "േ": "e",
    "ൈ": "ai",
    "ൊ": "o",
    "ോ": "o",
    "ൌ": "au",
    "ൗ": "au",
    "ം": "m",
    "ൻ": "n",
    "ൺ": "n",
    "ർ": "r",
    "ൽ": "l",
    "ൾ": "l",
    "്": "",
}

COMMON_MALAYALAM_ALIASES = {
    "ഒളവട്ടൂർ": "olavattur",
    "കോഴിക്കോട്": "kozhikode",
    "മലപ്പുറം": "malappuram",
    "കണ്ണൂർ": "kannur",
    "വയനാട്": "wayanad",
    "തൃശൂർ": "thrissur",
    "കാസർഗോഡ്": "kasargod",
}


def transliterate_malayalam(value):
    value = str(value or "").strip()
    if not value:
        return ""

    if value in COMMON_MALAYALAM_ALIASES:
        return COMMON_MALAYALAM_ALIASES[value]

    return "".join(MALAYALAM_MAP.get(character, character) for character in value)


def search_terms(query):
    query = str(query or "").strip()
    terms = {query}
    transliterated = transliterate_malayalam(query)
    if transliterated and transliterated != query:
        terms.add(transliterated)
    return [term for term in terms if term]
