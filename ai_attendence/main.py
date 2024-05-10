import os
import subprocess
import tkinter as tk
import cv2
import datetime
from PIL import Image, ImageTk
import util


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        # 1200x520 is Length x Breadth and x = 180 and y = 100 are coordinates
        self.main_window.geometry("1200x520+180+100")

        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register New user','gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        # Database for known people
        self.db_dir = './db'
        # If the folder already exists, don't create a new one
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'capture' not in self.__dict__:
            # noinspection PyArgumentList
            self.capture = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        # Capture the frame
        ret, frame = self.capture.read()
        self.most_recent_capture_arr = frame

        # Convert the format from OpenCV format to Pillow format
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        # Put the frame in the label after conversion
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        # Repeat the same process every 20ms
        self._label.after(10, self.process_webcam)

    def login(self):
        unknown_img_path = './.temp.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        # print(output)
        # Get the name from the output
        name = output.split(',')[1][:]
        # print(name)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oops!', 'Unknown user. Please register new user or try again.')
        else:
            util.msg_box('Welcome back!', f'Welcome, {name}')
            with open(self.log_path, 'a') as f:
                f.write(f'{name}\t\t{datetime.datetime.now()}\n')

        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+200+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        # Label for entering name
        self.name_text_label_register_new_user = util.get_text_label(self.register_new_user_window, "Enter your name:")
        self.name_text_label_register_new_user.place(x=750, y=0)

        # TextBox or Entry for new name
        self.name_entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.name_entry_text_register_new_user.place(x=750, y=40)

        # Label for entering rno
        self.rno_text_label_register_new_user = util.get_text_label(self.register_new_user_window,
                                                                    "Enter your roll number:")
        self.rno_text_label_register_new_user.place(x=750, y=140)

        # TextBox or Entry for new rno
        self.rno_entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.rno_entry_text_register_new_user.place(x=750, y=180)

    def try_again_register_new_user(self):
        # Will go back to the main window
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        # Get the text given by the user
        name = self.name_entry_text_register_new_user.get(1.0, "end-1c")
        rno = self.rno_entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, f'{name},{rno}.jpg'), self.register_new_user_capture)

        # Success message box
        util.msg_box('Success', 'User was registered successfully!')

        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()