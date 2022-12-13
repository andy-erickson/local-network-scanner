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
        #button.pack(pady=10)
        #deviceListBox = Listbox(root)
        #deviceListBox.pack()
        
    def localScan(self):
        temp = script.getIPv4()
        localLabel = Label(root, text="Your local IP: "+temp[0], font=("Calibri",18))
        localLabel.pack() 
        #print(script.initialScan(temp[0],temp[1]))
        deviceList = script.initialScan(temp[0],temp[1])
        self.buildListBox(deviceList)
        """
        deviceListBox = Listbox(root)
        deviceListBox.pack()        
        for i in range(len(deviceList[0])):
            try:
                deviceListBox.insert(END, deviceList[0][i])
            except:
                deviceListBox.insert("end", deviceList[0][i])
                """
        """
            deviceLabel = Label(root, text="Device name: "+deviceList[0][i]+"\nIP: "+deviceList[1][i]+"\nMAC Address: "+deviceList[2][i]+"\nDevice Type: "+deviceList[3][i]+"\n\n", font=("Calibri",10))
            deviceLabel.pack()"""                
        
    def customScan(self):
        text = self.entry_text.get()
        self.label_text.set(text)
        deviceList = script.initialScan(text,0)
        self.buildListBox(deviceList)
        #print(baseResults)
        
    def buildListBox(self, items):
        deviceListBox = Listbox(root)
        deviceListBox.pack()        
        for i in range(len(items[0])):
            try:
                deviceListBox.insert(END, items[0][i])
            except:
                deviceListBox.insert("end", items[0][i])        
               
     
root = Tk()
localIP = script.getIPv4()
print("Hi")   
App(root,localIP)
print("Hola")
root.mainloop()
print("yo")