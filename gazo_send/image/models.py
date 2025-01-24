from django.db import models
import os
from datetime import datetime

def upload_to(instance, filename):
    # 現在の日時を"YYYY-MM-DD-HH-MM-SS"形式でファイル名にする
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # 拡張子を保持してファイル名を変更
    ext = filename.split('.')[-1]
    return os.path.join('images/', f'{timestamp}.{ext}')

class UploadedImage(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.uploaded_at.strftime('%Y-%m-%d %H-%M-%S')}"