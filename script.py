import subprocess
import re

#returns local wifi IP from substring of return from ipconfig on windows
def getIPv4(): 
    ipScan = subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE).communicate()[0]
    string = ipScan.decode()

    wifiIndex = string.find("Wireless LAN adapter Wi-Fi:")
    sub = string[wifiIndex:]
    ipIndex = sub.find("IPv4 Address")
    ipSub = sub[ipIndex+12:]
    ip = ''
    ipArr = []
    for i, digit in enumerate(ipSub):
        if digit.isnumeric():
            ip += digit
        if digit == '.':
            if ipSub[i+1] == ' ':
                if ip != '':
                    ipArr.append(ip)
                    ip = ''
                continue
            ip += digit 
        
    print(f"Local IP : {ipArr[0]}\n")
    temp = ipArr[0]
    count = 0
    for i in range(len(temp)-1, 0, -1):
        if temp[i].isdigit():
            count += 1
        else: return temp, count

#def initialScan():        
ipRange, count = getIPv4()

scan = subprocess.Popen(["nmap", "-sn", ipRange[:-count]+"1-255", "--exclude", ipRange], stdout=subprocess.PIPE).communicate()[0]
string = scan.decode("UTF-8")
#print(scan)
startIndexes = [i.start() for i in re.finditer("Nmap scan report for", string)]
names = []
ips = []
macs = []
deviceTypes = []
for i in startIndexes:
    end = 0
    mac = None
    sub = string[i+21:]
    sub = sub.replace("\r", '')
    end = sub.find("Nmap scan report for")
    if end == -1:
        end = sub.find("Nmap done:")
    #print(sub[:end])
    sub = sub[:end]
    if sub.find("\n") < sub.find('('):
        name = sub[:sub.find("\n")]
        ip = name
    else:
        name = sub[:sub.find('(')]
        ip = sub[len(name)+1:sub.find(')')]
    macIndex = sub.find("MAC Address:")
    if macIndex != -1:
        mac = sub[macIndex+13:sub.find(' ', macIndex+13)]
        deviceType = sub[sub.find('(',macIndex+13)+1:sub.find(')',macIndex+13)]
    #print(f"Name: {name}")
    #print(f"IP: {ip}")
    #print(f"MAC Address: {mac}")
    #print(f"Device Type: {deviceType}")
    #print()
    names.append(name)
    ips.append(ip)
    macs.append(mac)
    deviceTypes.append(deviceType)
print(names)
print(ips)
print(macs)
print(deviceTypes)
               
    
    


