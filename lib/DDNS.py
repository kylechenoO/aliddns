import os
import re
import sys
import json
import requests
from datetime import datetime
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, DescribeDomainRecordInfoRequest

# class DDNS
class DDNS(object):
    
    def __init__(self, configObj, logger):
        # initial global val
        self.conf = configObj
        self.logger = logger

        # access_key_id
        self.access_key_id = configObj.DOMAIN_ACCESS_KEY_ID
 
        # access_key_secret
        self.access_key_secret = configObj.DOMAIN_ACCESS_KEY_SECRET
 
        # account_id
        self.account_id = configObj.DOMAIN_ACCOUNT_ID
 
        # domain
        self.domain = configObj.DOMAIN_DOMAIN
 
        # prefix
        self.prefix = configObj.DOMAIN_PREFIX
 
        # record type
        self.type = configObj.DOMAIN_TYPE
 
        # record ttl
        self.ttl = configObj.DOMAIN_TTL

        # record_id
        self.record_id = self.get_record_id()

        # self.ip
        self.ip = self.get_ip()
        self.oip = self.old_ip()

    # run func
    def run(self):
        if self.ip != self.oip:
            self.update()
 
    # get ip from ip.cn
    def get_ip(self):
	    get_ip_method = os.popen('curl -s ip.cn')
	    get_ip_responses = get_ip_method.readlines()[0]
	    get_ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
	    get_ip_value = get_ip_pattern.findall(get_ip_responses)[0]
	    self.logger.debug('get_ip {}'.format(get_ip_value))
	    return(get_ip_value)

    # get record id from alidns api
    def get_record_id(self):
        clt = client.AcsClient(self.access_key_id, self.access_key_secret, 'cn-hangzhou')
        request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_DomainName(self.domain)
        request.set_accept_format('json')
        result = clt.do_action_with_exception(request)
        result = json.loads(result)
        result = [ x['RecordId'] for x in result['DomainRecords']['Record'] if x['RR'] == self.prefix ][0]
        self.record_id = result
        self.logger.debug('get_record_id {}'.format(result))
        return(result)
 
    # get old ip from alidns api
    def old_ip(self):
        clt = client.AcsClient(self.access_key_id, self.access_key_secret, 'cn-hangzhou')
        request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
        request.set_RecordId(self.record_id)
        request.set_accept_format('json')
        result = clt.do_action_with_exception(request)
        result = json.JSONDecoder().decode(result)
        result = result['Value']
        self.logger.debug('old_ip {}'.format(result))
        return(result)
 
    # update dns record with alidns api
    def update(self):
        clt = client.AcsClient(self.access_key_id, self.access_Key_secret, 'cn-hangzhou')
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_RR(self.domain)
        request.set_Type(self.type)
        request.set_Value(self.ip)
        request.set_RecordId(self.record_id)
        request.set_TTL(self.ttl)
        request.set_accept_format('json')
        result = clt.do_action_with_exception(request)
        self.logger.debug('update_dns {}'.format(result))
        return(result)
