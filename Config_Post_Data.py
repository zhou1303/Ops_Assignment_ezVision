import Constant


def config_transport_ops_assignment(csrf, scac):
    data_dict = Constant.transport_by_report_format_dict.copy()
    data_dict['_csrf'] = csrf

    data_dict['filterfield0'] = Constant.field_status
    data_dict['filtercrit0'] = Constant.filter_in
    data_dict['filtervalue0'] = 'Booked, In Transit'

    data_dict['filterfield1'] = Constant.field_customer_code
    data_dict['filtercrit1'] = Constant.filter_not_equal
    data_dict['filtervalue1'] = 'RJR'

    data_dict['filterfield2'] = Constant.field_assigned_to
    data_dict['filtercrit2'] = Constant.filter_equal
    data_dict['filtervalue2'] = ''

    data_dict['filterfield3'] = Constant.field_carrier_scac
    data_dict['filtercrit3'] = Constant.filter_in
    data_dict['filtervalue3'] = scac

    return data_dict


def config_transport_ops_unassignment(csrf, scac):
    data_dict = config_transport_ops_assignment(csrf, scac)
    data_dict['filtercrit2'] = Constant.filter_not_equal
    return data_dict


def config_set_assign_to(csrf, assign_to_object):
    data_dict = Constant.set_assign_to_dict.copy()
    data_dict['_csrf'] = csrf

    data_dict['sAssignTo'] = assign_to_object
    return data_dict

