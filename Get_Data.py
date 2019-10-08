import Constant
import re


def get_shipment_report_by_oid(session_requests, csrf, oid):
    # SEND FIRST POST REQUEST

    post_data = Constant.open_shipment_report_by_oid_dict0.copy()
    post_data['_csrf'] = csrf
    post_data['reportoid'] = oid

    response = session_requests.post(
        Constant.url_list_shipments,
        data=post_data
    )

    # SEND FOLLOWING GET REQUESTS

    get_urls = Constant.re_pattern_url_shipment_report.findall(response.text)
    for url in get_urls:
        session_requests.get(Constant.url_tms_root + url)

    # SEND SECOND POST REQUEST
    post_data = Constant.open_shipment_report_by_oid_dict1.copy()
    post_data['_csrf'] = csrf
    post_data['reportoid'] = oid

    response = session_requests.post(
        Constant.url_list_shipments,
        data=post_data
    )

    print('Open report using oid successfully.')

    return response


def get_transport_report_by_report_format(session_requests, data_dict):
    response = session_requests.post(
        Constant.url_post_transport_report_format,
        data_dict
    )

    html_script = response.text
    urls = Constant.re_pattern_url_transport_report_format.findall(html_script)
    for url in urls:
        session_requests.get(Constant.url_tms_root + url)

    response = session_requests.get(Constant.url_get_transport_report_format0)
    html_script = response.text
    urls = Constant.re_pattern_url_transport_report_format.findall(html_script)
    for url in urls:
        session_requests.get(Constant.url_tms_root + url)

    response = session_requests.get(Constant.url_get_transport_report_format1)

    return response


def parse_data(html_script, re_pattern_dict):

    data_dict = dict()
    for key, item in re_pattern_dict.items():
        if item.search(html_script):
            data_list = item.findall(html_script)
            #REPLACE HTML EQUIVALENCE TO NORMAL SCRIPT
            data_list = [d.replace(Constant.html_equivalence_and, '&') for d in data_list]
            data_dict[key] = data_list
        else:
            break
    return data_dict


def read_login_credentials():
    login_userid = open('username.txt', mode='r')
    login_password = open('password.txt', mode='r')

    Constant.login_userid = login_userid.read()
    Constant.login_password = login_password.read()

    print('User credentials read successfully.')

