# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['USER_AGENT_LIST', 'Proxy', 'ProxyManager']

# Cell
import random, logging
import requests

# Cell
USER_AGENT_LIST = [
       #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    ]

# Cell


class Proxy:

    def __init__(self, proxy):
        self.proxy = proxy
        self.status = 1
        self.fail_count = 0

    def __repr__(self):
        return self.proxy

    def success(self):
        self.fail_count = 0

    def fail(self):
        self.fail_count += 1
        if self.fail_count >= 2:
            self.status = 0
            msg = 'REMOVING proxy {}'.format(self.proxy)
        else:
            msg = 'NOT removing proxy {}'.format(self.proxy)

        logging.info(msg)


class ProxyManager:

    def __init__(self, proxy_list):
        if not isinstance(proxy_list[0], Proxy):
            proxy_list = [Proxy(i) for i in proxy_list]

        self.proxy_list = proxy_list
        self.last_proxy = None
        self.fail_func = None

    def get_proxy_dict(self, proxy):
        if not proxy.startswith('http'): proxy = 'http://' + proxy
        proxy_dict = {"http" : proxy, "https": proxy}
        return proxy_dict

    def get_headers(self):
        ua = random.choice(USER_AGENT_LIST)
        headers = { "Connection" : "close","User-Agent" : ua }
        return headers

    def get_proxy(self):
        valid_proxies = [i for i in self.proxy_list if i.status == 1]
        return random.choice(valid_proxies)

    def captcha_check(self, r):
        if "h5>Please verify you\'re a human to continue." in r.text:
            return True
        return False

    def manual_fail(self):
        if self.last_proxy:
            logging.info("Manual Fail")
            self.last_proxy.fail()



    def one_request(self, url, timeout=30):

        if len(self.proxy_list) == 0:
            logging.info("No more proxies remain")
            raise Exception


        chosen_proxy = self.get_proxy()
        self.last_proxy = chosen_proxy

        proxy_dict = self.get_proxy_dict(chosen_proxy.proxy)
        headers = self.get_headers()

        try:
            r = requests.get(url, headers=headers, proxies=proxy_dict, timeout=timeout)
        except Exception as e:
            chosen_proxy.fail()
            msg = '{} remaining proxies'.format(len([i for i in self.proxy_list if i.status == 1]))
            logging.info(msg)
            logging.info(str(e))
            return {'status':'fail', 'typ':'error', 'status_code':None}


        if r.status_code not in [200, 404]:
            chosen_proxy.fail()
            msg = '{} remaining proxies'.format(len([i for i in self.proxy_list if i.status == 1]))
            logging.info(msg)
            return {'status':'fail', 'typ':'status_code', 'status_code':r.status_code}

        elif r.status_code == 404:
            return {'status':'fail', 'typ':'status_code', 'status_code':r.status_code, 'response':r}


        captcha = self.captcha_check(r)
        if captcha:
            chosen_proxy.fail()
            logging.info('Captcha FAIL')
            msg = '{} remaining proxies'.format(len([i for i in self.proxy_list if i.status == 1]))
            logging.info(msg)
            return {'status':'fail', 'typ':'captcha', 'status_code':None, 'response':r}


        if self.fail_func and self.fail_func(r):
            chosen_proxy.fail()
            logging.info("Manual FAIL")
            msg = '{} remaining proxies'.format(len([i for i in self.proxy_list if i.status == 1]))
            logging.info(msg)
            return {'status':'fail', 'type':'manual', 'status_code':r.status_code, 'response':r}



        chosen_proxy.success()
        return {'status':'success', 'response':r, 'status_code': 200}

    def make_request(self, url, fail_func=None):
        if fail_func:self.fail_func = fail_func

        for i in range(min(len(self.proxy_list),5)):
            result = self.one_request(url)
            if result.get('status') == 'success': return result

        return result