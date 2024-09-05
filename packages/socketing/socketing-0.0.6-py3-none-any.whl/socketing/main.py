import time
import os
import getpass
import keyboard

def connect():
    key = getpass.getpass(prompt='')

    if key == "a1":
        a1_text = r"""from socket import *
from datetime import datetime

serverIp = "127.0.0.1"
serverPort = 1000
maxBytes = 4096

sock = socket(AF_INET, SOCK_DGRAM, SOCK_STREAM)
sock.bind((serverIp, serverPort))

sock.listen()

while True:
    message, clientAddress = sock.recvfrom(maxBytes)
    connectionSocket, address = sock.accept()
    message = connectionSocket.recv(maxBytes)
    print(f"Nhận dữ liệu lúc: {datetime.now()}")
    print(f"Độ dài: {len(message)}")

    message = message.decode()
    modifiedMessage = message.upper()
    sock.sendto(modifiedMessage.encode(), clientAddress)

    with open("content1.txt", mode="wt", encoding="utf-8") as f:
        f.write(message.decode())
    
    with open("content1.png", mode="wb") as f:
        f.write(message)
        """
        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a1_text)
    
    if key == "a11":
        a11_text = r"""from socket import *

serverIp = "127.0.0.1"
serverPort = 1000
maxBytes = 4096

sock = socket(AF_INET, SOCK_DGRAM, SOCK_STREAM)
sock.connect((serverIP, serverPort))
data = "Lập trình mạng"

sock.sendto(data.encode(), (serverIp, serverPort))
sock.send(data.encode())
message, serverAddress = sock.recvfrom(maxBytes)
modifiedMessage = sock.recv(maxBytes)
sock.close()
print(message.decode())

with open("content.txt",mode="rt", encoding="utf-8") as f:
    data = f.read()

with open("a.png",mode="rb") as f:
    data = f.read()
        """
        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a11_text)

    if key == "a2":
        a2_text = r"""import socket

serverIP = "127.0.0.10"
serverPort = 1000
maxBytes = 4096

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((serverIP, serverPort))
sock.listen()
while True:
  connectionSocket, address = sock.accept()
  message = connectionSocket.recv(maxBytes)
  try:
    filename = message.decode().split()[1][1:]
    with open(filename, mode='rt', encoding='utf-8') as f:
      data = f.read()
      pass
    responseMessage = f"HTTP/1.1 200 OK\r\n\r\n{data}"
  except:
    data = "<p>Khong tim thay du lieu trong bo nho cua Server</p>"
    responseMessage = f"HTTP/1.1 404 Not Found\r\n\r\n{data}"
    pass
  connectionSocket.send(responseMessage.encode())
  connectionSocket.close()
  pass
        """
        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a2_text)

    if key == "a12":
        a12_text = r"""import socket
serverIP = "128.119.245.12"
serverPort = 80
maxBytes = 4096

request_message = "\
GET /wireshark-labs/INTRO-wireshark-file1.html HTTP/1.1\r\n\
Host: gaia.cs.umass.edu\r\n\
User-Agent: Group work 1\r\n\
Connection: keep-alive\r\n\
Accept-Language: vn\r\n\
\r\n\
"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((serverIP, serverPort))

sock.send(request_message.encode())
while True:
  resposeMessage = sock.recv(maxBytes)
  if resposeMessage == b"":
    break
  resposeMessage = resposeMessage.decode()
  print(resposeMessage)
  pass
sock.close()
        """
        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a12_text)

    if key == "a3":
        a3_text = r"""import socket

serverIP = "127.0.0.20"
serverPort = 2000
maxBytes = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((serverIP, serverPort))
sock.listen()
while True:
  connectionSocket, address = sock.accept()
  message = connectionSocket.recv(maxBytes)
  try:
    path = 'OriginWebServer/'
    filename = message.decode().split()[1][1:]
    with open(path+filename, mode='rt', encoding='utf-8') as f:
      data = f.read()
      pass
    responseMessage = f"HTTP/1.1 200 OK\r\n\r\n{data}"
  except:
    data = "<p>Khong tim thay du lieu trong bo nho cua Server</p>"
    responseMessage = f"HTTP/1.1 404 Not Found\r\n\r\n{data}"
    pass
  connectionSocket.send(responseMessage.encode())
  connectionSocket.close()
  pass
        """
        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a3_text)
    
    if key == "a13":
        a13_text = r"""import socket
serverIP = "127.0.0.10"
serverPort = 1000
maxBytes = 4096

request_message = "\
GET /Helloworld.html HTTP/1.1\r\n\
Host: localhost\r\n\
User-Agent: Group work 3\r\n\
\r\n\
"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((serverIP, serverPort))

sock.send(request_message.encode())
resposeMessage = sock.recv(maxBytes)
sock.close()

resposeMessage = resposeMessage.decode()
print(resposeMessage)
        """
        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a13_text)

    if key == "a23":
        a23_text = r"""import socket

proxyIP = "127.0.0.10"
serverPort = 1000
maxBytes = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((proxyIP, serverPort))
sock.listen()
while True:
  connectionSocket, address = sock.accept()
  message = connectionSocket.recv(maxBytes)
  filename = message.decode().split()[1][1:]
  try:
    with open(filename, mode='rt', encoding='utf-8') as f:
      data = f.read()
      pass
    responseMessage = f"HTTP/1.1 200 OK\r\n\r\n{data}"
  except:
    print("Khong co du lieu tu may chu tam thoi")
    serverIP = "127.0.0.20"
    serverPort = 2000
    server_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_Sock.connect((serverIP, serverPort))

    request_message = f"\
    GET /{filename} HTTP/1.1\r\n\
    Host: localhost\r\n\
    User-Agent: Group work 4\r\n\
    \r\n\
    "
    server_Sock.send(request_message.encode())
    RM_Temp = server_Sock.recv(maxBytes).decode()

    statusCode = RM_Temp.split()[1]
    ind = RM_Temp.find("\r\n\r\n") + 4
    data = RM_Temp[ind:]
    if statusCode=='200':
      with open(filename, mode='wt', encoding='utf-8') as f:
        f.write(data)
        print("Da luu du lieu tu may chu goc")
        pass
      responseMessage = f"HTTP/1.1 200 OK\r\n\r\n{data}"
    else:
      data = "<p>Khong tim thay du lieu tu may chu goc va tam thoi</p>"
      responseMessage = f"HTTP/1.1 404 Not Found\r\n\r\n{data}"
      pass
    pass
  connectionSocket.send(responseMessage.encode())
  connectionSocket.close()
  pass
        """
        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a23_text)

    if key == "a4":
        a4_text = r"""import dns.resolver 

def lookup(hostname):
  qtypes = ['AAAA', 'A', 'CNAME', 'MX', 'NS']
  for qtype in qtypes:
    answer = dns.resolver.resolve(hostname, qtype, raise_on_no_answer=False)
    if answer.rrset is not None:
      print(f"Loại bản ghi: {qtype}")
      print(f"Thời gian tồn tại của bản ghi: {answer.rrset.ttl}")
      if qtype=='NS':
        print(f"Tên chính tắc của tên miền: {hostname}")
      elif qtype=='MX':
        print(f"Tên của máy chủ thư điện tử được liên kết với tên miền: {hostname}")
      for item in answer.rrset.items:
        print(str(item)[:-1])
        # print(" ",item)
  pass

hostname = 'outlook.com'
print(f"Hostname: {hostname}")
lookup(hostname)
"""
        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a4_text)

    if key == "a5":
        a5_text = r"""import smtplib
from email.message import EmailMessage

EMAIL = 'laptrinhmang@outlook.com'
PASSWORD = 'LTM.DHCNHN.HaUI'
DESTINATION_EMAIL = 'laptrinhmang.haui@gmail.com'

SUBJECT_EMAIL = "Báo cáo nhóm"
BODY_EMAIL = "Thân gửi An,\n\nTôi gửi bạn báo cáo được đính kèm trong email này.\n\nTrân trọng."

msg = EmailMessage()
msg['To'] = DESTINATION_EMAIL
msg['To'] = "a@b.com, b@b.com, c@b.com"
msg['From'] = EMAIL
msg['Subject'] = SUBJECT_EMAIL
msg.set_content(BODY_EMAIL)

attachment_path = 'content.rar'
with open(attachment_path, 'rb') as f:
  data = f.read()
msg.add_attachment(data, maintype='text', subtype='plain', filename=f.name)

mailServer = 'smtp.office365.com'
mailPort = 587  

connection = smtplib.SMTP(mailServer, mailPort)
connection.starttls()
connection.login(EMAIL, PASSWORD)
connection.send_message(msg=msg, from_addr=EMAIL, to_addrs=DESTINATION_EMAIL)
connection.sendmail(msg=msg, from_addr=EMAIL, to_addrs=["a@b.com", "b@b.com", "c@b.com"])
connection.quit()"""

        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a5_text)
    
    if key == "a15":
        a15_text = r"""import poplib, imapclient
EMAIL = 'laptrinhmang@outlook.com'
PASSWORD = 'LTM.DHCNHN.HaUI'
mailServer = 'outlook.office365.com'
POP_object = poplib.POP3_SSL(mailServer)
IMAP_object = imapclient.IMAPClient(mailServer, ssl=True,)
try:
  POP_object.user(EMAIL)
  POP_object.pass_(PASSWORD)
  IMAP_object.login(EMAIL, PASSWORD)
except:
  print("Đăng nhập không thành công")
else:
  response, listings, octet_count = POP_object.list()
  if not listings:
    print("Không có hòm thư nào")
  for listing in listings:
    number, size = listing.decode().split()
    print(f"Hòm thư thứ {number} có kích thước {size} bytes")
    pass
  print()
  data = IMAP_object.list_folders()
  for flags, delimiter, folder_name in data:
    print(flags[0].decode(), delimiter.decode(), folder_name)
    pass
finally:
  POP_object.quit()
  IMAP_object.logout()"""

        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a15_text)

    if key == "a6":
        a6_text = r"""import ftplib, os
host = 'ftp.ibiblio.org'
filename = 'profil.tgz'
ftp = ftplib.FTP(host)
print("Welcome:", ftp.getwelcome())
ftp.login()
print(f"Đường dẫn hiện tại: {ftp.pwd()}")
ftp.cwd('/pub/linux/kernel')
print(f"Đường dẫn sau khi đổi: {ftp.pwd()}")
if os.path.exists(filename):
 print(f"Ghi đè tập tin {filename}")
with open(filename, 'wb') as f:
 ftp.retrbinary(f"RETR {filename}", f.write)
 pass
entries = []
ftp.dir(entries.append)
print(entries[4].split())
ftp.quit()


# ftp.dir()
# ftp.nlst()"""

        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a6_text)

    if key == "a16":
        a16_text = r"""with open(file, 'w') as f:
 def writeline(data):
    f.write(data)
    # f.write(os.linesep)
    f.write('\n')
    pass
 ftp.retrlines(f"RETR {file}", writeline)
 pass

with open(file, 'wb') as f:
 ftp.retrbinary(f"RETR {file}", f.write)
 pass

ftp.voidcmd("TYPE I")
socket, size = ftp.ntransfercmd(f"RETR{file}")
data = socket.recv(2048)

ftp.voidresp()
entries = []
ftp.dir(entries.append)"""

        with open("a.py", "wt", encoding="utf-8") as f:
            f.write(a16_text)