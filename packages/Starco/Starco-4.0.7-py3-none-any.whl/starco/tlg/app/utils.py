import re,json
from starco.utils import path_maker

def get_number(txt):
    txt = str(txt)
    numbers =re.findall(r'\d+', txt)
    if numbers:
        sn = ''.join(numbers)
        sn = sn.lstrip('0')
        return int(sn)

def session_number(number:int,base_number):
    out = f"{number}.session"
    if base_number[0]=='+':out=f'+{out}'
    return out

import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
import pycountry

def get_country_name(phone_number):
    try:
        phone_number = str(phone_number)
        if phone_number[0]!='+':phone_number=f"+{phone_number}"
        pn = phonenumbers.parse(phone_number)
        country = pycountry.countries.get(alpha_2=region_code_for_number(pn)).name
        country = country.replace(' ','_').replace(',','')
        return country
    except:return 'other'

def account_path_list(number, dtype='json', add_country=False):
    number = str(number)
    number = number.replace('+', '')
    out = ['accounts', dtype]
    if add_country:
        out += [get_country_name(number)]
    out += [number]
    return out

def path_for_tlg(number, dtype='json', add_country=False):
    pl = account_path_list(number, dtype=dtype, add_country=add_country)
    number = pl[-1]
    return path_maker(pl)+f'/{number}.{dtype}'

def cfg_from_json(json_path):
    with open(json_path, 'r') as f:
        cfg = json.loads(f.read())
    return ready_cfg(**cfg)

def ready_cfg(number: str, **data):
    number = number.replace('+', '')
    cfg = {
        'api_id': None,
        'api_hash': None,
        'device_model': None,
        'system_version': None,
        'app_version': None,
        'number': number,
        'session': path_for_tlg(number,data.get('dtype','session')),
        'lang_code': 'en',
        'system_lang_code': 'en',
        'proxy': None
    }
    # json = pMaker(number)+'.json'
    api_id, api_hash = [17203958, '82cefc4001e057c9d1488ab90e23d54f']

    cfg['api_id'] = data.get('api_id', api_id)
    cfg['api_hash'] = data.get('api_hash', api_hash)
    cfg['device_model'] = data.get('device_model', 'Telegram Desktop 4.12.2')
    cfg['system_version'] = data.get('system_version', '5.15.1')
    cfg['app_version'] = data.get('app_version', '1.6.7')
    cfg['lang_code'] = data.get('lang_code', 'en')
    cfg['system_lang_code'] = data.get('system_lang_code', 'en')
    cfg['proxy'] = data.get('proxy')
    return cfg

def save_json(tlg, json_path: str, p2fa=None):
    init_request = tlg._init_request
    device_model = init_request.device_model
    system_version = init_request.system_version
    app_version = init_request.app_version
    system_lang_code = init_request.system_lang_code
    lang_code = init_request.lang_code
    cfg = {
        'api_id': tlg.api_id,
        'number': tlg.number,
        'api_hash': tlg.api_hash,
        'device_model': device_model,
        'system_version': system_version,
        'app_version': app_version,
        'system_lang_code': system_lang_code,
        'lang_code': lang_code,
        'password_2fa': p2fa,
    }

    with open(json_path, 'w') as f:
        f.write(json.dumps(cfg))
