import Constant
import Config_Post_Data


def read_login_credentials():
    login_userid = open('username.txt', mode='r')
    login_password = open('password.txt', mode='r')
    Constant.login_userid = login_userid.read()
    Constant.login_password = login_password.read()
    print('User credentials read successfully.')


def get_info_xml(file_root_path, file_name):
    # -----------------------------------------------------------------------------------------------------------------
    # Concatenate for the directory path.
    file_path = file_root_path + file_name
    # -----------------------------------------------------------------------------------------------------------------
    # Open the file and read.
    content = open(file_path, 'r')
    lines = content.read()
    # -----------------------------------------------------------------------------------------------------------------
    # Find the primary reference and the weight information.
    pri_ref = Constant.re_pattern_xml_pri_ref.findall(lines)[0]
    weight = Constant.re_pattern_xml_weight.findall(lines)[0]
    # -----------------------------------------------------------------------------------------------------------------
    # Close the file.
    content.close()
    return pri_ref, weight


def get_shipment_report_by_report_format(session_requests, csrf, pri_ref_str):
    # -----------------------------------------------------------------------------------------------------------------
    # Configure POST data and send it to a given URL.
    data_dict = Config_Post_Data.config_shipment_report(csrf, pri_ref_str)
    response = session_requests.post(
        Constant.url_post_shipment_report_format,
        data_dict
    )
    # -----------------------------------------------------------------------------------------------------------------
    # Following is required requests for collecting response from TMS.
    html_script = response.text
    urls = Constant.re_pattern_url_report_format.findall(html_script)
    for url in urls:
        session_requests.get(Constant.url_tms_root + url)

    response = session_requests.get(Constant.url_get_shipment_report_format0)
    html_script = response.text
    urls = Constant.re_pattern_url_report_format.findall(html_script)
    for url in urls:
        session_requests.get(Constant.url_tms_root + url)

    response = session_requests.get(Constant.url_get_shipment_report_format1)

    return response
