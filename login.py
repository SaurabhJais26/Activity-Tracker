from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import trackerWindow

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('900x450')
        self.root.configure(bg='#fff')

        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'login.png')
        image = Image.open(img_path)
        self.img = ImageTk.PhotoImage(image)

        Label(self.root, image=self.img, bg='white').place(x=50, y=50)

        frame = Frame(self.root, width=350, height=350, bg='white')
        frame.place(x=480, y=70)

        heading = Label(frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        def on_enter(e):
            self.user.delete(0, 'end')

        def on_leave(e):
            name = self.user.get()
            if name == '':
                self.user.insert(0, 'Username')

        self.username_var = StringVar() # Variable to store the username
        self.user = Entry(frame, textvariable=self.username_var, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        self.user.place(x=30, y=80)
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', on_enter)
        self.user.bind('<FocusOut>', on_leave)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        def on_enter(e):
            self.code.delete(0, 'end')

        def on_leave(e):
            name = self.code.get()
            if name == '':
                self.code.insert(0, 'Password')

        self.code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        self.code.place(x=30, y=150)
        self.code.insert(0, 'Password')
        self.code.bind('<FocusIn>', on_enter)
        self.code.bind('<FocusOut>', on_leave)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

        Button(frame, width=39, pady=7, text='Sign In', bg='#57a1f8', fg='white', border=0, command=self.signin).place(x=35, y=204)

        self.label = Label(frame, text='')

    def open_tracker_window(self):
        self.tracker_window = Toplevel(self.root)
        app = trackerWindow.ActivityTrackerApp(self.tracker_window, self.username_var.get())
        self.tracker_window.protocol("WM_DELETE_WINDOW", self.on_tracker_window_close)
        self.root.withdraw()

    def on_tracker_window_close(self):
        self.tracker_window.destroy()
        self.root.deiconify()  # Show the main window when the tracker window is closed

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
