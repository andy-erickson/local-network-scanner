import subprocess

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
        
    print("Local IP : ",ipArr[0])
    temp = ipArr[0]
    count = 0
    for i in range(len(temp)-1, 0, -1):
        if temp[i].isdigit():
            count += 1
        else: return temp, count
        
ipRange, count = getIPv4()

scan = subprocess.Popen(["nmap", "-sn", ipRange[:-count]+"1-255"], stdout=subprocess.PIPE).communicate()[0]
print(scan)

    


