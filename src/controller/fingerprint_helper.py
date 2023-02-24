import hashlib


class FingerprintHelper(object):
    '''
    
    All the atributes that are used to generate the fingerprint
    It include the name of the attribute and the description of the attribute
    
    '''
    ################################################################################

    attributes = {
        'user_agent': "User Agent",
        'http_accept': "HTTP_ACCEPT Headers",
        'plugins': "Browser Plugin Details",
        'timezone': "Time Zone Offset",
        'timezone_string': "Time Zone",
        'video': "Screen Size and Color Depth",
        'fonts': "System Fonts",
        'cookie_enabled': "Are Cookies Enabled?",
        'supercookies': "Limited supercookie test",
        'canvas_hash': "Hash of canvas fingerprint",
        'webgl_hash': "Hash of WebGL fingerprint",
        'webgl_vendor_renderer': "WebGL Vendor & Renderer",
        'dnt_enabled': "DNT Header Enabled?",
        'language': "Language",
        'platform': "Platform",
        'touch_support': "Touch Support",
        'ad_block': "Ad Blocker Used",
        'audio': "AudioContext fingerprint",
        'cpu_class': "CPU Class",
        'hardware_concurrency': "Hardware Concurrency",
        'device_memory': "Device Memory (GB)",
        'activity': "Activity",
        'loads_remote_fonts': "Loads Remote Fonts",
        # 'location' : 'Location'
    }

    # Fingerprint Expantion Keys are the list of kes that are used to expand the fingerprint
    # table to store fingerprint data in the database.

    fingerprint_expansion_keys = {
        'keys': [
            'fonts_v2',
            'supercookies_v2',
            'canvas_hash_v2',
            'webgl_hash_v2',
            'timezone_string',
            'webgl_vendor_renderer',
            'ad_block',
            'audio',
            'cpu_class',
            'hardware_concurrency',
            'device_memory'
            'loads_remote_fonts'
        ]
    }

    # There are some keys that are long strings that we want to use the md5 to make
    # it possible to store in the database. It is due to limitation of the database
    # storing long strings

    md5_keys = [
        'plugins',
        'fonts',
        'user_agent',
        'http_accept',
        'supercookies',
        'touch_support',
        'webgl_vendor_renderer',
        'cpu_class'
    ]
    
    ################################################################################

    def create_md5_values(self, attributes):
        '''
        This function is used to convert the long string to md5 hash.
        It will return attributes with some hashed key-value pairs.
        This function is used at time of storing the fingerprint data in the database.

        '''
        md5_attributes = attributes.copy()
        for i in md5_attributes:
            if i in self.md5_keys:
                md5_attributes[i] = hashlib.md5(
                    md5_attributes[i].encode('ascii', 'ignore')).hexdigest()
        return md5_attributes
