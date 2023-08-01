# -*- coding: utf-8 -*-
'''
Скрипт проверяет доступность по snmp и получает значение имени через snmp.
Если имя не удалось сохранить в базе то ему добавляется адресс после имени
это обеспечивает уникальность имени в бд.
'''


import re
import commands
import subprocess
import os
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from noc.sa.models.managedobject import ManagedObject
from noc.sa.models.objectstatus import ObjectStatus
from noc.core.mongo.connection import connect

connect()

def snmpname_get(m):
    #print(m.name, m.address, m.profile, m.snmp_ro) # ОТЛАДКА
    
    # Проверяем наличие community для объекта и его статус
    #if m.snmp_ro and ObjectStatus.get_status(m):
    if m.snmp_ro:
        # Опрашиваем устройство
        cmd = "/usr/bin/snmpget -t 2 -r 1 -v 2c -Oqv -c {} {} .1.3.6.1.2.1.1.5.0 ".format(m.snmp_ro, m.address)
        #print(cmd)
        #cmd = "/usr/bin/snmpget"
        #par = "-t 2 -r 1 -v 2c -Oqv -c {} {} .1.3.6.1.2.1.1.5.0 ".format(m.snmp_ro, m.address)
        #snmpname = commands.getoutput(cmd).replace('"', '')
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            #print ('Device: {}\tSNMP_Result: {}'.format(m.address, 'snmp error')) # ОТЛАДКА
            #print (m.name)
            return 'no_snmp'
            #raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        #output = os.system(cmd)
        #print(output)
        snmpname = '{}'.format(output).replace('"', '').replace('b\'', '').replace('\\n\'', '')

        #print ('Device: {}\tSNMP_Result: {}'.format(m.address, snmpname)) # ОТЛАДКА
        
        # Если hostname отсутствует или опрос по SNMP неудачен - записываем IP-адрес в качество hostname
        if any([not snmpname, 'Timeout' in snmpname, 'No Such Object' in snmpname]):
            snmpname = m.address
        else:
            # Проверяем hostname, полученный по SNMP
            match = snmp_regex.search(snmpname.split('.')[0])
            # Если проверка выявляет совпадение и адрес объекта не loopback,
            # то дописываем к hostname ip-адрес
            if match and not any([m.address.startswith(x) for x in loopbacks]):
                snmpname = '{}-{}'.format(snmpname, m.address)
                #print ('Device: {}\tNot_Loopback: {}'.format(m.address, snmpname)) # ОТЛАДКА

        # Если текущий snmpname не совпадает с записью в базе
        #print ('name: {}\tsnmp: {}'.format(m.name,snmpname))
        if snmpname != m.name:
            #print('Device: {}\tSNMP_Name: {}\tBD_Name: {}'.format(m.address, snmpname, m.name)) # ОТЛАДКА
            m.name = snmpname
            # Пробуем записать в базу
            try:
                m.save()
                return 'Good'
            # Если запись в базу не удалась по причине совпадения имени - добавляем к имени ip-адрес
            except:
                m.name = '{}-{}'.format(m.name, m.address)
                #print ('Duplicate: {}\tNew_Hostname {}'.format(ManagedObject.objects.get(name=snmpname), m.name)) # ОТЛАДКА
                # тут всё может сломаться на сохранении из-за дубляжа ID
                try:
                    m.save()
                    return 'Duplicate'
                except:
                    print ("Error save")
                    return 'Error'
        else:
            if snmpname != m.address:
                return 'Name_in_DB'
            else:
                return 'IP_in_DB'


def multithread_snmp(objects, max_workers):
    pool = ThreadPool(max_workers)
    result = pool.map(snmpname_get, objects)
    pool.close()
    pool.join()

    return result


if __name__ == '__main__':
    # задаем количество потоков
    max_workers = 20
    # задаем правило проверки hostname роутеров
    snmp_regex = re.compile('(-RB-|\.RB\.|CORE)', re.IGNORECASE)
    snmp_regex = re.compile('(.*)', re.IGNORECASE)
    # Адреса loopback
    loopbacks = ['10.254.', '10.255.']
    # получаем список объектов, имеющих snmp_ro
    #mo = ManagedObject.objects.filter(is_managed=True,snmp_ro__isnull=False)
    mo = ManagedObject.objects.filter(is_managed=True,administrative_domain=2,object_profile=3)
    # Засекаем время
    start_time = datetime.now()
    # запускаем опрос hostname объектов по SNMP в заданное количество потоков
    result = multithread_snmp(mo, max_workers)
    # Останавливаем время
    end_time = datetime.now() - start_time

    # Статистика отработки
    print ('{:=^40}'.format(' Result '))
    print ('{:<25} {:<14}'.format('Total device count:', len(mo)))
    print ('{:<25} {:<14}'.format('Name = hostname in DB:', result.count('Name_in_DB')))
    print ('{:<25} {:<14}'.format('Name = IP in DB:', result.count('IP_in_DB')))
    print ('{:<25} {:<14}'.format('Good add in DB:', result.count('Good')))
    print ('{:<25} {:<14}'.format('Duplicate add in DB:', result.count('Duplicate')))
    print ('{:<25} {:<14}'.format('Error add in DB:', result.count('Error')))
    print ('{:<25} {:<14}'.format('Error get SNMP:', result.count('no_snmp')))
    print ('\n{:<25} {:<14}'.format('Threads number:', max_workers))
    #print ('{:<25} {:<14}'.format('Run time:', end_time))
    print ('=' * 40)