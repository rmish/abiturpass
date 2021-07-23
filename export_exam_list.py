#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
import os
import subprocess

if (len(sys.argv) > 3) or (len(sys.argv) == 1) :
    print('Неверное количество параметров, смотрите комментарии внутри скрипта')
    sys.exit(1)
elif len(sys.argv) == 2 :
    passwordsDir = '/mnt/uop/Приёмная кампания 2021/регистрация общий список/'
    inputFile = sys.argv[1]
else :
    passwordsDir = sys.argv[2]
    inputFile = sys.argv[1]


examList = csv.DictReader(open(inputFile,encoding='utf-8'),dialect='unix',delimiter=';',)
usersList = os.listdir(passwordsDir)
examListPasswords = csv.DictWriter(open(inputFile+'.pass.csv','w',encoding='utf-8',newline=''), \
    ['username','email','fullname','password','phone1','group1','course1','group2','course2'], \
    dialect='excel')    
examListPasswords.writeheader()

for record in examList :
    passwords = []
    for usersFile in usersList:
        tcsv = csv.DictReader(open(passwordsDir+usersFile,encoding='utf-8'),dialect='excel')
        for rcsv in tcsv:
            if rcsv['username'] == record['username'] :
                passwords.append(rcsv['password'])
    if len(passwords) == 0 : 
        pstring = 'не зарегиcтрирован'
    elif len(passwords) >1 :
        pstring = 'несколько учётных записей'
    else :
        pstring = passwords[0]

    tmp = {'username':record['username'],'email':record['email'],'fullname':record['fullname'], \
        'phone1':record['phone1'],'group1':record['type'],'password':pstring, \
        'course1':record['course1'],'course2':record['course1'],'group2':'2021_'+record['group1']}
    examListPasswords.writerow(tmp)
