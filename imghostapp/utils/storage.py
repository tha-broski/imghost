import os
from django.conf import settings

def get_user_storage_size(user):
    folder_path = os.path.join(settings.MEDIA_ROOT, f'user_{user.username}')
    total_size=0

    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            file_path = os.path.join(dirpath, f)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)

    return total_size

def get_user_storage_limit(user):
    if user.is_premiumuser:
        return 15 * 1024 ** 3
    return 5 * 1024 **3