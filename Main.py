import Constant
import Get_Data
import G_API
import Post_Data
import Config_Post_Data
import time


if __name__ == '__main__':

    #START COUNTING RUNNING TIME
    start = time.time()

    #LOGIN TMS
    Get_Data.read_login_credentials()
    session_requests, csrf = Post_Data.login_tms()

    #READ GOOGLE SHEETS VALUE

    print('Loading Google Sheet...')

    workbook_cr = G_API.get_workbook_by_id(Constant.g_sheets_workbook_id_ops)
    worksheet_cr = G_API.get_worksheet_by_id(workbook_cr, Constant.g_sheets_worksheet_id_ops)
    sheet_values = G_API.get_values_in_list(worksheet_cr)
    sheet_values = G_API.convert_values_to_dict(sheet_values) #Convert value list to dictionary.
    for key, value_list in sheet_values.items():
        sheet_values[key] = ','.join(value_list)
    assert sheet_values is not None, 'Error: Google Sheet is empty or reading failure.'
    print('Google Sheet loading completed.')

    for key, item in sheet_values.items():

        #SET UP FILTER FOR REMOVE ASSIGNMENT BY CARRIER SCAC
        unassign_data_dict = Config_Post_Data.config_transport_ops_unassignment(csrf, item)
        #SET UP FILTER FOR ASSIGN NEW REP BY CARRIER SCAC
        assign_data_dict = Config_Post_Data.config_transport_ops_assignment(csrf, item)
        # SET UP POST REQUEST DATA
        set_unassign_to_dict = Config_Post_Data.config_set_assign_to(csrf, '')
        #SET UP POST REQUEST DATA
        set_assign_to_dict = Config_Post_Data.config_set_assign_to(csrf, key)

        print('Removing current assignment for', key, '...')

        #REMOVE ASSIIGN
        while True:

            response = Get_Data.get_transport_report_by_report_format(session_requests, unassign_data_dict)
            html_script = response.text

            menu_values = Constant.re_pattern_menu_value.findall(html_script)

            if menu_values:
                for menu_value in menu_values:
                    set_unassign_to_dict['sidOwner'] = menu_value
                    Post_Data.transport_set_assign_to(session_requests, set_unassign_to_dict)
            else:
                break

        print('Removing completed.')

        #ASSIGN

        print('Assigning loads to', key, '...')

        count = 0

        while True:

            response = Get_Data.get_transport_report_by_report_format(session_requests, assign_data_dict)
            html_script = response.text

            menu_values = Constant.re_pattern_menu_value.findall(html_script)

            if menu_values:
                for menu_value in menu_values:
                    set_assign_to_dict['sidOwner'] = menu_value
                    Post_Data.transport_set_assign_to(session_requests, set_assign_to_dict)
                    count += 1
            else:
                print('Assigning completed.', count, 'load(s) assigned.')
                break

    #END TIME
    end = time.time()

    #UPDATE LOG REPORT ON GOOGLE SHEETS
    duration = end - start
    workbook_log = G_API.get_workbook_by_id(Constant.g_sheets_workbook_id_log)
    worksheet_log = G_API.get_worksheet_by_id(workbook_log, Constant.g_sheets_worksheet_id_log)
    Post_Data.log_event(worksheet_log, duration)

# save_file = open(Constant.root_path + 'test.html', 'w+')
# save_file.write(html_script)
# save_file.close()