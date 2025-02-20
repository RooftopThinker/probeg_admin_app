from django.utils.functional import LazyObject
from django.contrib import admin
from .models import User, Referral, Receipt
from unfold.admin import ModelAdmin


@admin.register(Referral)
class UserAdmin(ModelAdmin):
    list_display = ('telegram_id', 'people_invited', 'people_bought_subscription')
    ordering = ('-people_invited', '-people_bought_subscription')
    search_fields = ('telegram_id',)


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('telegram_id', 'telegram_username', 'telegram_name', 'phone_number', 'admin_role',
                    'email', 'full_name', 'company_name', 'position', 'is_accepted', 'is_bot_blocked',
                    'applied_to_paid_membership', 'is_accepted_to_paid_membership',
                    'subscription_till')
    list_filter = ('is_accepted', 'role', 'is_accepted_to_paid_membership','is_bot_blocked',
                   'applied_to_paid_membership')
    search_fields = ('telegram_username', 'phone_number', 'email', 'telegram_id', 'full_name', 'company_name',
                     'position')
    # ordering = ('-telegram_id',)
    fieldsets = (
        ('Personal Info', {
            'fields': ('telegram_id', 'telegram_username', 'telegram_name', 'email', 'phone_number')
        }),
        ('Role and Status', {
            'fields': ('role', 'is_accepted', 'is_bot_blocked', 'applied_to_paid_membership',
                       'is_accepted_to_paid_membership')
        }),
        ('Other Details', {
            'fields': ('full_name', 'company_name', 'position', 'subscription_till')
        }),
    )
    readonly_fields = ('telegram_id',)


@admin.register(Receipt)
class ReceiptAdmin(ModelAdmin):
    list_display = ('order_id', 'telegram_id', 'date', 'is_paid')