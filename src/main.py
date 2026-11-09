from tkinter import messagebox

from forms import odeslat
from screen import nacist_kalibrace


def main():
    kalibrace = nacist_kalibrace()
    if not kalibrace:
        return
    chyby = odeslat(kalibrace)
    if chyby:
        messagebox.showerror("Chyba při odesílání", "\n".join(chyby))
    else:
        messagebox.showinfo("Hotovo", f"Odesláno kalibrací: {len(kalibrace)}")


if __name__ == "__main__":
    main()
