from tkinter import messagebox

from CTkMessagebox import CTkMessagebox


def show_confirm(msg):
    return messagebox.askyesno("Confirm", msg)


def show_error(msg):
    CTkMessagebox(title="Error", message=msg, icon="cancel")


def show_info(msg):
    CTkMessagebox(title="Info", message=msg, icon="info")


def show_warning(msg):
    CTkMessagebox(title="Warning", message=msg, icon="warning")


def show_info_v2(msg):
    messagebox.showinfo("Info", msg)


def show_warning_v2(msg):
    messagebox.showwarning("Warning", msg)
