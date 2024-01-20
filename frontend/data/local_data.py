def authentificated_session(user_data):
    new_user_session = {
        'name': user_data.get('payload', {}).get('name', ''),
        'access_token': user_data.get('session', {}).get('access_token', ''),
        'expiration': user_data.get('session', {}).get('expiration', ''),
        'is_authenticated': True,
        'is_superuser': user_data.get('payload', {}).get('is_superuser', False)
    }
    return new_user_session
