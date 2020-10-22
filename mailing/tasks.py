from django_journal.celery import app


@app.task
def send_notification(user_email):
    """
    Тестовая функция заглушка.
    Предназначена для отправки email\sms\message по контактным данным пользователя.
    Рассылку сообщений инициирует учитель.
    """
    return user_email
