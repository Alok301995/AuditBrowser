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
        'language': "Language",
        'platform': "Platform",
        'touch_support': "Touch Support",
        'ad_block': "Ad Blocker Used",
        'audio': "AudioContext fingerprint",
        'cpu_class': "CPU Class",
        'hardware_concurrency': "Hardware Concurrency",
        'activity': "Activity",
        'loads_remote_fonts': "Loads Remote Fonts",
    }

    ################################################################################
    
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
