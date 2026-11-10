# Uživatelská dokumentace

## K čemu aplikace slouží

Zadáte údaje o kalibraci, načtete čtečkou kódy měřidel, doplníte naměřené hodnoty a stisknete **Odeslat**. Aplikace sama otevře prohlížeč a pro každé měřidlo vyplní a odešle Microsoft Forms. Nahrazuje ruční vyplňování formuláře.

## Požadavky

- Windows, macOS nebo Linux
- [uv](https://docs.astral.sh/uv/) (správce Python prostředí; Python 3.14 si stáhne sám)
- Účet s přístupem k formuláři Microsoft Forms
- Čtečka čárových/QR kódů, která se chová jako klávesnice (nepovinné, kódy lze psát ručně)

## Instalace

```powershell
git clone <adresa repozitáře>
cd maturitni_prace
uv sync
uv run playwright install chromium
```

### Konfigurace

Zkopírujte `.env.example` na `.env` a upravte:

```
FORM_URL=https://<tenant>.sharepoint.com/:l:/s/<site>/<id>?nav=<nav>
STORAGE_STATE=auth/skola.storage.json
```

- `FORM_URL` – odkaz na formulář, do kterého se odesílá.
- `STORAGE_STATE` – soubor s uloženým přihlášením (cookies). Není v gitu.

### Jednorázové přihlášení

Aplikace se do Microsoft 365 nepřihlašuje sama, používá uložené přihlášení. Vytvoříte ho jednou:

```powershell
uv run playwright codegen --save-storage=auth/skola.storage.json <FORM_URL>
```

V otevřeném prohlížeči se přihlaste a okno zavřete. Soubor s přihlášením nikomu nepředávejte, dává přístup k vašemu účtu.

## Spuštění

```powershell
uv run python src/main.py
```

Otevřou se dvě okna.

## Ovládání

### Okno „Kalibrace" – společné údaje

| Pole | Význam | Výchozí |
|---|---|---|
| `id` | Označení kalibrace | – |
| `date` | Datum kalibrace (`RRRR-MM-DD`) | dnešek |
| `campaign` | Kampaň ve tvaru `RRRR-MM` | aktuální měsíc |
| `inspection_location` | Místo kontroly | `on site` |
| `inspection_note` | Poznámka | – |
| `supplier` | Dodavatel | `KCZ` |
| `condition_temp` | Teplota při kalibraci (°C) | – |
| `condition_hum` | Vlhkost při kalibraci (0–100 %) | – |

Desetinná čísla lze psát s čárkou i tečkou.

### Okno „Měřidla" – tabulka

Jeden řádek = jedno měřidlo.

| Sloupec | Význam |
|---|---|
| `idi` | Kód měřidla, tvar `KCZM` + 5 číslic (např. `KCZM06088`) |
| `v01` | Naměřená teplota – etalon (TE) |
| `v02` | Naměřená teplota – kalibrované měřidlo (TK) |
| `v03` | Vlhkost – etalon (HE), 0–100 |
| `v04` | Vlhkost – kalibrované měřidlo (HK), 0–100 |

Tlačítka:
- **Načíst čtečkou** – otevře okno, ve kterém naskenujete kódy ze štítků měřidel (viz fotografie v [README](README.md)). Každý platný kód se zapíše do prvního volného řádku. Neplatný nebo již načtený kód se zahlásí červeně a pípnutím.
- **Přidat řádek** – další řádek tabulky.
- **Odeslat** – zvaliduje data a odešle je.

V tabulce přeskakuje **Enter** na další pole a na konci řádku na nový řádek. Prázdné řádky se ignorují.

### Typický postup

1. Zkontrolujte společné údaje (okno „Kalibrace").
2. V okně „Měřidla" klikněte na **Načíst čtečkou** a naskenujte všechna měřidla, pak **Hotovo**.
3. Do tabulky doplňte hodnoty `v01`–`v04`.
4. Klikněte na **Odeslat**.
5. Otevře se prohlížeč a postupně odešle formulář za každé měřidlo. Nezasahujte do něj.
6. Zobrazí se hlášení **Hotovo – Odesláno kalibrací: N**, nebo **Chyba při odesílání** se seznamem měřidel, která se nepodařila.

## Jak poznám, že to funguje

1. Po stisku **Odeslat** s chybným vstupem (např. kód `ABC`, vlhkost 150) se zobrazí okno **Chyba** s popisem řádku a pole. Nic se neodešle.
2. Se správným vstupem se otevře prohlížeč, formulář se sám vyplní a odešle a zobrazí se hláška **Hotovo**.
3. Záznam se objeví v SharePoint seznamu `TableAction` (vytvoří ho stávající Power Automate flow z odpovědí Forms).

## Řešení problémů

| Problém | Příčina / řešení |
|---|---|
| `KeyError: 'FORM_URL'` | Chybí soubor `.env` nebo v něm `FORM_URL`. |
| Prohlížeč ukáže přihlašovací stránku | Vypršelo uložené přihlášení, proveďte znovu jednorázové přihlášení. |
| Chyba `Timeout` / `locator` u měřidla | Formulář se změnil nebo se nenačetl. Zkuste znovu, případně viz [programátorská dokumentace](programatorska.md#závislost-na-formuláři). |
| `Executable doesn't exist` | Chybí prohlížeč: `uv run playwright install chromium`. |
