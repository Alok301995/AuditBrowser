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
    def get_bits_of_info(self, attributes, signature, signature_mobile , is_mobile):
        '''
        Function to get the bits of information from each attribute
        '''
        helper = FingerprintHelper()
        md5_attributes = helper.create_md5_values(attributes)
        response = {}
        result = []
        total_count = db.fetch_count_totals_table()
        
        ###########
        # cookie_c = db.fetch_individual_count('cookie_enabled', md5_attributes['cookie_enabled'])
        # ua_c = db.fetch_individual_count('user_agent', md5_attributes['user_agent'])
        # ha_c = db.fetch_individual_count('http_accept', md5_attributes['http_accept'])
        # # dnt_c  = db.fetch_individual_count('dnt_enabled', md5_attributes['dnt_enabled'])
        # plugin_c = db.fetch_individual_count('plugins', md5_attributes['plugins'])
        # video_c = db.fetch_individual_count('video', md5_attributes['video'])
        # timezone_c = db.fetch_individual_count('timezone', md5_attributes['timezone'])
        # language_c = db.fetch_individual_count('language', md5_attributes['language'])
        # platform_c = db.fetch_individual_count('platform', md5_attributes['platform'])
        # touch_support_c = db.fetch_individual_count('touch_support', md5_attributes['touch_support'])
        # fonts_c = db.fetch_individual_count('fonts', md5_attributes['fonts'])
        # supercookies_c = db.fetch_individual_count('supercookies', md5_attributes['supercookies'])
        # canvas_hash_c  = db.fetch_individual_count('canvas_hash', md5_attributes['canvas_hash'])
        # webgl_hash_c = db.fetch_individual_count('webgl_hash', md5_attributes['webgl_hash'])
        # timezone_string_c = db.fetch_individual_count('timezone_string', md5_attributes['timezone_string'])
        # webgl_v_c = db.fetch_individual_count('webgl_vendor_renderer', md5_attributes['webgl_vendor_renderer'])
        # # ad_c = db.fetch_individual_count('ad_block', md5_attributes['ad_block'])
        # cpu_class_c = db.fetch_individual_count('cpu_class', md5_attributes['cpu_class'])
        # hardware_concurrency_c = db.fetch_individual_count('hardware_concurrency', md5_attributes['hardware_concurrency'])
        # # device_memory_c = db.fetch_individual_count('device_memory', md5_attributes['device_memory'])
        # activity_c = db.fetch_individual_count('activity', md5_attributes['activity'])
        # loads_remote_c = db.fetch_individual_count('loads_remote_fonts', md5_attributes['loads_remote_fonts'])
        # sig_c = db.fetch_individual_count('signature', md5_attributes['signature'])
        
        
        ###########
        cookie_boi = db.find_entropy("cookie_enabled",is_mobile )
        user_agent_boi = db.find_entropy("user_agent",is_mobile)
        http_accept_boi = db.find_entropy("http_accept",is_mobile)
        # dnt_boi = self.bits_of_info('dnt_enabled',dnt_count, total_count , dnt_c)
        plugins_boi = db.find_entropy("plugins",is_mobile)
        video_boi = db.find_entropy("video",is_mobile,  )
        timezone_boi = db.find_entropy("timezone" ,is_mobile)
        language_boi = db.find_entropy("language", is_mobile)
        platform_boi = db.find_entropy("platform", is_mobile)
        touch_support_boi = db.find_entropy("touch_support", is_mobile)
        fonts_boi = db.find_entropy("fonts",is_mobile)
        supercookies_boi = db.find_entropy("supercookies",is_mobile)
        canvas_hash_boi = db.find_entropy("canvas_hash",is_mobile)
        webgl_hash_boi = db.find_entropy("webgl_hash",is_mobile)
        timezone_string_boi = db.find_entropy("timezone_string",is_mobile)
        webgl_v_boi = db.find_entropy("webgl_vendor_renderer",is_mobile)
        # ad_boi = self.bits_of_info('ad_block',ad_count, total_count,  ad_c)
        cpu_class_boi = db.find_entropy("cpu_class",is_mobile)
        hardware_concurrency_boi = db.find_entropy("hardware_concurrency",is_mobile)
        # # device_memory_boi = self.bits_of_info('device_memory',device_memory_count, total_count, device_memory_c)
        activity_boi = db.find_entropy("activity",is_mobile)
        loads_remote_boi = db.find_entropy("loads_remote_fonts",is_mobile)
        # sig_boi = self.bits_of_info('signature',sig_count, total_count)

        
        
        
        
        
        result = [cookie_boi, user_agent_boi, http_accept_boi, plugins_boi, video_boi, timezone_boi, language_boi, platform_boi, touch_support_boi, fonts_boi, supercookies_boi, canvas_hash_boi, webgl_hash_boi, timezone_string_boi, webgl_v_boi, cpu_class_boi, hardware_concurrency_boi, activity_boi, loads_remote_boi]

        signature_count = db.fetch_count(signature, signature_mobile)

        desk_aoi = 0
        mob_aoi  =0
        for i in result:
            desk_aoi += i['ent_desk']
            mob_aoi += i["ent_mob"]
        
        
        for i in result:
            print(i['attribute'] ,i['ent_desk'],i['ent_mob'])
        response['attributes'] = result
        response['desktop'] = desk_aoi
        response['mobile'] = mob_aoi
        

        return response


    ###############################################################################

    def bits_of_info(self, varibale_name, count, total_count):
        '''
        Function to calculate the bits of i
        '''
        bits = round(-log(count / float(total_count), 2), 2)

        return {'attribute': varibale_name, 'bits_of_info': bits}

    ################################################################################
    # def find_entropy(counts , attribute):
    #     etp = 0
    #     total = 0
    #     for i in counts:
    #         total += i[0]
    #     for i in counts:
    #         etp = etp + (i[0]/total)*log(i[0]/total,2)
    #     return etp            
    
    
    
    ################################################################################
    


if __name__ == '__main__':
    pass
