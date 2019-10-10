import Constant
import requests
import G_API
from datetime import datetime
import time
import Config_Post_Data


def login_tms():

    login_info = {
        'UserId': Constant.login_userid,
        'Password': Constant.login_password,
        'RememberMe': 'true',
        'submitbutton': '++++Sign+In++++',
        'NoAutoLogin': 'true',
        'menus': 'top',
        'inline': 'true'
    }

    session_requests = requests.session()

    response = session_requests.post(
        Constant.url_tms_login,
        data=login_info,
    )

    csrf = Constant.re_pattern_csrf.search(response.text).group(1)

    print('Login as', Constant.login_userid, '...')
    print('Login to TMS successfully.')

    return session_requests, csrf


def log_event(worksheet, duration):

    now = datetime.fromtimestamp(time.time()).strftime(Constant.time_format_military)

    titles = worksheet.get_all_values()[0]
    titles_dict = dict()
    for i, title in enumerate(titles):
        titles_dict[title] = i + 1

    next_row = G_API.get_next_available_row(worksheet, 1)

    worksheet.update_cell(next_row, titles_dict['Process'], Constant.process_name)
    worksheet.update_cell(next_row, titles_dict['Log By'], Constant.login_userid)
    worksheet.update_cell(next_row, titles_dict['Log Time'], now)
    worksheet.update_cell(next_row, titles_dict['Duration'], duration)


def item_change_weight(session_requests, csrf, item_info_entry, item_freight_class, item_weight):

    data_dict_item = Config_Post_Data.config_item_edit(csrf, item_info_entry, item_freight_class, item_weight)

    # Request change.
    response = session_requests.post(
        url=Constant.url_post_edit_item,
        data=data_dict_item
    )

    html_script = response.text
    followup_urls = Constant.re_pattern_url_parse.findall(html_script)[0]
    api_key = Constant.re_pattern_api_key.findall(html_script)[0]
    for followup_url in followup_urls:
        session_requests.get(Constant.url_tms_root + followup_url)

    pendo_io = Constant.url_pendo_io_cdn
    pendo_io = pendo_io.replace('API_TO_REPLACE', api_key)
    session_requests.get(pendo_io)

    # Confirm.

    data_dict_item['norefresh'] = ''

    response = session_requests.post(
        url=Constant.url_post_edit_item,
        data=data_dict_item
    )

    html_script = response.text
    followup_urls = Constant.re_pattern_url_parse.findall(html_script)[0]
    api_key = Constant.re_pattern_api_key.findall(html_script)[0]
    for followup_url in followup_urls:
        session_requests.get(Constant.url_tms_root + followup_url)

    pendo_io = Constant.url_pendo_io_cdn
    pendo_io = pendo_io.replace('API_TO_REPLACE', api_key)
    session_requests.get(pendo_io)


def __add_ref_customer_gl_code_shipment(session_requests, csrf, oid, gl_code):

    data_dict = Config_Post_Data.config_add_ref_shipment(csrf, oid,
                                                         Constant.sid_ref_type_customer_gl_code, gl_code)
    response = session_requests.post(
        url=Constant.url_post_add_ref,
        data=data_dict
    )
    html_script = response.text
    followup_urls = Constant.re_pattern_url_parse.findall(html_script)[0]
    api_key = Constant.re_pattern_api_key.findall(html_script)[0]

    for followup_url in followup_urls:
        session_requests.get(Constant.url_tms_root + followup_url)
    pendo_io_cdn = Constant.url_pendo_io_cdn
    pendo_io_cdn = pendo_io_cdn.replace('API_TO_REPLACE', api_key)
    session_requests.get(pendo_io_cdn)

    pendo_io_data = Constant.url_pendo_io_data
    pendo_io_data = pendo_io_data.replace('API_TO_REPLACE', api_key)
    session_requests.get(pendo_io_data)


def add_ref_customer_gl_code_shipment_list(session_requests, csrf, dict_list):
    count = 0
    for value in dict_list:
        gl_code = value['Customer GL Code']
        if gl_code != '-1':
            oid = value['OID']
            __add_ref_customer_gl_code_shipment(session_requests, csrf, oid, gl_code)
            count += 1
    print('Customer GL code has been added to', count, 'number of shipiments.')
