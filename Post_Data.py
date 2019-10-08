import requests
import Constant
import G_API
import time
from datetime import datetime


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


def transport_set_assign_to(session_requests, data_dict):
    response = session_requests.post(
        Constant.url_set_assign_to,
        data_dict
    )
    return response


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


