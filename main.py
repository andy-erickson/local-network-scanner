from tkinter import *
import script


class App:
    def __init__(self,root,localIP):
        root.title("Network Scanner")
        root.geometry("500x600")
        #root.maxsize(1000,800)
        #scrollbar = Scrollbar(root)
        #scrollbar.pack( side = RIGHT, fill = Y )        
        self.label_text = StringVar()
        global localScanButton, infoLabel,entry, begin
        titleLabel = Label(root, text="Network scanner", bg="orange", font=("Calibri",24)).pack(pady=10)       
        localScanButton = Button(root, text="Scan your local network", command=self.localScan)
        localScanButton.pack()
        
        infoLabel = Label(root, text="or other IP/range (e.g.: 192.168.1.1-255):", font=("Calibri",10)).pack(pady=2)
        self.entry_text = StringVar()
        entry = Entry(root, textvariable=self.entry_text)
        entry.pack()
        begin = Button(root, text="Begin", command=self.customScan).pack(pady=10)
        
        
    def hideOptions(self):
        print("forgetting")
        localScanButton.destroy()
        infoLabel.destroy()
        entry.pack_forget()
        begin.pack_forget()
        
        
    def localScan(self):
        global localLabel
        self.hideOptions
        try:
            deviceListBox.pack_forget()
            infoButton.pack_forget()
            deviceInfo.pack_forget()
            localLabel.pack_forget()
        except:
            pass
           
        #localScanButton.pack_forget()
        temp = script.getIPv4()
        localLabel = Label(root, text="Your local IP: "+temp[0], font=("Calibri",18))
        localLabel.pack(pady=5) 
        deviceList = script.initialScan(temp[0],temp[1])
        self.buildListBox(deviceList)
                  
        
    def customScan(self):
        self.hideOptions
        text = self.entry_text.get()
        self.label_text.set(text)
        try:
            deviceListBox.pack_forget()
            infoButton.pack_forget()
            deviceInfo.pack_forget()                        
            localLabel.pack_forget()
        except:
            pass
        localLabel = Label(root, text="Scanning: "+text, font=("Calibri",18))
        localLabel.pack()        
        deviceList = script.initialScan(text,0)
        self.buildListBox(deviceList)

        
    def buildListBox(self, items):
        global deviceListBox, infoButton, deviceInfo
        logButton = Button(root, text="Log connected devices", command=self.localScan)
        logButton.pack()
        deviceListBox = Listbox(root)
        deviceListBox.pack(padx=20, fill=BOTH)        
        for i in range(len(items[0])):
            try:
                deviceListBox.insert(END, items[0][i])
                if items[3][i] != "Unknown":
                    deviceListBox.itemconfig(END, {'bg':'#efea86'})
                    items[3][i] += "\nSome device information revealed by MAC address"
            except:
                deviceListBox.insert("end", items[0][i])       
        def moreInfo():
            global portScanButton
            device = deviceListBox.get(ANCHOR)
            itemIndex = items[0].index(device)
            deviceInfo.config(text="Device name: "+items[0][itemIndex]+"\nIP: "+items[1][itemIndex]+"\nMAC Address: "+items[2][itemIndex]+"\nDevice Type: "+items[3][itemIndex])
            try:
                portScanButton.pack_forget()
                
            except:
                pass
            
            portScanButton = Button(root, text="Port scan this device", command=lambda: self.portScanDevice(device))
            portScanButton.pack()            
            try:
                #portScanButton.pack_forget()
                pScan.pack_forget()
            except:
                pass
            
            return
                
                            
        infoButton = Button(root, text="More info", command=moreInfo)
        infoButton.pack()    
        deviceStr = StringVar()
        deviceStr.set("aaaa")
        deviceInfo = Label(root, text=deviceStr, bg="white")
        deviceInfo.pack(pady=5)
        deviceInfo.config(text=deviceListBox.get(ANCHOR))
       
        
        
    
    def portScanDevice(self, ip):
        global pScan
        #deviceScanButton = Button(root, text="Port scan this device", command=lambda: Label(root, text=script.portScan(ip),bg="white").pack(fill=BOTH))
        try:
            portScanButton.pack_forget()
            #pScan.pack_forget()
        except:
            pass        


        pScan = Label(root, text=script.portScan(ip),bg="white")
        pScan.pack()
        #portScanButton.pack_forget()
        #Label(root, text=out, bg="white")
        print("got it")
        
    def logScan(self):
        temp = script.getIPv4
        deviceList = script.initialScan(temp[0],temp[1])
        while True:
            time.sleep(60)
            deviceList = script.logScan(deviceList,temp[0],temp[1])
            self.buildListBox(deviceList)
            print("LoGgEd")
            
        
        
        
                
        
               
     
root = Tk()
localIP = script.getIPv4()
print("Hi")   
App(root,localIP)
print("Hola")
root.mainloop()
print("yo")