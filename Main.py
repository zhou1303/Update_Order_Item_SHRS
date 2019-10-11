import Post_Data
import Constant
import os
import G_API
import time
import Get_Data
import Parse_Data


if __name__ == '__main__':

    # START COUNTING RUNNING TIME
    start = time.time()

    # Create a dictionary object to save primary reference, file name, and weight information.
    weight_dict = dict()
    file_list = os.listdir(Constant.shearers_xml_path)
    for file in file_list:
        pri_ref, weight = Get_Data.get_info_xml(Constant.shearers_xml_path, file)
        weight_dict[pri_ref] = [weight, Constant.shearers_xml_path + file]

    # Convert primary reference list to a string separated by comma.
    pri_ref_str = ','.join([key for key, item in weight_dict.items()])

    # LOGIN TMS
    Get_Data.read_login_credentials()
    session_requests, csrf = Post_Data.login_tms()

    shipment_report_html_script = Get_Data.get_shipment_report_by_report_format(session_requests, csrf, pri_ref_str).text

    all_cols = Constant.re_pattern_all_cols.findall(shipment_report_html_script)

#--------------------------------------------------------------------------------------------------------------
# Add customer GL code.

    # Make the returned list a list of dictionaries.
    dict_list = list()
    for tp in all_cols:
        tp_dict = {
            'OID': tp[0],
            'Primary Reference': tp[1],
            'ConGroup': tp[2],
            'Customer GL Code': tp[3],
            'Dest Name': tp[4],
            'Dest City': tp[5]
        }
        dict_list.append(tp_dict)

    print('Pairing customer GL code using destination name...')
    dict_list = Parse_Data.get_gl_code(dict_list)
    print('Adding customer GL code reference to orders in the system...')
    Post_Data.add_ref_customer_gl_code_shipment_list(session_requests, csrf, dict_list)

# --------------------------------------------------------------------------------------------------------------
# Correct item weight and cube.

    print('Updating item weight and cube in shipments...')

    cube_dict = Parse_Data.get_pdf_cube()

    for i, value in enumerate(dict_list):
        # Concatenate item list url for this shipment.
        url_item_list = Constant.url_item_list
        url_item_list = url_item_list.replace('OID_TO_REPLACE', value['OID'])

        # Get item list html.
        response = session_requests.get(url_item_list)
        html_script = response.text

        # Get item html.
        item_oid = Constant.re_pattern_item_oid.findall(html_script)[0]
        url_item = Constant.url_item
        url_item = url_item.replace('OID_TO_REPLACE', item_oid)
        response = session_requests.get(url_item)
        html_script = response.text

        item_info_entry = Constant.re_pattern_item_edit_entry.findall(html_script)
        item_info_dropdown = Constant.re_pattern_item_edit_dropdown.findall(html_script)

        item_freight_class = item_info_dropdown[0]

        item_weight = weight_dict[value['Primary Reference']][0]
        item_cube = cube_dict[value['Primary Reference']]

        # Change weight on item.
        Post_Data.item_editing(session_requests, csrf, item_info_entry, item_freight_class, item_weight)

        # Remove files from folder.
        os.remove(weight_dict[value['Primary Reference']][1])

    len_oid = len(all_cols)
    print('Process completes.', len_oid, 'number of shipments are updated. This window will be closed in 30 seconds.')

    # END TIME
    end = time.time()

    # UPDATE LOG REPORT ON GOOGLE SHEETS
    duration = end - start
    workbook_log = G_API.get_workbook_by_id(Constant.g_sheets_workbook_id_log)
    worksheet_log = G_API.get_worksheet_by_id(workbook_log, Constant.g_sheets_worksheet_id_log)
    Post_Data.log_event(worksheet_log, duration)

    time.sleep(30)


# html_script = response.text

# save_file = open(Constant.root_path + 'test.html', 'w+')
# save_file.write(html_script)
# save_file.close()