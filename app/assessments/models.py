from django.db import models


class Log(models.Model):
    error_message = models.TextField('錯誤訊息')
    create_at = models.DateTimeField('錯誤時間', auto_now_add=True)
    checked = models.BooleanField('已檢查', default=False)

    def __str__(self):
        return 'Error at {}'.format(self.create_at)
