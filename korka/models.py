from django.db import models
from django.conf import settings


class Application(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('phone', 'Перевод по номеру телефона'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('done', 'Обучение завершено'),
    ]
    COURSE_CHOICES = [
        ('algorithms', 'Основы алгоритмизации и программирования'),
        ('web_design', 'Основы веб-дизайна'),
        ('databases', 'Основы проектирования баз данных'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    course_name = models.CharField('Наименование курса', max_length=200, choices=COURSE_CHOICES, blank=True)
    start_date = models.DateField('Желаемая дата начала')
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField('Статус заявки', max_length=20, choices=STATUS_CHOICES, default='new')
    feedback = models.TextField('Отзыв', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.course_name} — {self.user.username} — {self.get_status_display()}"
    
