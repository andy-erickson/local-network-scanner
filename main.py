from tkinter import *
import script


class App:
    def __init__(self,root,localIP):
        root.title("Network Scanner")
        root.geometry("500x600")
        #root.maxsize(1000,800)
        scrollbar = Scrollbar(root)
        scrollbar.pack( side = RIGHT, fill = Y )        
        self.label_text = StringVar()
        titleLabel = Label(root, text="Network scanner", bg="orange", font=("Calibri",24)).pack(pady=15)       
        localScanButton = Button(root, text="Scan your local network", command=self.localScan)
        localScanButton.pack()
        
        Label(root, text="or other IP/range (e.g.: 192.168.1.1-255):", font=("Calibri",10)).pack(pady=2)
        self.entry_text = StringVar()
        entry = Entry(root, textvariable=self.entry_text)
        entry.pack()
        Button(root, text="Begin", command=self.customScan).pack(pady=10)
        
        
    def localScan(self):
        temp = script.getIPv4()
        localLabel = Label(root, text="Your local IP: "+temp[0], font=("Calibri",18))
        localLabel.pack() 
        deviceList = script.initialScan(temp[0],temp[1])
        self.buildListBox(deviceList)
                  
        
    def customScan(self):
        text = self.entry_text.get()
        self.label_text.set(text)
        localLabel = Label(root, text="Scanning: "+text, font=("Calibri",18))
        localLabel.pack()        
        deviceList = script.initialScan(text,0)
        self.buildListBox(deviceList)

        
    def buildListBox(self, items):
        deviceListBox = Listbox(root)
        deviceListBox.pack()        
        for i in range(len(items[0])):
            try:
                deviceListBox.insert(END, items[0][i])
            except:
                deviceListBox.insert("end", items[0][i])       
        def moreInfo():
            device = deviceListBox.get(ANCHOR)
            itemIndex = items[0].index(device)
            deviceInfo.config(text="Device name: "+items[0][itemIndex]+"\nIP: "+items[1][itemIndex]+"\nMAC Address: "+items[2][itemIndex]+"\nDevice Type: "+items[3][itemIndex])

        my_button = Button(root, text="More info", command=moreInfo)
        my_button.pack()
        global deviceInfo
        deviceStr = StringVar()
        deviceStr.set("aaaa")
        deviceInfo = Label(root, text=deviceStr, bg="white")
        deviceInfo.pack(pady=5)
        deviceInfo.config(text=deviceListBox.get(ANCHOR))
        
        
                
        
               
     
root = Tk()
localIP = script.getIPv4()
print("Hi")   
App(root,localIP)
print("Hola")
root.mainloop()
print("yo")