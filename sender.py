#!/usr/bin/python3
# -*- coding : utf-8 -*-

#
# Рассылка сообщений о регистрации на экзамен. Первый параметр - csv 
# файл с данными (email,username,course1,password), второй - шаблон
#

from string import Template
import smtplib
from email.mime.text import MIMEText
from socket import gethostbyaddr, gethostname
from time import sleep
from datetime import datetime
import csv
import sys

log = open('sender.log','a',encoding='utf-8')

def mailPassword(auser):
    sender = "bot@" + str(gethostbyaddr(gethostname())[0])
    ftemplate = open(sys.argv[2],'r',encoding='utf-8')
    body = Template(ftemplate.read())
    mailBody = MIMEText(body.safe_substitute(login=auser['username'],
        course1=auser['course1'],password=auser['password']),'plain',
        _charset='utf-8')
    #print(mailBody.as_string())
    mailBody['From'] = 'no-replay@edu.vsu.ru'
    mailBody['To'] = auser['email']
    mailBody['Subject'] = 'Регистрация на экзамен '+auser['course1']
    try:
        server = smtplib.SMTP("relay1.vsu.ru")
        server.sendmail(sender, auser['email'], mailBody.as_string())
        server.quit()
        log.write(str(datetime.now())+" Почта успешно отправлена на "+auser['email']+"\n")
        return True
    except smtplib.SMTPRecipientsRefused as recipients:
        log.write(str(datetime.now())+" Фигня с отправкой почты на "+auser['email']+"\n")
        return False

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Недостаточно параметров (первый - csv с данными, второй - шаблон письма для рассылки)\n")
        sys.exit(1)
    log.write(str(datetime.now())+" Начинаем работу с "+sys.argv[1]+"\n")

    success = 0
    failure = 0
    infile = open(sys.argv[1],encoding='utf-8')
    users = csv.DictReader(infile,delimiter=",")
    for row in users:  
        #print(row['username']+" "+row['email']+" "+row['password']+" "+row["course1"])
        if (row['group1'] == 'dist') and (row['password'][0] != 'н'):
            #print(row)
            if mailPassword(row):
                success += 1
            else:
                failure += 1
            sleep(0.05)
    print ("Успешно "+str(success)+", ошибок "+str(failure))
    log.write(str(datetime.now())+" Отправили "+str(success)+", ошибок "+str(failure)+"\n")
