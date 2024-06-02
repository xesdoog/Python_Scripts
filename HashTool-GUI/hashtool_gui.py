import customtkinter
import hashlib
import itertools
import multiprocessing
import os
import string
import threading
import time
from PIL import Image
from threading import Thread

CRACK_BUTTON_STATE = "normal"
CRACK_BUTTON_LABEL = "Crack"
RESULT_TEXT        = "Ready"
HASH               = str
HASH_TYPE          = str
CHARSET            = str
PASS_LENGTH        = int
PROGRESS_INTER     = int

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
class App(customtkinter.CTk):
    ALPHA_LOWER                     = ''.join((string.ascii_lowercase,))
    ALPHA_UPPER                     = ''.join((string.ascii_uppercase,))
    ALPHA_MIXED                     = ''.join((string.ascii_lowercase, string.ascii_uppercase))
    PUNCTUATION                     = ''.join((string.punctuation,))
    NUMERIC                         = ''.join((''.join(map(str, range(0, 10))),))
    ALPHA_LOWER_NUMERIC             = ''.join((string.ascii_lowercase, ''.join(map(str, range(0, 10)))))
    ALPHA_UPPER_NUMERIC             = ''.join((string.ascii_uppercase, ''.join(map(str, range(0, 10)))))
    ALPHA_MIXED_NUMERIC             = ''.join((string.ascii_lowercase, string.ascii_uppercase, ''.join(map(str, range(0, 10)))))
    ALPHA_LOWER_PUNCTUATION         = ''.join((string.ascii_lowercase, string.punctuation))
    ALPHA_UPPER_PUNCTUATION         = ''.join((string.ascii_uppercase, string.punctuation))
    ALPHA_MIXED_PUNCTUATION         = ''.join((string.ascii_lowercase, string.ascii_uppercase, string.punctuation))
    NUMERIC_PUNCTUATION             = ''.join((''.join(map(str, range(0, 10))), string.punctuation))
    ALPHA_LOWER_NUMERIC_PUNCTUATION = ''.join((string.ascii_lowercase, ''.join(map(str, range(0, 10))), string.punctuation))
    ALPHA_UPPER_NUMERIC_PUNCTUATION = ''.join((string.ascii_uppercase, ''.join(map(str, range(0, 10))), string.punctuation))
    ALPHA_MIXED_NUMERIC_PUNCTUATION = ''.join((string.ascii_lowercase, string.ascii_uppercase, ''.join(map(str, range(0, 10))), string.punctuation))
    def __init__(self, HASH_TYPE, HASH, CHARSET, progress_interval):
        self.__charset = CHARSET
        self.__curr_iter = 0
        self.__prev_iter = 0
        self.__curr_val = ""
        self.__progress_interval = PROGRESS_INTER
        self.__hash_type = HASH_TYPE
        self.__hash = HASH
        self.__hashers = {}
        super().__init__()

        # configure window
        self.title("SAMURAI's HashTool")
        self.geometry(f"{600}x{400}")
        self.resizable(False, False)
        self.wm_iconbitmap("SamuraisHashTool.ico")
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure((2, 3), weight = 0)
        self.grid_rowconfigure((0, 1, 2), weight = 1)
        # create sidebar frame with widgets
        self.logo_image = customtkinter.CTkImage(Image.open("SamuraisHashTool.ico"), size = (26, 26))
        self.sidebar_frame = customtkinter.CTkFrame(self, width = 140, corner_radius = 0)
        self.sidebar_frame.grid(row = 0, column = 0, rowspan = 4, sticky = "nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight = 1)
        # self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text = " SAMURAI's\nHashTool", image = self.logo_image, compound = "left", 
        #                                          font = customtkinter.CTkFont(size = 20, weight = "bold"))
        # self.logo_label.grid(row = 0, column = 0, padx = 20, pady = (20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text = "Theme:", anchor = "w")
        self.appearance_mode_label.grid(row = 5, column = 0, padx = 20, pady = (10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values = ["Light", "Dark", "System"],
                                                                       command = self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row = 6, column = 0, padx = 20, pady = (10, 10))
        self.appearance_mode_optionemenu.set("Dark")

        # create main entry
        self.hash_type_text = customtkinter.CTkLabel(self, text = "Select Hash Type:", anchor = "w")
        self.hash_type_text.grid(row = 0, column = 1, padx = 20, pady = (10, 0))
        self.hash_type = customtkinter.CTkOptionMenu(self, values = ["MD5", "MD4", "LM", "NTLM", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"],
                                                     command = self.set_hash_type)
        self.hash_type.grid(row = 1, column = 1, padx = 20, pady = (10, 10))
        self.charset_text = customtkinter.CTkLabel(self, text = "Select Charset:", anchor = "w")
        self.charset_text.grid(row = 0, column = 2, padx = 20, pady = (10, 0))
        self.charset = customtkinter.CTkOptionMenu(self, values = [App.ALPHA_LOWER, App.ALPHA_UPPER, App.ALPHA_MIXED, App.NUMERIC, App.ALPHA_LOWER_NUMERIC, App.ALPHA_UPPER_NUMERIC, App.ALPHA_MIXED_NUMERIC, App.PUNCTUATION, App.ALPHA_LOWER_PUNCTUATION, App.ALPHA_UPPER_PUNCTUATION, App.ALPHA_MIXED_PUNCTUATION, App.NUMERIC_PUNCTUATION, App.ALPHA_LOWER_NUMERIC_PUNCTUATION, App.ALPHA_UPPER_NUMERIC_PUNCTUATION, App.ALPHA_MIXED_NUMERIC_PUNCTUATION],
                                                     command = self.set_charset)
        self.charset.grid(row = 1, column = 2, padx = 20, pady = (10, 10))
        self.pass_length = customtkinter.CTkEntry(self, placeholder_text = "Password Length")
        self.pass_length.grid(row = 2, column = 1, columnspan = 1, padx = (20, 20), pady = (50, 50), sticky = "nsew")
        self.length_button = customtkinter.CTkButton(self, text = "Confirm", 
                                                     command = self.set_length)
        self.length_button.grid(row = 2, column = 2, columnspan = 1, padx = 1, pady = (1, 1))
        self.hash = customtkinter.CTkEntry(self, placeholder_text = "Enter Password Hash")
        self.hash.grid(row = 3, column = 1, columnspan = 3, padx = (20, 20), pady = (30, 30), sticky = "nsew")
        self.crack_button = customtkinter.CTkButton(self, text = CRACK_BUTTON_LABEL, state = CRACK_BUTTON_STATE,
                                                    command = self.start_cracking)
        self.crack_button.grid(row = 4, column = 1, columnspan = 1, padx = 10, pady = (10, 10))
        self.crack_result_text = customtkinter.CTkLabel(self, text = RESULT_TEXT, anchor = "w", font = customtkinter.CTkFont(size = 12))
        self.crack_result_text.grid(row = 5, column = 1, padx = 10, pady = (10, 0))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def __init_hasher(self):
        hashlib_type = self.__hash_type if self.__hash_type != "ntlm" else "md4"
        self.__hashers[self.__hash_type] = hashlib.new(hashlib_type)

    def __encode_utf8(self, data):
        return data.encode("utf-8")

    def __encode_utf16le(self, data):
        return data.encode("utf-16le")
    
    @staticmethod
    def __search_space(charset, maxlength):
        return (
            ''.join(candidate) for candidate in
            itertools.chain.from_iterable(
                itertools.product(charset, repeat=i) for i in
                range(1, maxlength + 1)
            )
        )
    
    def __attack(self, q, max_length):
        self.__init_hasher()
        self.start_reporting_progress()
        hash_fn = self.__encode_utf8 if self.__hash_type != "ntlm" else self.__encode_utf16le
        for value in self.__search_space(self.__charset, max_length):
            hasher = self.__hashers[self.__hash_type].copy()
            self.__curr_iter += 1
            self.__curr_val = value
            hasher.update(hash_fn(value))
            if self.__hash == hasher.hexdigest():
                q.put("FOUND")
                q.put("{}Match found! Password is {}{}".format(
                    os.linesep, value, os.linesep))
                self.stop_reporting_progress()
                return

        q.put("NOT FOUND")
        self.stop_reporting_progress()

    @staticmethod
    def work(work_q, done_q, max_length):
        obj = work_q.get()
        obj.__attack(done_q, max_length)

    def start_reporting_progress(self):
        self.__progress_timer = threading.Timer(
            self.__progress_interval, self.start_reporting_progress)
        self.__progress_timer.start()
        global RESULT_TEXT
        RESULT_TEXT = f"Character set: {self.__charset}, iteration: {self.__curr_iter}, trying: {self.__curr_val}, hashes/sec: {self.__curr_iter - self.__prev_iter}"
        self.__prev_iter = self.__curr_iter

    def stop_reporting_progress(self):
        global RESULT_TEXT
        self.__progress_timer.cancel()
        RESULT_TEXT = f"Finished character set {self.__charset} after {self.__curr_iter} iterations"
    
    def set_hash_type(self, hash_type: str):
        global HASH_TYPE
        HASH_TYPE = hash_type
    
    def set_charset(self, charset: str):
        global CHARSET
        CHARSET = charset

    def set_length(self):
        global PASS_LENGTH
        length = f"{self.pass_length.get()}"
        PASS_LENGTH = length

    def start_cracking(self):
        global RESULT_TEXT
        HASH = f"{self.hash.get()}"
        RESULT_TEXT = f"Trying to crack hash {HASH}"
        processes = []
        work_queue = multiprocessing.Queue()
        done_queue = multiprocessing.Queue()
        progress_interval = 3
        cracker = App(HASH_TYPE.lower(), HASH.lower(),
                        ''.join(CHARSET), progress_interval)
        start_time = time.time()
        p = multiprocessing.Process(target=App.work, args=(work_queue, done_queue, PASS_LENGTH))
        processes.append(p)
        work_queue.put(cracker)
        p.start()

        if len(CHARSET) > 1:
            for i in range(len(CHARSET)):
                progress_interval += .2
                cracker = App(HASH_TYPE.lower(), HASH.lower(),
                                CHARSET[i], progress_interval)
                p = multiprocessing.Process(target=App.work, args=(work_queue, done_queue, PASS_LENGTH))
                processes.append(p)
                work_queue.put(cracker)
                p.start()

        failures = 0
        while True:
            data = done_queue.get()
            if data == "NOT FOUND":
                failures += 1
            elif data == "FOUND":
                RESULT_TEXT = done_queue.get()
                for p in processes:
                    p.terminate()
                break

            if failures == len(processes):
                RESULT_TEXT = "No matches found!"
                break

        RESULT_TEXT = "Took {} seconds".format(time.time() - start_time)

if __name__ == "__main__":
    app = App(HASH, HASH_TYPE, CHARSET, PROGRESS_INTER)
    app.mainloop()