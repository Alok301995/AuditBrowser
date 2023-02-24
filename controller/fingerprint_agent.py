from fastapi import Request 


# Class which contain function to extract server attributes from request object


class FingerprintAgent:

    def __init__(self, request :Request):
        self.request = request
        self.headers =  request.headers

    def detect_server_attributes(self):
        attributes = {}
        # get cookie enabled
        
        # check if cookies are enabled or not
        if self.request.cookies:
            attributes['cookie_enabled'] = 'Yes'
        else:
            attributes['cookie_enabled'] = 'No'
        # get user_agent
        attributes['user_agent'] = self._get_header('user-agent')
        
        
        # Get http_accept 

        attributes['http_accept'] = " ".join([
            self._get_header('accept'),
            self._get_header('accept-charset'),
            self._get_header('accept-encoding'),
            self._get_header('accept-language')
        ])
        
        attributes['dnt_enabled'] = (self._get_header('dnt') != "")
        attributes['plugins'] = u"no javascript"
        attributes['video'] = u"no javascript"
        attributes['timezone'] = u"no javascript"
        attributes['language'] = u"no javascript"
        attributes['platform'] = u"no javascript"
        attributes['touch_support'] = u"no javascript"
        attributes['fonts'] = u"no javascript"
        attributes['supercookies'] = u"no javascript"
        attributes['canvas_hash'] = u"no javascript"
        attributes['webgl_hash'] = u"no javascript"
        attributes['timezone_string'] = u"no javascript"
        attributes['webgl_vendor_renderer'] = u"no javascript"
        attributes['ad_block'] = u"no javascript"
        attributes['audio'] = u"no javascript"
        attributes['cpu_class'] = u"no javascript"
        attributes['hardware_concurrency'] = u"no javascript"
        attributes['device_memory'] = u"no javascript"
        attributes['activity'] =u"no javascript"
        
        attributes['load_remote_fonts'] = u"no javascript"
        
        # attributes['location'] =u"no javascript"
        # vars_v3 = attributes.copy()
        # vars_v3['loads_remote_fonts'] = u"no js"

        return attributes

    def _get_header(self,header):
        return self.headers.get(header) or ""
