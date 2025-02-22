import hashlib

import config


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_token(params: dict, password: str) -> bool:
    try:
        token = params['Token']
    except KeyError:
        return False
    del params['Token']
    params_with_password = params.copy()
    params_with_password['Password'] = password
    for i in params_with_password.items():
        if i[1] == True:
            params_with_password[i[0]] = 'true'
        if i[1] == False:
            params_with_password[i[0]] = 'false'
    sorted_params = dict(sorted(params_with_password.items()))

    concatenated_string = ''.join(str(value) for value in sorted_params.values())

    sha256_hash = hashlib.sha256(concatenated_string.encode('utf-8')).hexdigest()
    if sha256_hash == token:
        return True
    return False


vkid = {
  "TerminalKey": "1733912605907DEMO",
  "OrderId": "17400300641186221701",
  "Success": "true",
  "Status": "AUTHORIZED",
  "PaymentId": 5896706994,
  "ErrorCode": "0",
  "Amount": 40000000,
  "CardId": 534687770,
  "Pan": "400000******0119",
  "ExpDate": "1230",
  "Token": "15a3dab077955982ef752af067bf80e0154a057f31963aff89a1fa611e90daae"
}
validate_token(vkid, config.PASSWORD)
