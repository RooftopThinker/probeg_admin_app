from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram import Bot
from monitor.models import Receipt, User
import datetime
import json
import config
import asyncio
from monitor.utils import get_client_ip, validate_token


def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context


@csrf_exempt
def test(request):
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
    order.telegram_id.subscription_till = datetime.datetime.now() + datetime.timedelta(days=365)
    order.telegram_id.save()
    bot = Bot(token=config.BOT_TOKEN)
    asyncio.run(bot.send_message(text="Вам дан доступ к платным форматам! [ссылка]", chat_id=order.telegram_id.telegram_id))
    asyncio.run(bot.session.close())
    return HttpResponse(status=200)
