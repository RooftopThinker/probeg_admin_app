from django.db import models
from django.contrib import admin
from unfold.admin import ModelAdmin


class User(models.Model):
    ROLE_CHOICES = (
        (0, 'Simple User'),
        (1, 'Ambassador'),
        (2, 'Agent'),
    )
    id = models.BigAutoField(primary_key=True)
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
    #invited_by = models.ForeignKey('Referral', on_delete=models.CASCADE, to_field='telegram_id')
    invited_by = models.BigIntegerField()
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
        return f"User: {self.telegram_username or self.telegram_id}"

    class Meta:
        db_table = 'users'

    def get_role_display(self):

        try:
            return dict(self.ROLE_CHOICES)[self.role]
        except KeyError:
            return f"Role {self.role}"

    @admin.display(description='Role')
    def admin_role(self):

        return self.get_role_display()


class Referral(models.Model):
    id = models.BigAutoField(primary_key=True)
    telegram_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, null=False, db_column='telegram_id',
                                    to_field='telegram_id', verbose_name='User')
    people_invited = models.IntegerField(default=0, verbose_name='People Invited')
    people_bought_subscription = models.IntegerField(default=0, verbose_name='People Invited & Bought Subscription')

    class Meta:
        db_table = 'referrals'

    def __str__(self):
        return f"Referral ID: {self.telegram_id}"




