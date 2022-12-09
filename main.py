from tkinter import *
import script




class App:
    def __init__(self,root,localIP):
        root.title("Network Scanner")
        root.geometry("500x600")
        #root.maxsize(1000,800)
        self.label_text = StringVar()
        titleLabel = Label(root, text="Network scanner", bg="orange", font=("Calibri",24))
        titleLabel.pack()        
        localScanButton = Button(root, text="Scan your local network", command=self.localInitialScan)
        localScanButton.pack()        
        label2 = Label(root, text="or scan custom IP/range (e.g.: 192.168.1.1-255):", font=("Calibri",10))
        label2.pack()           
        self.entry_text = StringVar()
        entry = Entry(root, textvariable=self.entry_text)
        entry.pack()
        button = Button(root, text="Begin", command=self.press_button)
        button.pack()
        
    def localInitialScan(self):
        temp = script.getIPv4()
        localLabel = Label(root, text="Your local IP: "+temp[0], font=("Calibri",18))
        localLabel.pack()           
        print(script.initialScan(temp[0],temp[1]))
        deviceList = script.initialScan(temp[0],temp[1])
        for i in range(len(deviceList[0])):
            deviceLabel = Label(root, text="Device name: "+deviceList[0][i]+"\nIP: "+deviceList[1][i]+"\nMAC Address: "+deviceList[2][i]+"\nDevice Type: "+deviceList[3][i]+"\n\n", font=("Calibri",10))
            deviceLabel.pack()                
        
    def press_button(self):
        text = self.entry_text.get()
        self.label_text.set(text)
        print(script.initialScan(text,localIP[1]))
               
     
root = Tk()
localIP = script.getIPv4()
print("Hi")   
App(root,localIP)
print("Hola")
root.mainloop()
print("yo")