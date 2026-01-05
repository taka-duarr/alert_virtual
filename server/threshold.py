def check_threshold(data):
    t = data.get("temperature", 0)

    if t >= 60:
        return {"status": "BAHAYA", "message": f"🔥 KEBAKARAN ({t}°C)"}
    elif t >= 50:
        return {"status": "PERINGATAN", "message": f"⚠️ SUHU TINGGI ({t}°C)"}
    else:
        return {"status": "AMAN", "message": f"🟢 AMAN ({t}°C)"}
