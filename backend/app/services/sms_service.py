class SmsAlertService:
    def send(self, phone: str, message: str) -> dict:
        print(f"[SMS SIMULATION] to={phone} message={message}")
        return {"status": "sent", "phone": phone}
