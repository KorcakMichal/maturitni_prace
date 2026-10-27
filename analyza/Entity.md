# Entity v procesu kalibrace TeHum měřidel

Přehled všech systémů, úložišť, dokumentů a rolí, které se vyskytují v procesu popsaném v [Notes.md](Notes.md) a nakresleném v [before.bpmn](before.bpmn).

> Poznámka: popisy datových seznamů (TableInfra, ListAssessment, ListCompanyInfra) vycházejí z jejich názvů a z toho, jak je používá Excel. Přesné sloupce je potřeba doplnit/ověřit přímo v SharePointu.

## Role (kdo)

| Entita | Co to je |
|---|---|
| **Uživatel (kalibrátor)** | Člověk, který kalibraci fyzicky provede, zapíše ji do Forms, zadá naměřené hodnoty a vygeneruje PDF kalibračního listu. |
| **Pavel Korčák** | Schvalovatel. Kontroluje vygenerovaný PDF list, podepisuje ho digitálním podpisem, tiskne, archivuje a předává zákazníkovi. |
| **Zákazník** | Příjemce vytištěného, podepsaného kalibračního listu. |

## Datové zdroje (SharePoint)

| Entita | Typ | Co obsahuje / k čemu slouží |
|---|---|---|
| **TableAction** | SharePoint seznam | Záznamy o provedených akcích (kalibracích). Vzniká automaticky z Forms (kdy a kdo), kalibrátor do něj ručně doplní naměřené hodnoty. Hlavní zdroj dat pro kalibrační list. Má pohled „Meridla" filtrovaný na typ měřidla (teploměr/vlhkoměr digitální). |
| **TableInfra** (TableInfrastructure) | SharePoint seznam | Evidence infrastruktury, tedy konkrétních přístrojů/měřidel (instancí) s identifikátory typu KCZM03196, KCZM03249 apod. a jejich technickými parametry. |
| **ListAssessment** | SharePoint seznam | Podklady pro vyhodnocení (kritéria, tolerance, postupy), podle kterých se výsledky kalibrace posuzují. |
| **ListCompanyInfra** | SharePoint seznam | Seznam firem/zákazníků a jejich infrastruktury, tj. komu měřidlo patří a komu se list předává. |

Všechny čtyři leží na webu `sites/infrastructure` a Excel je čte přes Power Query.

## Nástroje a automatizace

| Entita | Co to je |
|---|---|
| **Microsoft Forms** | Jednoduchý formulář, kam kalibrátor zadá pouze *kdy* a *kdo* kalibraci provedl. Spouští celý proces. |
| **Power Automate flow** | Automatizace, která po odeslání formuláře přepíše záznam z Forms do TableAction (v diagramu úloha „Flow přepíše záznam"). |
| **Excel pro TeHum měřidla** | Sešit s Power Query, který stahuje data ze čtyř SharePoint seznamů. Kalibrátor v něm vybere etalon a ID z TableAction, sešit sám spočítá hodnoty a vyplní list **Kalibrační list**. |
| **Power Query** | Součást Excelu, která aktualizuje (natahuje) data ze SharePointu. |
| **Etalon** | Referenční (kalibrovaný) přístroj, vůči kterému se zkoušené měřidlo porovnává. Vybírá se v Excelu. |

## Dokumenty a úložiště výstupů

| Entita | Co to je |
|---|---|
| **Kalibrační list** | List v Excelu s vypočtenými výsledky. Exportuje se do PDF a je finálním výstupem pro zákazníka. |
| **PDF kalibračního listu** | Export Kalibračního listu. Nahrává se Pavlu Korčákovi ke kontrole a podpisu. |
| **copy03** | Složka na OneDrive Pavla Korčáka, kam kalibrátor nahrává PDF k připravení ke kontrole a podpisu. |
| **registrKL** | Složka ve sdílených dokumentech SharePointu (registr kalibračních listů), kam se archivuje použitý Excel. |

## Jak to do sebe zapadá

1. Kalibrátor vyplní **Forms** → **Power Automate** zapíše záznam do **TableAction**.
2. Kalibrátor doplní naměřené hodnoty do **TableAction**.
3. V **Excelu** se přes **Power Query** načtou data z TableAction, TableInfra, ListAssessment a ListCompanyInfra.
4. Kalibrátor vybere **etalon** a ID, Excel vyplní **Kalibrační list**, ten se exportuje do **PDF**.
5. PDF jde do **copy03** → **Pavel Korčák** ho podepíše, vytiskne, archivuje a předá **zákazníkovi**.
6. Souběžně se Excel uloží do **registrKL**.
