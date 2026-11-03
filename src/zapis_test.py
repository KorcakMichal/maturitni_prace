import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth/skola.storage.json")
    page = context.new_page()
    page.goto("https://gymjs.sharepoint.com/:l:/s/MaturitnprceMK/JADu45yM7DL5T7lG9_uoAoVXAbfrg6-vmHY70uk7M30Xq44?nav=YmQ1ZTNhZTgtZWM4My00OTY2LTk5M2UtNWU1ZjYyYTQzNGM4")
    page.get_by_role("textbox", name="Title Required Field, empty,").click()
    page.get_by_role("textbox", name="Title Required Field, empty,").fill("ACT...")
    page.get_by_role("textbox", name="ItemCode, empty, field editor.").click()
    page.get_by_role("textbox", name="ItemCode, empty, field editor.").fill("KCZM...testicek")
    page.get_by_role("combobox", name="ActionDate, Tab to navigate").click()
    page.get_by_role("combobox", name="ActionDate, Tab to navigate").fill("17.10.2026")
    page.get_by_role("combobox", name="ActionDate, Tab to navigate").press("Enter")
    page.get_by_role("textbox", name="Campaign, empty, field editor.").click()
    page.get_by_role("textbox", name="Campaign, empty, field editor.").fill("2026-10")
    page.get_by_role("combobox", name="selectInspectionLocation,").click()
    page.get_by_text("on site").click()
    page.get_by_role("textbox", name="ConditionsTemp, empty, field").click()
    page.get_by_role("textbox", name="ConditionsTemp, empty, field").fill("25")
    page.get_by_role("textbox", name="ConditionsHum, empty, field").click()
    page.get_by_role("textbox", name="ConditionsHum, empty, field").fill("50")
    page.get_by_role("textbox", name="Supplier, empty, field editor.").click()
    page.get_by_role("textbox", name="Supplier, empty, field editor.").fill("KCZ")
    page.get_by_role("textbox", name="V01, empty, field editor.").click()
    page.get_by_role("textbox", name="V01, empty, field editor.").fill("25,0")
    page.get_by_role("textbox", name="V02, empty, field editor.").click()
    page.get_by_role("textbox", name="V02, empty, field editor.").fill("25,1")
    page.get_by_role("textbox", name="V03, empty, field editor.").click()
    page.get_by_role("textbox", name="V03, empty, field editor.").fill("50,0")
    page.get_by_role("textbox", name="V04, empty, field editor.").click()
    page.get_by_role("textbox", name="V04, empty, field editor.").fill("50,1")
    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Thank you")).to_be_visible(timeout=15_000)

    # ---------------------
    context.storage_state(path="auth/skola.storage.json")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
