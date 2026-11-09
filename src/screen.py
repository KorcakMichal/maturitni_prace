import re
import tkinter as tk
from datetime import date
from tkinter import messagebox

from pydantic import ValidationError
from schemas import Kalibrace, Meridlo

# společná pole kalibrace (bez měřidla, to se zadává v tabulce)
POLE_KALIBRACE = [n for n in Kalibrace.model_fields if n != "meridlo"]
SLOUPCE_MERIDLA = list(Meridlo.model_fields)
CISELNA_POLE = ("condition_temp", "condition_hum")
KOD_MERIDLA = re.compile(Meridlo.model_fields["idi"].metadata[0].pattern)


def sestavit(spolecne, radky):
    """Z hodnot formuláře a řádků tabulky vyrobí seznam Kalibrace a seznam chyb."""
    spolecne = {n: v.replace(",", ".") if n in CISELNA_POLE else v for n, v in spolecne.items()}
    kalibrace, chyby = [], []
    for cislo, radek in enumerate(radky, start=1):
        if not any(radek.values()):
            continue  # prázdný řádek se přeskočí
        try:
            radek = {n: v.replace(",", ".") if n != "idi" else v for n, v in radek.items()}
            kalibrace.append(Kalibrace.model_validate({**spolecne, "meridlo": radek}))
        except ValidationError as e:
            for err in e.errors():
                pole = ".".join(str(p) for p in err["loc"])
                chyby.append(f"Řádek {cislo}: {pole}: {err['msg']}")
    if not kalibrace and not chyby:
        chyby.append("Přidej aspoň jedno měřidlo.")
    return kalibrace, chyby


def nacist_kalibrace():
    """Otevře formulář a tabulku měřidel, vrátí seznam Kalibrace (nebo None)."""
    root = tk.Tk()
    root.title("Kalibrace")

    # --- okno 1: společné údaje ---
    entries = {}
    for row, name in enumerate(POLE_KALIBRACE):
        field = Kalibrace.model_fields[name]
        tk.Label(root, text=name).grid(row=row, column=0, sticky="w", padx=8, pady=2)
        entry = tk.Entry(root, width=30)
        entry.grid(row=row, column=1, padx=8, pady=2)
        if not field.is_required():
            entry.insert(0, str(field.default))
        entries[name] = entry
    entries["date"].insert(0, date.today().isoformat())
    entries["campaign"].insert(0, date.today().strftime("%Y-%m"))

    # --- okno 2: tabulka měřidel ---
    tabulka = tk.Toplevel(root)
    tabulka.title("Měřidla")
    root.update_idletasks()
    tabulka.geometry(f"+{root.winfo_x() + root.winfo_width() + 10}+{root.winfo_y()}")
    tabulka.protocol("WM_DELETE_WINDOW", root.destroy)

    for sloupec, name in enumerate(SLOUPCE_MERIDLA):
        tk.Label(tabulka, text=name, font=("TkDefaultFont", 9, "bold")).grid(
            row=0, column=sloupec, padx=4, pady=4
        )

    radky = []  # každý řádek je slovník {sloupec: Entry}

    def pridat_radek():
        i = len(radky) + 1
        radek = {}
        for sloupec, name in enumerate(SLOUPCE_MERIDLA):
            e = tk.Entry(tabulka, width=14)
            e.grid(row=i, column=sloupec, padx=2, pady=1)
            e.bind("<Return>", lambda _, r=i - 1, c=sloupec: dalsi(r, c))
            radek[name] = e
        radky.append(radek)
        tlacitka.grid(row=i + 1, column=0, columnspan=len(SLOUPCE_MERIDLA), pady=8)
        return radek

    def dalsi(r, c):
        """Enter (čtečka ho posílá za kódem) přeskočí na další pole, na konci řádku na nový řádek."""
        if c + 1 < len(SLOUPCE_MERIDLA):
            radky[r][SLOUPCE_MERIDLA[c + 1]].focus_set()
        else:
            if r + 1 == len(radky):
                pridat_radek()
            radky[r + 1][SLOUPCE_MERIDLA[0]].focus_set()

    vysledek = []

    def odeslat():
        spolecne = {name: e.get().strip() for name, e in entries.items()}
        hodnoty = [{n: e.get().strip() for n, e in radek.items()} for radek in radky]
        kalibrace, chyby = sestavit(spolecne, hodnoty)
        if chyby:
            messagebox.showerror("Chyba", "\n".join(chyby))
            return
        vysledek.extend(kalibrace)
        root.destroy()

    def nacist_ctekou():
        """Okno pro čtečku: přijímá jen kódy měřidel a každý zapíše do prvního volného řádku."""
        okno = tk.Toplevel(tabulka)
        okno.title("Čtečka")
        okno.transient(tabulka)
        tk.Label(okno, text="Naskenuj kódy měřidel (KCZM…)").pack(padx=10, pady=(10, 2))
        entry = tk.Entry(okno, width=24, justify="center")
        entry.pack(padx=10, pady=2)
        stav = tk.Label(okno, text="")
        stav.pack()
        seznam = tk.Listbox(okno, height=8, width=24)
        seznam.pack(padx=10, pady=4)

        def zapsat(kod):
            radek = next((r for r in radky if not r["idi"].get().strip()), None) or pridat_radek()
            radek["idi"].insert(0, kod)

        def prijmout(_=None):
            """Čtečka za kódem posílá Tab (Enter jde také)."""
            kod = entry.get().strip()
            entry.delete(0, "end")
            if not KOD_MERIDLA.match(kod):
                stav.config(text=f"Neplatný kód: {kod}", fg="red")
                okno.bell()
            elif kod in seznam.get(0, "end"):
                stav.config(text=f"Už načteno: {kod}", fg="red")
                okno.bell()
            else:
                zapsat(kod)
                seznam.insert("end", kod)
                stav.config(text=f"OK: {kod}", fg="green")
            return "break"  # Tab nesmí přesunout kurzor z pole

        entry.bind("<Return>", prijmout)
        entry.bind("<Tab>", prijmout)
        tk.Button(okno, text="Hotovo", command=okno.destroy).pack(pady=(2, 10))
        okno.grab_set()
        entry.focus_force()

    tlacitka = tk.Frame(tabulka)
    tk.Button(tlacitka, text="Načíst čtečkou", command=nacist_ctekou).pack(side="left", padx=4)
    tk.Button(tlacitka, text="Přidat řádek", command=pridat_radek).pack(side="left", padx=4)
    tk.Button(tlacitka, text="Odeslat", command=odeslat).pack(side="left", padx=4)

    pridat_radek()["idi"].focus_set()  # kurzor čeká na načtení čtečkou
    root.mainloop()
    return vysledek or None


if __name__ == "__main__":
    print(nacist_kalibrace())
