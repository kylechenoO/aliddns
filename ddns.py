# -*- coding: UTF-8 -*-
# 请使用Python2.X来执行此脚本
import json
import os
import re
import sys
import requests
from datetime import datetime
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainRecordsRequest, \
    DescribeDomainRecordInfoRequest
from aliyunsdkcore import client
 
#请填写你的Access Key ID
access_key_id = 'XXX'
 
#请填写你的Access Key Secret
access_Key_secret = 'XXX'
 
#请填写你的账号ID
account_id = 'XXX'
 
#请填写你的一级域名
rc_domain = 'XXX.com'
 
#请填写你的解析记录
rc_rr = 'www'
 
#请填写你的记录类型，DDNS请填写A，表示A记录
rc_type = 'A'
 
#请填写解析记录ID(可以先check_records()获取ID再填写这里)
rc_record_id = 'XXX'
 
#请填写解析有效生存时间TTL，单位：秒
rc_ttl = '600'
 
#请填写返还内容格式，json，xml
rc_format = 'json'
 
# 获取当前IP地址, 有多种方式实现, 我这边最快的是seip.cc就用它了
def my_ip():
	get_ip_method = os.popen('curl -s seip.cc')
	get_ip_responses = get_ip_method.readlines()[0]
	get_ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
	get_ip_value = get_ip_pattern.findall(get_ip_responses)[0]
	return(get_ip_value)

# 获取所有记录与相关信息, 包含rc_record_id
def check_records(dns_domain):
    clt = client.AcsClient(access_key_id, access_Key_secret, 'cn-hangzhou')
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(dns_domain)
    request.set_accept_format(rc_format)
    result = clt.do_action_with_exception(request)
    return(result)
 
# 获取原来的DNS记录值 
def old_ip():
    clt = client.AcsClient(access_key_id, access_Key_secret, 'cn-hangzhou')
    request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    request.set_RecordId(rc_record_id)
    request.set_accept_format(rc_format)
    result = clt.do_action_with_exception(request)
    result = json.JSONDecoder().decode(result)
    result = result['Value']
    return(result)
 
# 更新DNS记录信息 
def update_dns(dns_rr, dns_type, dns_value, dns_record_id, dns_ttl, dns_format):
    clt = client.AcsClient(access_key_id, access_Key_secret, 'cn-hangzhou')
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(dns_rr)
    request.set_Type(dns_type)
    request.set_Value(dns_value)
    request.set_RecordId(dns_record_id)
    request.set_TTL(dns_ttl)
    request.set_accept_format(dns_format)
    result = clt.do_action_with_exception(request)
    return(result)
 
# 将每次IP变动的过程写入日志文件, 以便后续分析
def write_to_file():
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_script_path = sys.path[7]
    print(current_script_path)
    log_file = current_script_path + '/' + 'aliyun_ddns_log.txt'
    write = open(log_file, 'a')
    write.write(time_now + ' ' + str(rc_value) + '\n')
    write.close()
    return(True)
 
# mail run parts 
if __name__ == '__main__':
    # 如果你是第一次运行, 请先执行check_records, 获取相关rc_record_id, 完善文件头中的变量信息后再执行后续操作
	# print check_records(rc_domain)
    # rc_value = my_ip()

    # 获取当前IP
	rc_value = my_ip()
    # 获取当前DNS记录值
	rc_value_old = old_ip()
    # 如果当前IP与DNS记录值一致, 则不更新记录
	if rc_value_old == rc_value:
		print('The specified value of parameter Value is the same as old')

    # 否则更新记录, 写入日志文件
	else:
		print(update_dns(rc_rr, rc_type, rc_value, rc_record_id, rc_ttl, rc_format))
		write_to_file()
