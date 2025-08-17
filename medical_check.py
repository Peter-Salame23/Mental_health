def validate_response(response: str) -> str:
    red_flags = [
        "stop taking meds", "you don’t need therapy",
        "ignore your symptoms", "just tough it out"
    ]
    for flag in red_flags:
        if flag in response.lower():
            return "⚠️ Potential unsafe advice detected. Please rephrase or consult a professional."
    return " Response validated."
