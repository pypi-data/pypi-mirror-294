import sys
Bte=False
Bto=open
BtX=file
Btz=True
Btf=print
BtS=input
BtI=Exception
Btw=exit
BtU=sys.argv
BtF=sys.Btw
import requests
BtD=requests.post
import os
BtP=os.remove
BtR=os.makedirs
BtO=os.path
from datetime import datetime,timedelta
BtV=datetime.now
Btm=datetime.fromtimestamp
from colorama import init,Fore,Style
import bc_pulse
Bth=bc_pulse.__version__
from bc_pulse import cli
BtH=cli.main
init()
Btv="./"
BtE=BtO.join(Btv,"key.txt")
def Btn(key,check_key=Bte):
 Btr={'resultText':key,'check_key':'true' if check_key else 'false'}
 Bts=BtD("https://www.mod-mon.com/bcsfe_pulse/checkKey.php",data=Btr)
 return Bts
if not BtO.exists(Btv):
 BtR(Btv)
if BtO.exists(BtE):
 BtA=BtO.getctime(BtE)
 Btb=Btm(BtA)
 if BtV()-Btb>timedelta(days=3):
  BtP(BtE)
 else:
  with Bto(BtE,'r')as BtX:
   BtJ=BtX.read().strip()
   Bts=Btn(BtJ,check_key=Btz)
   if Bts.status_code==200:
    Btf("���α׷��� ���������� �����մϴ�.")
    BtH.Main().main()
    BtF(0)
   else:
    Btf(Bts.text)
    Btf("���� 001 : �۵��� �ȵǸ� \"����Ƽ��\" ����Ʈ�� ����")
    BtF(1)
BtC=BtS(f"\n{Fore.GREEN}���ۿ��� {Fore.RESET}{Fore.RED}\"����Ƽ��\"{Fore.RESET}{Fore.GREEN}�� �˻� ���ּ���!{Fore.RESET}\n{Fore.GREEN}�Ǵ� {Fore.RESET}{Fore.RED}\"www.mod-mon.com\"{Fore.RESET}{Fore.GREEN}���� ���� ���ּ���!\n\n{Fore.RESET}{Fore.RED}\"����Ƽ��\"{Fore.RESET}{Fore.GREEN}���� �߱޹��� Ű�� �ٿ���������:{Fore.RESET}\n")
Bts=Btn(BtC)
if Bts.status_code==200:
 Btf("Ű�� ��ȿ�ϸ� ���α׷��� �����մϴ�.")
 Bty=BtD("https://www.mod-mon.com/bcsfe_pulse/updateKey.php",data={'resultText':user_input})
 if Bty.status_code==200:
  if BtO.exists(BtE):
   BtP(BtE)
  try:
   with Bto(BtE,'w')as BtX:
    BtX.write(BtC)
  except BtI as e:
   Btf(f"���� 002 : �۵��� �ȵǸ� \"����Ƽ��\" ����Ʈ�� ����")
   BtF(1)
 else:
  Btf("���� 003 : �۵��� �ȵǸ� \"����Ƽ��\" ����Ʈ�� ����")
  BtF(1)
else:
 Btf(f"\n{Fore.GREEN}Ű�� Ʋ�Ȱų� �̹� ���Ǿ����ϴ�.\n{Fore.RED}\"����Ƽ��\"{Fore.RESET} {Fore.GREEN}����Ʈ���� {Fore.RED}Ű{Fore.RESET}{Fore.GREEN}�� ��߱� ��������.{Fore.RESET}")
 BtF(1)
BtH.Main().main()
Btq=BtU[1:]
for BtK in Btq:
 if BtK.lower()in["--version","-v"]:
  Btf(Bth)
  Btw()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

