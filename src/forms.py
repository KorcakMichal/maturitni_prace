import os
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import Page, Playwright, expect, sync_playwright

from schemas import Kalibrace

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
STORAGE_STATE = str(ROOT / os.environ.get("STORAGE_STATE", "auth/skola.storage.json"))
FORM_URL = os.environ["FORM_URL"]  # odkaz na formulář je v .env


def cislo(v):
    return f"{v:.1f}".replace(".", ",")


def vyplnit(page: Page, k: Kalibrace):
    textboxy = [
        ("Title Required Field, empty,", k.id),
        ("ItemCode, empty, field editor.", k.meridlo.idi),
        ("Campaign, empty, field editor.", k.campaign),
        ("ConditionsTemp, empty, field", cislo(k.condition_temp)),
        ("ConditionsHum, empty, field", cislo(k.condition_hum)),
        ("Supplier, empty, field editor.", k.supplier),
        ("V01, empty, field editor.", cislo(k.meridlo.v01)),
        ("V02, empty, field editor.", cislo(k.meridlo.v02)),
        ("V03, empty, field editor.", cislo(k.meridlo.v03)),
        ("V04, empty, field editor.", cislo(k.meridlo.v04)),
        ("InspectionNote, empty, field", k.inspection_note),
    ]
    for label, hodnota in textboxy:
        page.get_by_role("textbox", name=label).fill(hodnota)

    # speciální pole
    page.get_by_role("combobox", name="ActionDate, Tab to navigate").fill(
        k.date.strftime("%d.%m.%Y")
    )
    page.get_by_role("combobox", name="selectInspectionLocation,").click()
    page.get_by_text(k.inspection_location).click()


def odeslat_kalibrace(playwright: Playwright, kalibrace: list[Kalibrace]) -> list[str]:
    """Odešle každou kalibraci do Forms, vrátí seznam chyb (prázdný = vše OK)."""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state=STORAGE_STATE)
    chyby = []
    try:
        for k in kalibrace:
            page = context.new_page()
            try:
                page.goto(FORM_URL)
                vyplnit(page, k)
                page.get_by_role("button", name="Submit").click()
                expect(page.get_by_text("Thank you")).to_be_visible(timeout=15_000)
            except Exception as e:
                chyby.append(f"{k.meridlo.idi}: {e}")
            finally:
                page.close()
        context.storage_state(path=STORAGE_STATE)
    finally:
        context.close()
        browser.close()
    return chyby


def odeslat(kalibrace: list[Kalibrace]) -> list[str]:
    with sync_playwright() as playwright:
        return odeslat_kalibrace(playwright, kalibrace)
