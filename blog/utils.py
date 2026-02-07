def get_session_key(request):
    """Возвращает ключ сессии пользователя, создавая его при необходимости."""
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key
