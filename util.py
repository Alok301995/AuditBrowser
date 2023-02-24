import hmac
import re

####################################################################################


def number_format(num, places=0):
    """Format a number with grouped thousands and given decimal places"""

    places = max(0, places)
    tmp = "%.*f" % (places, num)
    point = tmp.find(".")
    integer = (point == -1) and tmp or tmp[:point]
    decimal = (point != -1) and tmp[point:] or ""

    count = 0
    formatted = []
    for i in range(len(integer), 0, -1):
        count += 1
        formatted.append(integer[i - 1])
        if count % 3 == 0 and i - 1:
            formatted.append(",")

    integer = "".join(formatted[::-1])
    return integer + decimal

####################################################################################


def get_ip_hmacs(ip_addr):
    # result looks like 192.168.1
    google_style_ip_split = ip_addr.split(".")[0:3]
    # we're not handling ipv6
    google_style_ip_raw = ".".join(google_style_ip_split)

    google_style_ip = hmac.new(b'', google_style_ip_raw.encode("utf8"), 'MD5').hexdigest()
    ip = hmac.new(b'', ip_addr.encode("utf8"), 'MD5').hexdigest()
    return ip, google_style_ip

####################################################################################


def detect_browser_and_platform(user_agent):
    browser = "other"
    platform = "desktop"
    if user_agent:
        if re.search("firefox", user_agent, re.IGNORECASE):
            browser = "firefox"
            if re.search("android", user_agent, re.IGNORECASE):
                platform = "android"
        elif re.search("msie", user_agent, re.IGNORECASE) or \
                re.search("trident", user_agent, re.IGNORECASE):
            browser = "ie"
        elif re.search("opr\/", user_agent, re.IGNORECASE):
            browser = "opera"
            if re.search("mobile", user_agent, re.IGNORECASE):
                platform = "android"
        elif re.search("chrome", user_agent, re.IGNORECASE):
            browser = "chrome"
            if re.search("android", user_agent, re.IGNORECASE):
                platform = "android"
        elif re.search("fxios", user_agent, re.IGNORECASE):
            platform = "ios"
            browser = "firefox"
        elif re.search("crios", user_agent, re.IGNORECASE):
            platform = "ios"
            browser = "chrome"
        elif re.search("safari", user_agent, re.IGNORECASE):
            browser = "safari"
            if re.search("mobile", user_agent, re.IGNORECASE):
                platform = "ios"
    return {'browser': browser, 'platform': platform}

####################################################################################
