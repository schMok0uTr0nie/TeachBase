from django.db import models


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    owner_id = models.IntegerField(verbose_name='Владелец')
    owner_name = models.CharField(max_length=100, verbose_name='Имя владельца')

    description = models.TextField(max_length=1000, verbose_name='Описание')
    total_score = models.IntegerField(verbose_name='Макс.результат')
    total_tasks = models.IntegerField(verbose_name='Всего заданий')
    unchangeable = models.BooleanField(default=False)
    include_weekly_report = models.BooleanField(default=False)

    content_type = models.IntegerField(default=1, help_text='1 - Course; 2 - Quiz; 3 - Literature')
    is_netology = models.BooleanField(default=False)
    demo = models.BooleanField(default=False)
    custom_author_names = models.CharField(max_length=255, verbose_name='Псевдонимы')
    custom_contents_link = models.CharField(max_length=500, null=True, verbose_name='Ссылка')
    duration = models.IntegerField(null=True, help_text='Duration in sec.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-id']
