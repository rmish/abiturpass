#!/usr/bin/python3
# # -*- coding: utf-8 -*-
"""Объединение ведомости с общим спском паролей
делается поиск каждого человека в ведомости в общем 
списке и формирование нового файла ведомости с добавлением пароля

Параметры командной строки:
  Обязательные:
   первый: файл с ведомостью (csv с разделеителем ";"  текстовыми полями в кавычках)
  Необязательные
   второй: каталог с файлами всех зарегистрированных (csv с разеделителем ";" и текстовыми полми в кавычках)
"""

import sys
import csv
import subprocess

if (len(sys.argv) > 3) or (len(sys.argv) == 1) :
    print('Неверное количество параметров, смотрите комментарии внутри скрипта')
    sys.exit(1)
elif len(sys.argv) == 2 :
    passwordsDir = '/mnt/sys/Приёмная кампания 2021/регистрация общий список/'
    inputFile = sys.argv[1]
else :
    passwordsDir = sys.argv[2]
    inputFile = sys.argv[1]

examList = csv.DictReader(open(inputFile),dialect='unix')
examListPasswords = csv.DictWriter(open(inputFile+'.pass.csv','w'),['username','email', \
    'fullname','password','phone','type'],dialect='excel')    
examListPasswords.writeheader()

for record in examList :
    passString=subprocess.Popen(["grep","-r",record['username'],passwordsDir],stdout=subprocess.PIPE,encoding='utf8')
#    print(passString.stdout.read())
    try :
         passwords=passString.stdout.read().strip().split(':',1)[1]
    except :
        passwords='не зарегиcтрирован'
    password=passwords.split(',')
    try :
        pstring=password[2]
    except:
        pstring = '"не зарегистрирован"'

    tmp = {'username':record['username'],'email':record['email'],'fullname':record['fullname'], \
        'phone':record['phone1'],'type':record['type'],'password':pstring[1:-1]}
    examListPasswords.writerow(tmp)