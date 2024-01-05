from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import trackerWindow

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('1200x600')
        self.root.minsize(900, 600)  # Set a minimum width
        self.root.configure(bg='#fff')

        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login.png')
        image = Image.open(img_path)
        image = image.resize((400, 400), resample=Image.BICUBIC)
        self.img = ImageTk.PhotoImage(image)

        container = Frame(self.root, bg='white')
        container.pack(expand=True, fill='both', padx=5, pady=10)

        frame = Frame(container, bg='white')
        frame.pack(side=RIGHT, padx=(40, 120))

        Label(container, image=self.img, bg='white').pack(side=LEFT, pady=(20, 0), padx=(80, 0))

        heading = Label(frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 30, 'bold'))
        heading.grid(row=0, column=0, pady=(10, 50), sticky='w')

        def on_enter(e):
            self.user.delete(0, 'end')

        def on_leave(e):
            name = self.user.get()
            if name == '':
                self.user.insert(0, 'Username')

        self.username_var = StringVar() 
        self.user = Entry(frame, textvariable=self.username_var, width=20, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 12))
        self.user.grid(row=1, column=0, pady=(0, 15), sticky='w')  # Increased pady
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', on_enter)
        self.user.bind('<FocusOut>', on_leave)

        Frame(frame, width=300, height=2, bg='black').grid(row=2, column=0, pady=(0, 20), sticky='w')

        def on_enter(e):
            self.code.delete(0, 'end')

        def on_leave(e):
            name = self.code.get()
            if name == '':
                self.code.insert(0, 'Password')

        self.code = Entry(frame, width=20, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 12))
        self.code.grid(row=3, column=0, pady=(0, 10), sticky='w')  
        self.code.insert(0, 'Password')
        self.code.bind('<FocusIn>', on_enter)
        self.code.bind('<FocusOut>', on_leave)

        Frame(frame, width=300, height=2, bg='black').grid(row=4, column=0, pady=(0, 40), sticky='w')  

        Button(frame, width=20, pady=7,text='Sign In', bg='#57a1f8', fg='white', border=0, font=('Microsoft YaHei UI Light', 14), command=self.signin).grid(row=5, column=0, pady=(0, 40), sticky='w')

        self.label = Label(frame, text='')

    def open_tracker_window(self):
        self.tracker_window = Toplevel(self.root)
        app = trackerWindow.ActivityTrackerApp(self.tracker_window, self.username_var.get())
        self.tracker_window.protocol("WM_DELETE_WINDOW", self.on_tracker_window_close)
        self.root.withdraw()

    def on_tracker_window_close(self):
        self.tracker_window.destroy()
        self.root.deiconify()

    def signin(self):
        username = self.user.get()
        password = self.code.get()

        if username == 'admin' and password == '1234':
            self.open_tracker_window()
        elif username != 'admin' and password != '1234':
            messagebox.showerror("Invalid", "Invalid username and password")
        elif username != 'admin':
            messagebox.showerror("Invalid", "Invalid username")
        elif password != '1234':
            messagebox.showerror("Invalid", "Invalid password")

if __name__ == "__main__":
    root = Tk()
    app = LoginApp(root)
    root.mainloop()
