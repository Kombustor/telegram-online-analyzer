import time
from pyrogram.api import types


def fetch_users(telegram_app_instance):
    # Getting contacts from the telegram api
    my_contacts = telegram_app_instance.get_contacts()
    users = []

    # Transforming all User instances into dictionaries
    for user in my_contacts.users:
        # If user is a bot, there's no data to track
        if user.bot:
            continue

        # Getting the last online attribute, if exists
        was_online = None
        if hasattr(user.status, 'was_online'):
            was_online = user.status.was_online

        # Getting the status
        status = get_status(user.status)
        # If the status is online, the "was_online" value is "NaN", so we're setting it to the current timestamp
        if status == 'online':
            was_online = int(time.time())

        # Adding the user to the list
        users.append({
            'time': int(time.time()),
            'userId': user.id,
            'name_first': user.first_name,
            'name_last': user.last_name,
            'name_user': user.username,
            'phone': user.phone,
            'status': status,
            'status_was_online': was_online
        })

    return users


def get_status(status):
    if isinstance(status, types.user_status_offline.UserStatusOffline):
        return 'offline'
    elif isinstance(status, types.user_status_empty.UserStatusEmpty):
        return 'empty'
    elif isinstance(status, types.user_status_online.UserStatusOnline):
        return 'online'
    elif isinstance(status, types.user_status_recently.UserStatusRecently):
        return 'recently'
    else:
        return 'unknown'
