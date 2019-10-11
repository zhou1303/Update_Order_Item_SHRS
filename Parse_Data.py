import Constant
import os
import PyPDF2 as ppdf
import time


def __clean_location_name(location_name):
    location_name = location_name.strip()
    location_name = location_name.replace(Constant.html_equivalence_and, 'and')
    location_name = ''.join(i.lower() for i in location_name if i.isalpha())
    return location_name


def __match_albertsons(location_name):
    if 'albertson' in location_name or \
            'carrs' in location_name or \
            ('jewel' in location_name and 'osco' in location_name) or \
            'lucky' in location_name or \
            'plated' in location_name or \
            'randall' in location_name or \
            'safeway' in location_name or \
            'shaws' in location_name or \
            ('star' in location_name and 'market' in location_name) or \
            ('tom' in location_name and 'thumb' in location_name) or \
            'vons' in location_name:
        return True
    return False


def __match_kroger(location_name):
    if 'kroger' in location_name or \
            'bakers' in location_name or \
            ('city' in location_name and 'market' in location_name) or \
            'dillon' in location_name or \
            ('food' in location_name and 'less' in location_name) or \
            ('food' in location_name and 'co' in location_name) or \
            ('fred' in location_name and 'meyer' in location_name) or \
            'frys' in location_name or \
            'gerbes' in location_name or \
            ('harris' in location_name and 'teeter' in location_name) or \
            ('king' in location_name and 'sooper' in location_name) or \
            ('owen' in location_name and 'market' in location_name) or \
            'qfc' in location_name or \
            ('jay' in location_name and 'food' in location_name and 'c' in location_name) or \
            ('pay' in location_name and 'less' in location_name and 'super' in location_name) or \
            ('smith' in location_name and 'food' in location_name) or \
            'ralphs' in location_name or \
            'mariano' in location_name or \
            'roundys' in location_name:
        return True
    return False


def __match_winco(location_name):
    if 'winco' in location_name:
        return True
    return False


def __match_costco(location_name):
    if 'costco' in location_name:
        return True
    return False


def __match_save_a_lot(location_name):
    if 'save' in location_name and 'lot' in location_name:
        return True
    return False


def __match_smart_n_final(location_name):
    if 'smart' in location_name and 'final' in location_name:
        return True
    return False


def __match_aldi(location_name):
    if 'aldi' in location_name:
        return True
    return False


def __match_keefe(location_name):
    if 'keefe' in location_name:
        return True
    return False


def __match_save_mart(location_name):
    if 'save' in location_name and 'mart' in location_name:
        return True
    return False


def __match_publix(location_name):
    if 'publix' in location_name:
        return True
    return False


def __match_stater_brother(location_name):
    if 'stater' in location_name and 'brother' in location_name:
        return True
    return False


def __match_trader_joe(location_name):
    if 'trader' in location_name and 'joe' in location_name:
        return True
    return False


def __match_ics_perham(location_name):
    if 'perham' in location_name and 'ics' in location_name:
        return True
    return False


def __match_sysco(location_name):
    if 'sysco' in location_name:
        return True
    return False


def __match_us_foods(location_name):
    if 'us' in location_name and 'foods' in location_name:
        return True
    return False


def __match_circle_k(location_name):
    if 'circlek' in location_name:
        return True
    return False


def __match_cns(location_name):
    if 'cands' in location_name or 'cns' in location_name:
        return True
    return False


def __match_affiliated_foods(location_name):
    if 'affiliated' in location_name and 'foods' in location_name:
        return True
    return False


def __match_food_lion(location_name):
    if 'food' in location_name and 'lion' in location_name:
        return True
    return False


def __match_brookshire_grocery(location_name):
    if 'brookshire' in location_name and 'grocery' in location_name:
        return True
    return False


def __match_heb(location_name):
    if 'heb' in location_name or 'hegrocery' in location_name:
        return True
    return False


def __match_giant_eagle(location_name):
    if ('giant' in location_name and 'eagle' in location_name) or \
            ('ok' in location_name and 'grocery' in location_name):
        return True
    return False


def __match_dollar_general(location_name):
    if ('dollar' in location_name and 'general' in location_name):
        return True
    return False


def __match_target(location_name):
    if 'target' in location_name:
        return True
    return False


def __group_location_by_name(location_name, location_city, congroup):
    location_name = __clean_location_name(location_name)
    if congroup == 'Safeway' or congroup == 'Albertsons' or __match_albertsons(location_name):
        return 91588
    elif congroup == 'Kroger' or __match_kroger(location_name):
        return 91515
    elif congroup == 'CostCo' or __match_costco(location_name):
        return 91408
    elif congroup == 'Winco' or __match_winco(location_name):
        return 91567
    elif congroup == 'SAVE A LOT' or __match_save_a_lot(location_name):
        return 91589
    elif congroup == 'Smart & Final' or __match_smart_n_final(location_name):
        return 93036
    elif __match_aldi(location_name):
        return 91530
    elif __match_keefe(location_name):
        return 93021
    elif __match_save_mart(location_name):
        return 93035
    elif congroup == 'Publix' or __match_publix(location_name):
        return 91538
    elif congroup == 'Stater Brothers' or __match_stater_brother(location_name):
        return 93081
    elif congroup == 'Trader Joes' or __match_trader_joe(location_name):
        return 93065
    elif __match_ics_perham(location_name):
        return 93066
    elif congroup == 'Sysco' or __match_sysco(location_name):
        return 93123
    elif congroup == 'US Foods' or __match_us_foods(location_name):
        return 93125
    elif congroup == 'Circle K' or __match_circle_k(location_name):
        return 91472
    elif congroup == 'C&S' or __match_cns(location_name):
        return 91517
    elif __match_affiliated_foods(location_name):
        return 91583
    elif __match_food_lion(location_name):
        return 91514
    elif __match_brookshire_grocery(location_name):
        return 91574
    elif congroup == 'HEB' or __match_heb(location_name):
        return 91417
    elif congroup == 'Giant Eagle' or __match_giant_eagle(location_name):
        return 91414
    elif congroup == 'Dollar General' or __match_dollar_general(location_name):
        return 91411
    elif congroup == 'Target' or __match_target(location_name):
        return 93052
    elif 'shearer' in location_name:
        if 'navarre' in location_city:
            return 91612
        elif 'hermiston' in location_city:
            return 91614
        elif 'waterford' in location_city:
            return 93068
        elif 'perham' in location_city:
            return 93066
        elif 'newport' in location_city:
            return 91616
        elif 'phoenix' in location_city:
            return 93067
        elif 'bristol' in location_city:
            return 91613
        elif 'burlington' in location_city:
            return 91617
        elif 'brewster' in location_city:
            return 91612
        elif 'lubbock' in location_city:
            return 93163
    else:
        return -1


def get_gl_code(dict_list):
    for i, value in enumerate(dict_list):
        if value['Customer GL Code'] == '':
            gl_code = __group_location_by_name(value['Dest Name'], value['Dest City'], value['ConGroup'])
        else:
            gl_code = -1
        dict_list[i]['Customer GL Code'] = str(gl_code)
    return dict_list


def get_pdf_cube():

    print('Extracting cube data from PDF files...')

    cube_dict = dict()
    files = os.listdir(Constant.shearers_pdf_path)
    current_time = time.time() # The timestamp of the current time.

    for file in files:
        if '.pdf' in file:
            file = Constant.shearers_pdf_path + file
            file_ctime = os.path.getctime(file) # The timestamp when the file was created.

            # Only look back PDFs that were created in past 4 days.
            diff = 60*60*24*5 # sec*min*hour*day

            if current_time - file_ctime < diff:
                pdf_obj = open(file, 'rb')
                pdf_read = ppdf.PdfFileReader(pdf_obj)
                pdf_page0 = pdf_read.getPage(0)
                pdf_lines = pdf_page0.extractText()
                pdf_obj.close()

                pri_ref = Constant.re_pattern_pdf_pri_ref.findall(pdf_lines)[0]
                cube = Constant.re_pattern_pdf_number.findall(pdf_lines)[0]

                cube_dict[pri_ref] = float(cube.replace(',', ''))
    print('Cube data extracted successfully.')
    return cube_dict
