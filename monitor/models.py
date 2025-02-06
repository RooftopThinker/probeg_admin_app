from django.db import models
from django.contrib import admin
from unfold.admin import ModelAdmin


class User(models.Model):
    ROLE_CHOICES = (
        (0, 'Simple User'),
        (1, 'Ambassador'),
        (2, 'Agent'),
    )
    telegram_id = models.BigIntegerField(unique=True, null=False)
    telegram_username = models.CharField(max_length=255, blank=True, null=True)
    telegram_name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=20, null=False, verbose_name='Phone Number')
    email = models.EmailField(blank=True, null=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Full Name')
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Company Name')
    position = models.CharField(max_length=255, blank=True, null=True, verbose_name='Position')
    is_accepted = models.BooleanField(default=False, verbose_name='Is Accepted to Free Channels')
    is_accepted_to_paid_partnership = models.BooleanField(default=False, verbose_name='Is Accepted to Paid Channels')
    subscription_till = models.DateField(blank=True, null=True, verbose_name="Subscription lasts till")
    # phone_number = models.CharField(max_length=20, null=False, verbose_name='Номер телефона')
    # email = models.EmailField(blank=True, null=True)
    # role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    # full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО')
    # company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Компания')
    # position = models.CharField(max_length=255, blank=True, null=True, verbose_name='Должность')
    # is_accepted = models.BooleanField(default=False, verbose_name='Допущен к бесплатным форматам')
    # is_accepted_to_paid_partnership = models.BooleanField(default=False, verbose_name='Допущен к платным форматам')
    # subscription_till = models.DateField(blank=True, null=True, verbose_name="Подписка истекает")

    def __str__(self):
        return f"User: {self.telegram_username or self.telegram_name or self.telegram_id}"

    class Meta:
        db_table = 'users'

    def get_role_display(self):

        try:
            return dict(self.ROLE_CHOICES)[self.role]
        except KeyError:
            return f"Роль {self.role}"

    @admin.display(description='Роль')
    def admin_role(self):
        """
        Поле специально для админки Django, которое возвращает название роли.
        """
        return self.get_role_display()





