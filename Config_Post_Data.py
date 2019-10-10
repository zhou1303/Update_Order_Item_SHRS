import Constant


def config_item_edit(csrf, item_info_list, freight_class, weight):
    data_dict = Constant.data_dict_item.copy()
    data_dict['_csrf'] = csrf
    data_dict['bIsShipUnit'] = item_info_list[0]
    data_dict['oid'] = item_info_list[1]
    data_dict['nSequence'] = item_info_list[2]
    data_dict['sItemID'] = item_info_list[3]
    data_dict['sDescription'] = item_info_list[4]
    data_dict['fFreightClass'] = freight_class
    data_dict['sNMFC'] = item_info_list[5]
    data_dict['fOrderedQuantity'] = item_info_list[6]
    data_dict['fPlannedQuantity'] = item_info_list[7]
    data_dict['fActualQuantity'] = item_info_list[8]
    data_dict['fPlannedWeight'] = weight
    data_dict['fActualWeight'] = weight
    data_dict['fLength'] = item_info_list[11]
    data_dict['fWidth'] = item_info_list[12]
    data_dict['fHeight'] = item_info_list[13]
    data_dict['fDeliveredWeight'] = item_info_list[14]
    data_dict['fCube'] = item_info_list[15]
    data_dict['nStackability'] = item_info_list[-4]
    data_dict['sTrackingNumber'] = item_info_list[-3]

    return data_dict


def config_shipment_report(csrf, pri_refs):
    data_dict = Constant.open_shipment_report_by_report_format_dict.copy()
    data_dict['_csrf'] = csrf
    data_dict['col0'] = Constant.field_oid
    data_dict['col1'] = Constant.field_pri_ref
    data_dict['col2'] = Constant.field_congroup
    data_dict['col3'] = Constant.field_customer_gl_code
    data_dict['col4'] = Constant.field_dest_name
    data_dict['col5'] = Constant.field_dest_city

    data_dict['filterfield0'] = Constant.field_pri_ref
    data_dict['filtercrit0'] = Constant.filter_in
    data_dict['filtervalue0'] = pri_refs

    data_dict['filterfield1'] = Constant.field_owner
    data_dict['filtercrit1'] = Constant.filter_begins_with
    data_dict['filtervalue1'] = 'Shear'

    return data_dict


def config_add_ref_shipment(csrf, oid, sid_ref_type, ref_value):
    data_dict = Constant.data_dict_add_ref_shipment.copy()
    data_dict['_csrf'] = csrf
    data_dict['sidOwner'] = '(' + oid + ',3700,0)'
    data_dict['sidReferenceType1'] = sid_ref_type
    data_dict['sReference1'] = ref_value
    return data_dict
