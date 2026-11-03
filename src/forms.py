from schemas import Kalibrace, Meridlo
from playwright.sync_api import Playwright, sync_playwright, expect

k = Kalibrace(
    id="ACT...",
    meridlo=Meridlo(idi="KCZM01234"),
    date="2026-10-17",
    campaign="2026-10",
    inspection_note="note",
    condition_temp=25,
    condition_hum=50,
    v01=25.0,
    v02=25.1,
    v03=50.0,
    v04=50.1,
)

def cislo(v):
    return f"{v:.1f}".replace(".", ",")


def vyplnit(page, k : Kalibrace):
    textboxy = [
        ("Title Required Field, empty,", k.id),
        ("ItemCode, empty, field editor.", k.meridlo.idi),
        ("Campaign, empty, field editor.", k.campaign),
        ("ConditionsTemp, empty, field", str(k.condition_temp)),
        ("ConditionsHum, empty, field", str(k.condition_hum)),
        ("Supplier, empty, field editor.", k.supplier),
        ("V01, empty, field editor.", cislo(k.v01)),
        ("V02, empty, field editor.", cislo(k.v02)),
        ("V03, empty, field editor.", cislo(k.v03)),
        ("V04, empty, field editor.", cislo(k.v04)),
        ("InspectionNote, empty, field", k.inspection_note),
    ]
    for label, hodnota in textboxy:
        page.get_by_role("textbox", name=label).fill(hodnota)

    # speciální pole
    page.get_by_role("combobox", name="ActionDate, Tab to navigate").fill(
        k.date.strftime("%d.%m.%Y")
    )
    page.pause()
    page.get_by_role("combobox", name="selectInspectionLocation,").fill(k.inspection_location)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="auth/skola.storage.json")
    page = context.new_page()
    page.goto("https://gymjs.sharepoint.com/:l:/s/MaturitnprceMK/JADu45yM7DL5T7lG9_uoAoVXAbfrg6-vmHY70uk7M30Xq44?nav=YmQ1ZTNhZTgtZWM4My00OTY2LTk5M2UtNWU1ZjYyYTQzNGM4")
    
    vyplnit(page, k)

    page.pause()

    page.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("Thank you")).to_be_visible(timeout=15_000)
    # ---------------------
    context.storage_state(path="auth/skola.storage.json")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
