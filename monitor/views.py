from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram import Bot
from monitor.models import Receipt, User
import datetime
import json
import config
import asyncio
from monitor.utils import validate_token
from django.utils import timezone



def dashboard_callback(request, context):

    alive_users = User.objects.filter(is_bot_blocked=False).count()
    all_users = User.objects.count()
    users_registered = User.objects.exclude(full_name__isnull=True).exclude(full_name__exact='').count()
    users_in_paid_membership = (User.objects.exclude(subscription_till__isnull=True).
                                exclude(subscription_till__gte=datetime.datetime.today())).count()
    users_applied = User.objects.filter(applied_to_paid_membership=True).count()
    users_approved = User.objects.filter(is_accepted_to_paid_membership=True).count()

    data = {"bars": [
        {
            "title": "Alive users",
            "description": f"{alive_users} out of {all_users}",
            "value": alive_users // all_users * 100,
        },
        {
            "title": "Registered users",
            "description": f"{users_registered} out of {all_users}",
            "value": alive_users // users_registered * 100,
        }
        ,
        {
            "title": "Users applied for paid membership",
            "description": f"{users_applied} out of {all_users}",
            "value": users_applied // all_users * 100,
        }
        , {
            "title": "Users approved for paid membership",
            "description": f"{users_approved} out of {all_users}",
            "value": users_approved // all_users * 100,
        },
        {
            "title": "Members of paid membership",
            "description": f"{users_in_paid_membership} out of {all_users}",
            "value": users_in_paid_membership // all_users * 100,
        }
        ]}
    context.update(data)

    return context


@csrf_exempt
def accept_payment(request):
    request_json = json.loads(request.body)
    if not request_json['Success'] or request_json['Status'] != "AUTHORIZED":
        # asyncio.run(bot.send_message(text=str(list(Receipt.objects.get())) + 'SOSI HUETS', chat_id=1186221701))
        return HttpResponse(status=200)
    if not validate_token(request_json, config.PASSWORD):
        return HttpResponse(status=400)
    try:
        order = Receipt.objects.get(order_id=request_json['OrderId'])
    except Receipt.DoesNotExist:
        bot = Bot(token=config.BOT_TOKEN)
        asyncio.run(bot.send_message(text=str(request_json), chat_id=1186221701))
        asyncio.run(bot.session.close())
        return HttpResponse(status=200)
    order.is_paid = True
    order.save()
    order.telegram_id.subscription_till = timezone.now() + datetime.timedelta(days=365)
    order.telegram_id.save()
    bot = Bot(token=config.BOT_TOKEN)
    asyncio.run(
        bot.send_message(text="Вам дан доступ к платным форматам! [ссылка]", chat_id=order.telegram_id.telegram_id))
    asyncio.run(bot.session.close())
    return HttpResponse(status=200)
