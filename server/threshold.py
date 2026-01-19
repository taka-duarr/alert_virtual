def check_threshold(data):
    t = float(data.get("temperature", 0))

    if t >= 60:
        return {
            "status": "BAHAYA",
            "temperature": t,
            "message": "🔥 KEBAKARAN"
        }
    elif t >= 50:
        return {
            "status": "PERINGATAN",
            "temperature": t,
            "message": "⚠️ SUHU TINGGI"
        }
    else:
        return {
            "status": "AMAN",
            "temperature": t,
            "message": "🟢 AMAN"
        }
