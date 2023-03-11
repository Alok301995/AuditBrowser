from math import log
from src.model import Database
from src.controller import FingerprintHelper


################################################################################
db = Database('database.db')
################################################################################


class Entropy(object):
    '''
    Class to get information value from each attribute and combined signature
    '''

    def __init__(self) -> None:
        pass

    ################################################################################
    def get_bits_of_info(self, attributes, signature, signature_mobile):
        '''
        Function to get the bits of information from each attribute
        '''

        helper = FingerprintHelper()
        md5_attributes = helper.create_md5_values(attributes)

        list = ['cookie_enabled', 'user_agent', 'http_accept', 'dnt_enabled', 'plugins', 'video', 'timezone', 'language', 'platform', 'touch_support', 'fonts', 'supercookies', 'canvas_hash',
                'webgl_hash', 'timezone_string', 'webgl_vendor_renderer', 'ad_block', 'audio', 'cpu_class', 'hardware_concurrency', 'device_memory', 'activity', 'loads_remote_fonts',]

        response = {}
        result = []
        total_count = db.fetch_count_totals_table()
        for i in list:
            count = db.fetch_individual_count(i, md5_attributes[i])
            # print(i ,md5_attributes[i], count, total_count)
            boi = self.bits_of_info(i, count, total_count)
            result.append(boi)

        signature_count = db.fetch_count(signature, signature_mobile)

        desk_aoi = self.bits_of_info(
            'signature_desktop', signature_count[0][0], signature_count[0][1])
        mob_aoi = self.bits_of_info(
            'signature_mobile', signature_count[1][0], signature_count[1][1])

        response['attributes'] = result
        response['desktop'] = desk_aoi
        response['mobile'] = mob_aoi

        return response

    ################################################################################

    def bits_of_info(self, varibale_name, count, total_count):
        '''
        Function to calculate the bits of i
        '''
        bits = round(-log(count / float(total_count), 2), 2)

        return {'attribute': varibale_name, 'bits_of_info': bits}

    ################################################################################


if __name__ == '__main__':
    pass
