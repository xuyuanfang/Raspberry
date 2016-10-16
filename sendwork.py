#-*-coding=utf-8-*-
import socket
import fcntl
import struct
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import os

#get ip
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])
try:
    localIP1=get_ip_address('eth0')
except Exception:
    localIP1="米有连上有线网络呢"
    pass
try:
    localIP2=get_ip_address('wlan0')
except Exception:
    localIP2="米有连上无线网络呢"
    pass

# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
 
# Return RAM information (unit=kb) in a list                                      
# Index 0: total RAM                                                              
# Index 1: used RAM                                                                
# Index 2: free RAM                                                                
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
 
# Return % of CPU used by user as a character string                               
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
 
# Return information about disk space as a list (unit included)                    
# Index 0: total disk space                                                        
# Index 1: used disk space                                                        
# Index 2: remaining disk space                                                    
# Index 3: percentage of disk used                                                 
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
 
 
# CPU informatiom
CPU_temp = getCPUtemperature()
CPU_usage = getCPUuse()
 
# RAM information
# Output is in kb, here I convert it in Mb for readability
RAM_stats = getRAMinfo()
RAM_total = round(int(RAM_stats[0]) / 1000,1)
RAM_used = round(int(RAM_stats[1]) / 1000,1)
RAM_free = round(int(RAM_stats[2]) / 1000,1)
 
# Disk information
DISK_stats = getDiskSpace()
DISK_total = DISK_stats[0]
DISK_used = DISK_stats[1]
DISK_perc = DISK_stats[3]
 
if __name__ == '__main__':
    print('')
    print('CPU Temperature = '+CPU_temp)
    print('CPU Use = '+CPU_usage)
    print('')
    print('RAM Total = '+str(RAM_total)+' MB')
    print('RAM Used = '+str(RAM_used)+' MB')
    print('RAM Free = '+str(RAM_free)+' MB')
    print('') 
    print('DISK Total Space = '+str(DISK_total)+'B')
    print('DISK Used Space = '+str(DISK_used)+'B')
    print('DISK Used Percentage = '+str(DISK_perc))


#mail.qq.com
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr="xuyuanfang@vip.qq.com"
password="sim/+*-200818534"
smtp_server="smtp.qq.com"
to_addr="691066230@qq.com"
server = smtplib.SMTP(smtp_server, 25)

#message
msg = MIMEText("主人主人，我来汇报工作啦~"
+"\n有线IP为："'%s'%localIP1 
+"\n无线IP为："'%s'%localIP2 
+"\nCPU温度为："'%s'%CPU_temp+"℃"  
+"\nCPU占用率："'%s'%CPU_usage+"%" 
+"\n内存总量为："'%s'%RAM_total+"MB" 
+"\n内存已占用："'%s'%RAM_used+"MB" 
+"\n内存还剩余："'%s'%RAM_free+"MB"
+"\n磁盘总量为："'%s'%DISK_total+"B"
+"\n磁盘已使用："'%s'%DISK_used+"B"
+"\n磁盘占用率："'%s'%DISK_perc , _subtype='plain', _charset='utf-8')

#email
msg['From'] = _format_addr(u'小派 <%s>' % from_addr)
msg['To'] = _format_addr(u'QQ邮箱 <%s>' % to_addr)
msg['Subject'] = Header(u'来自小派的工作汇报呢', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()