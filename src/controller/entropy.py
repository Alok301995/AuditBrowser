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
        
        
        response = {}
        result = []
        total_count = db.fetch_count_totals_table()
        
        
        cookie_count = db.fetch_individual_count('cookie_enabled', md5_attributes['cookie_enabled'])
        ua_count = db.fetch_individual_count('user_agent', md5_attributes['user_agent'])
        ha_count = db.fetch_individual_count('http_accept', md5_attributes['http_accept'])
        # dnt_count  = db.fetch_individual_count('dnt_enabled', md5_attributes['dnt_enabled'])
        plugin_count = db.fetch_individual_count('plugins', md5_attributes['plugins'])
        video_count = db.fetch_individual_count('video', md5_attributes['video'])
        timezone_count = db.fetch_individual_count('timezone', md5_attributes['timezone'])
        language_count = db.fetch_individual_count('language', md5_attributes['language'])
        platform_count = db.fetch_individual_count('platform', md5_attributes['platform'])
        touch_support_count = db.fetch_individual_count('touch_support', md5_attributes['touch_support'])
        fonts_count = db.fetch_individual_count('fonts', md5_attributes['fonts'])
        supercookies_count = db.fetch_individual_count('supercookies', md5_attributes['supercookies'])
        canvas_hash_count  = db.fetch_individual_count('canvas_hash', md5_attributes['canvas_hash'])
        webgl_hash_count = db.fetch_individual_count('webgl_hash', md5_attributes['webgl_hash'])
        timezone_string_count = db.fetch_individual_count('timezone_string', md5_attributes['timezone_string'])
        webgl_v_count = db.fetch_individual_count('webgl_vendor_renderer', md5_attributes['webgl_vendor_renderer'])
        # ad_count = db.fetch_individual_count('ad_block', md5_attributes['ad_block'])
        cpu_class_count = db.fetch_individual_count('cpu_class', md5_attributes['cpu_class'])
        hardware_concurrency_count = db.fetch_individual_count('hardware_concurrency', md5_attributes['hardware_concurrency'])
        # device_memory_count = db.fetch_individual_count('device_memory', md5_attributes['device_memory'])
        activity_count = db.fetch_individual_count('activity', md5_attributes['activity'])
        loads_remote_count = db.fetch_individual_count('loads_remote_fonts', md5_attributes['loads_remote_fonts'])
        sig_count = db.fetch_individual_count('signature', md5_attributes['signature'])
        
        
        cookie_boi = self.bits_of_info('cookie_enabled',cookie_count, total_count)
        user_agent_boi = self.bits_of_info('user_agent',ua_count, total_count)
        http_accept_boi = self.bits_of_info('http_accept',ha_count, total_count)
        # dnt_boi = self.bits_of_info('dnt_enabled',dnt_count, total_count)
        plugins_boi = self.bits_of_info('plugins',plugin_count, total_count)
        video_boi = self.bits_of_info('video',video_count, total_count)
        timezone_boi = self.bits_of_info('timezone',timezone_count, total_count)
        language_boi = self.bits_of_info('language',language_count, total_count)
        platform_boi = self.bits_of_info('platform',platform_count, total_count)
        touch_support_boi = self.bits_of_info('touch_support',touch_support_count, total_count)
        fonts_boi = self.bits_of_info('fonts',fonts_count, total_count)
        supercookies_boi = self.bits_of_info('supercookies',supercookies_count, total_count)
        canvas_hash_boi = self.bits_of_info('canvas_hash',canvas_hash_count, total_count)
        webgl_hash_boi = self.bits_of_info('webgl_hash',webgl_hash_count, total_count)
        timezone_string_boi = self.bits_of_info('timezone_string',timezone_string_count, total_count)
        webgl_v_boi = self.bits_of_info('webgl_vendor_renderer',webgl_v_count, total_count)
        # ad_boi = self.bits_of_info('ad_block',ad_count, total_count)
        cpu_class_boi = self.bits_of_info('cpu_class',cpu_class_count, total_count)
        hardware_concurrency_boi = self.bits_of_info('hardware_concurrency',hardware_concurrency_count, total_count)
        # # device_memory_boi = self.bits_of_info('device_memory',device_memory_count, total_count)
        activity_boi = self.bits_of_info('activity',activity_count, total_count)
        loads_remote_boi = self.bits_of_info('loads_remote_fonts',loads_remote_count, total_count)
        # sig_boi = self.bits_of_info('signature',sig_count, total_count)
        
        result = [cookie_boi, user_agent_boi, http_accept_boi, plugins_boi, video_boi, timezone_boi, language_boi, platform_boi, touch_support_boi, fonts_boi, supercookies_boi, canvas_hash_boi, webgl_hash_boi, timezone_string_boi, webgl_v_boi, cpu_class_boi, hardware_concurrency_boi, activity_boi, loads_remote_boi]
    
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
