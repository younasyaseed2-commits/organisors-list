PLACE_DISTRICT_MAP = {
    "bekal": "Kasargod",
    "calicut": "Kozhikode",
    "chalakudy": "Thrissur",
    "cheruvathur": "Kasargod",
    "edappal": "Malappuram",
    "feroke": "Kozhikode",
    "guruvayur": "Thrissur",
    "iritty": "Kannur",
    "irinjalakuda": "Thrissur",
    "kalpetta": "Wayanad",
    "kanhangad": "Kasargod",
    "kannur": "Kannur",
    "kasaragod": "Kasargod",
    "kasargod": "Kasargod",
    "kodungallur": "Thrissur",
    "kondotty": "Malappuram",
    "kottakkal": "Malappuram",
    "kozhikode": "Kozhikode",
    "kunnamkulam": "Thrissur",
    "mananthavady": "Wayanad",
    "manjeri": "Malappuram",
    "manjeshwar": "Kasargod",
    "mattannur": "Kannur",
    "mavoor": "Kozhikode",
    "medical college": "Kozhikode",
    "meppadi": "Wayanad",
    "nadakkavu": "Kozhikode",
    "nilambur": "Malappuram",
    "nileshwar": "Kasargod",
    "panamaram": "Wayanad",
    "panoor": "Kannur",
    "payyanur": "Kannur",
    "perinthalmanna": "Malappuram",
    "ponnani": "Malappuram",
    "pulpally": "Wayanad",
    "sulthan bathery": "Wayanad",
    "taliparamba": "Kannur",
    "thalassery": "Kannur",
    "thrissur": "Thrissur",
    "tirur": "Malappuram",
    "uppala": "Kasargod",
    "vythiri": "Wayanad",
    "wadakkanchery": "Thrissur",
}


def resolve_district_name(location_name, explicit_district_name=""):
    explicit_district_name = str(explicit_district_name or "").strip()
    if explicit_district_name:
        return explicit_district_name

    normalized_location = str(location_name or "").strip().lower()
    for place_name, district_name in PLACE_DISTRICT_MAP.items():
        if place_name in normalized_location:
            return district_name

    return "Unknown"
