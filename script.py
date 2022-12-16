import subprocess
import re
import time

#returns local wifi IP from substring of ipconfig output on windows
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


# performs initial Nmap scan and returns quick basic information on all devices in 2D array
def initialScan(ip, endCount):
    if endCount != 0:
        scan = subprocess.Popen(["nmap", "-sn", ip[:-endCount]+"1-255", "--exclude", ip], stdout=subprocess.PIPE).communicate()[0]
    else:
        print(ip)
        scan = subprocess.Popen(["nmap", "-sn", ip], stdout=subprocess.PIPE).communicate()[0]
    string = scan.decode("UTF-8")
    startIndexes = [i.start() for i in re.finditer("Nmap scan report for", string)]
    names, ips, macs, deviceTypes = [], [], [], []

    for i in startIndexes:
        end = 0
        mac = None
        sub = string[i+21:]
        sub = sub.replace("\r", '')
        end = sub.find("Nmap scan report for")
        if end == -1:
            end = sub.find("Nmap done:")
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
        names.append(name)
        ips.append(ip)
        macs.append(mac)
        deviceTypes.append(deviceType)
        
    return names, ips, macs, deviceTypes


# calls initialScan and checks for differences between new call and previous call passed in as arg
def logScan(baseScan, ip, endCount):
    newScan = initialScan(ip, endCount)
    redundancy = initialScan(ip, endCount)
    if baseScan[0] != newScan[0] and baseScan[0] != redundancy[0]:
        for i in range(len(baseScan[0])):
            if baseScan[0][i] not in newScan[0] and baseScan[0][i] not in redundancy[0]:
                with open('logFile.txt', 'a') as f:
                    f.write(f"Removed {time.ctime()}\nName: {baseScan[0][i]}\nIP: {baseScan[1][i]}\nMAC: {baseScan[2][i]}\nDevice Type: {baseScan[3][i]}\n\n")
                    print(f"Device removed on {time.ctime()}: {baseScan[0][i]}")
                f.close()
        for i in range(len(newScan[0])):
            if newScan[0][i] not in baseScan[0] and newScan[0][i] in redundancy[0]:
                with open('logFile.txt', 'a') as f:
                    f.write(f"Added {time.ctime()}\nName: {newScan[0][i]}\nIP: {newScan[1][i]}\nMAC: {newScan[2][i]}\nDevice Type: {newScan[3][i]}\n\n")
                    print(f"Device added on {time.ctime()}: {newScan[0][i]}")
                f.close()                        
               
        return newScan
    return baseScan

def newLog(baseScan):
    with open('logFile.txt', 'w') as f:
        for i in range(len(baseScan[0])):
            f.write(f"Added {time.ctime()}\nName: {baseScan[0][i]}\nIP: {baseScan[1][i]}\nMAC: {baseScan[2][i]}\nDevice Type: {baseScan[3][i]}\n\n")
            print(f"Added to log {time.ctime()}: {baseScan[0][i]}")
    f.close()    

def portScan(ip):
    scan = subprocess.Popen(["nmap", "-sS", ip], stdout=subprocess.PIPE).communicate()[0]
    print(scan)
    string = scan.decode()
    loc = string.find("open")
    if loc == -1:
        s = "No open ports found"
        print(s)
        return s        
    else:
        s = f"Port {string[loc-9:loc+4].strip()}"
        print(s)
        return s        
    
    
def tempGUIlog(baseScan, ip, endCount):
    while True:
        time.sleep(60)
        baseScan = logScan(baseScan, ip, endCount)

if __name__ == "__main__": 
    
    ip, endCount = getIPv4()    
    baseScan = initialScan(ip, endCount)
    print(f"Connected devices at {time.ctime()}:\n")
    for i in range(len(baseScan[0])):
        print(f"Name: {baseScan[0][i]}")
        print(f"IP: {baseScan[1][i]}")
        print(f"MAC: {baseScan[2][i]}")
        print(f"Device Type: {baseScan[3][i]}\n")
        
    choice = input("Would you like to log connections? (Y/N): ")
    if choice.upper() == 'Y':
        print("All entries stored to \"logFile.txt\" located in program directory\n")
        newLog(baseScan)
        while True:
            time.sleep(60)
            baseScan = logScan(baseScan, ip, endCount)
    else:
        print("\nGoodbye\n")

    


