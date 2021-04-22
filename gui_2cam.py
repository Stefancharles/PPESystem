import tkinter as tk
import threading
from PIL import ImageTk, Image
import cv2


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.title("PPE System")
        self.root.geometry("1340x850")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.configure(bg='white')
        label1 = tk.Label(self.root, text="Persons with helmet : ",font=("Ubuntu Mono", 10),bg = 'white').place(x=10, y=530)
        label2 = tk.Label(self.root, text="Persons without helmet : ",font=("Ubuntu Mono", 10),bg = 'white').place(x=10, y=550)
        label3 = tk.Label(self.root, text="Persons with helmet : ",font=("Ubuntu Mono", 10),bg = 'white').place(x=440, y=530)
        label4 = tk.Label(self.root, text="Persons without helmet : ",font=("Ubuntu Mono", 10),bg = 'white').place(x=440, y=550)

        label5 = tk.Label(self.root, text="Camera 1",font=("Ubuntu Mono", 10),bg = '#87CEFA',relief = tk.RIDGE).place(x=170, y=500)
        label6 = tk.Label(self.root, text="Camera 2",font=("Ubuntu Mono", 10),bg = '#87CEFA',relief = tk.RIDGE).place(x=600, y=500)
        label7 = tk.Label(self.root, text="All Messages",font=("Ubuntu Mono", 10),bg = '#87CEFA',relief = tk.RIDGE).place(x=1030, y=500)

        self.num_with_helmet1 = tk.StringVar()
        label_with_helmet1 = tk.Label(self.root, textvariable=self.num_with_helmet1,font=("Ubuntu Mono", 10),bg = '#90EE90').place(x=230, y=530)

        self.num_without_helmet1 = tk.StringVar()
        label_without_helmet1 = tk.Label(self.root, textvariable=self.num_without_helmet1,font=("Ubuntu Mono", 10),bg = 'red').place(x=260, y=550)

        self.num_with_helmet2 = tk.StringVar()
        label_with_helmet2 = tk.Label(self.root, textvariable=self.num_with_helmet2,font=("Ubuntu Mono", 10),bg = '#90EE90').place(x=660, y=530)

        self.num_without_helmet2 = tk.StringVar()
        label_without_helmet2 = tk.Label(self.root, textvariable=self.num_without_helmet2,font=("Ubuntu Mono", 10),bg = 'red').place(x=690, y=550)

        self.messages1 = tk.Text(self.root,bg='#FFFFE0')
        self.messages1.place(x=10, y=580, width=425, height=180)

        self.messages2 = tk.Text(self.root,bg='#FFFFE0')
        self.messages2.place(x=430, y=580, width=425, height=180)

        self.allmessages = tk.Text(self.root,bg='#FFFFE0')
        self.allmessages.place(x=860, y=540, width=425, height=220)

        img = cv2.imread('./resourse/no_signal.jpg', 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        self.panel1 = tk.Label(image=img)
        self.panel1.image = img
        self.panel1.place(x=20, y=0)
        self.panel1.configure(image=img)
        self.panel1.image = img

        self.panel2 = tk.Label(image=img)
        self.panel2.image = img
        self.panel2.place(x=680, y=0)
        self.panel2.configure(image=img)
        self.panel2.image = img
        photo = tk.PhotoImage(file='./resourse/btn2.png')
        
        quit_btn = tk.Button(self.root, image=photo,borderwidth=0,overrelief='sunken',command=self.root.quit)
        quit_btn.place(x=620, y=760)
        

        self.root.mainloop()

    def callback(self):
        self.root.quit()

    def quit(self):
        # self.stop_event.set()
        self.root.destroy()

    def update(self, images, values, messages):
        img = cv2.cvtColor(images[0], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        self.panel1.configure(image=img)
        self.panel1.image = img


        self.num_with_helmet1.set(values[0])
        self.num_without_helmet1.set(values[1])
        message = messages[0]
        if message != "":
            self.messages1.insert(tk.INSERT, message)
            self.allmessages.insert(tk.INSERT, "Cam 1: " + message)

        if len(images)>1:
            img = cv2.cvtColor(images[1], cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            self.panel2.configure(image=img)
            self.panel2.image = img

            self.num_with_helmet2.set(values[2])
            self.num_without_helmet2.set(values[3])

            message = messages[1]
            if message != "":
                self.messages2.insert(tk.INSERT, message)
                self.allmessages.insert(tk.INSERT, "Cam 2: " + message)

