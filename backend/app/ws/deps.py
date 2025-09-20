from app.ws.notifier import Notifier


notifier_instance = Notifier()

def get_notifier() -> Notifier:
    return notifier_instance