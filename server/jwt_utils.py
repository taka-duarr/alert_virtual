import jwt
import datetime

SECRET = "iot-secret"

def generate_token(device_id):
    payload = {
        "device": device_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None
