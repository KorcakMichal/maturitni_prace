# Programátorská dokumentace

## Přehled architektury

```
main.py ──► screen.py ──► schemas.py
   │         (Tkinter UI)   (Pydantic modely)
   └──────► forms.py ─────► schemas.py
            (Playwright)
```

Tok dat: UI → text z políček → `sestavit()` → ověřené objekty `Kalibrace` → `odeslat()` → Microsoft Forms → (stávající flow) → SharePoint `TableAction`.

Širší kontext procesu: [BPMN před](img/proces-before.svg) a [entity](img/entity.svg), podrobně v [analyza/](../analyza).

## Technologie

- Python ≥ 3.14, správa závislostí přes `uv` (`pyproject.toml`, `uv.lock`)
- **Pydantic 2** – model a validace vstupu
- **Playwright (sync API)** – ovládání Chromia
- **Tkinter** – UI (součást Pythonu)
- **python-dotenv** – konfigurace z `.env`

## Moduly (`src/`)

### `schemas.py` – datový model

- `Meridlo`: `idi` (regex `^KCZM\d{5}$`), `v01`–`v04` (teploty bez omezení, vlhkosti 0–100).
- `Kalibrace`: `id`, `meridlo`, `date`, `campaign` (`^\d{4}-\d{2}$`), `inspection_location` (výchozí `on site`), `inspection_note`, `supplier` (výchozí `KCZ`), `condition_temp`, `condition_hum` (0–100).

Jediný zdroj pravdy o polích a pravidlech. Zbytek kódu z něj vychází.

### `screen.py` – UI

- `POLE_KALIBRACE`, `SLOUPCE_MERIDLA` se odvozují z `model_fields`, takže přidání pole do modelu přidá pole i do UI. `KOD_MERIDLA` je regex převzatý z metadat pole `idi` (čtečka tedy validuje stejným pravidlem jako model).
- `sestavit(spolecne, radky)` – čistá funkce bez UI: převede desetinné čárky na tečky, přeskočí prázdné řádky, každý řádek zvaliduje přes `Kalibrace.model_validate` a vrátí `(kalibrace, chyby)`. Chyby se sbírají pro všechny řádky najednou, aby uživatel opravil vše v jednom kole.
- `nacist_kalibrace()` – vytvoří okna a vrátí seznam `Kalibrace` nebo `None` (okno zavřeno / nic k odeslání). Vnořené funkce:
  - `pridat_radek`, `dalsi` – správa řádků a navigace Enterem,
  - `nacist_ctekou` – modální okno pro čtečku,
  - `odeslat` – sestaví a zvaliduje, při chybě ukáže `messagebox`, jinak zavře UI.

**Neobvyklé rozhodnutí – čtečka jako klávesnice.** Čtečka za kódem posílá Tab (některé Enter). Okno čtečky proto váže obě klávesy na `prijmout` a vrací `"break"`, aby Tab nepřeskočil fokus. Čtečka tak nepotřebuje žádný ovladač.

### `forms.py` – odeslání do Forms

- `vyplnit(page, k)` – vyplní textová pole podle seznamu `(popisek, hodnota)`, pak datum (`combobox`, formát `dd.mm.rrrr`) a místo kontroly (výběr z nabídky).
- `odeslat_kalibrace(playwright, kalibrace)` – spustí Chromium (`headless=False`, aby uživatel viděl průběh), vytvoří kontext z `STORAGE_STATE`, pro každé měřidlo otevře novou stránku, vyplní, odešle a čeká na text „Thank you" (15 s). Výjimka u jednoho měřidla se uloží do seznamu chyb a pokračuje se dalším. Na konci se stav (cookies) uloží zpět, aby přihlášení vydrželo.
- `odeslat(kalibrace)` – obálka kolem `sync_playwright()`.
- `cislo(v)` – formát čísla s jedním desetinným místem a čárkou (`23,5`), jak ho formulář očekává.

### `main.py`

Propojí obě části a ukáže výsledek v `messagebox`. Importy jsou bez balíčku (`from forms import ...`), proto se spouští z kořene jako `python src/main.py`.

## Závislost na formuláři

Pole formuláře se hledají podle přístupnostních názvů, např. `ItemCode, empty, field editor.`, `ConditionsTemp, empty, field`. Názvy jsou useknuté, protože Playwright hledá podle podřetězce. Při změně formuláře (přejmenování otázky, jiný jazyk) je třeba upravit seznam `textboxy` a názvy `combobox`ů ve `vyplnit`. Tyto názvy lze zjistit pomocí `uv run playwright codegen <FORM_URL>`.

Mapování polí modelu na pole formuláře:

| Model | Pole ve Forms |
|---|---|
| `id` | `Title` |
| `meridlo.idi` | `ItemCode` |
| `campaign` | `Campaign` |
| `condition_temp` / `condition_hum` | `ConditionsTemp` / `ConditionsHum` |
| `supplier` | `Supplier` |
| `meridlo.v01`–`v04` | `V01`–`V04` |
| `inspection_note` | `InspectionNote` |
| `date` | `ActionDate` |
| `inspection_location` | `selectInspectionLocation` |

## Bezpečnost

- `.env` a `auth/` (uložené cookies) jsou v `.gitignore` a nesmí se commitovat. Uložený stav prohlížeče dává přístup k účtu.
- Aplikace neukládá hesla.

## Rozšíření a další kroky

- Přidat pole: upravit `schemas.py` (UI se přizpůsobí), pak přidat odpovídající řádek do `forms.py`.
- Testování bez zásahu do ostrých dat: nastavit `FORM_URL` na testovací formulář (např. na školním SharePointu).
- Neřešeno: automatické testy (`sestavit()` je čistá funkce a jde testovat hned), paralelní odesílání, headless režim.
- Uvažovaný další krok ze zadání: nahradit i ruční zadání hodnot do `TableAction` a navázat na Excel s kalibračním listem.
