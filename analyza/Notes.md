# Notes

překresli toto do souboru before
toto jsou instance:
https://performance4cz.sharepoint.com/sites/infrastructure/Lists/TableInfrastructure/AllItems.aspx?FilterFields1=LinkTitle&FilterValues1=KCZM03196%3B%23KCZM03249%3B%23KCZM03250%3B%23KCZM06073%3B%23KCZM06074%3B%23KCZM06075&FilterTypes1=Computed&viewid=c2659113%2De0c9%2D46a7%2Dbdcc%2D5d4332304cf3

https://performance4cz.sharepoint.com/sites/infrastructure/Lists/TableAction/Meridla.aspx?FilterField1=ItemCode%5Fx003a%5F%5Fx0020%5FTechSpec2&FilterValue1=teplom%C4%9Br%2Fvlhkom%C4%9Br%20digit%C3%A1ln%C3%AD&FilterType1=Lookup&viewid=73ce118b%2D56d3%2D40b6%2D9e39%2Decdf79b8609b&newTargetListUrl=%2Fsites%2Finfrastructure%2FLists%2FTableAction&viewpath=%2Fsites%2Finfrastructure%2FLists%2FTableAction%2FMeridla%2Easpx

https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=FDCpPOAHCEW0A3i5iPmcv67jCVKgcNBNmWNy_0ep0AlUNU9GUThFTjNDM1cxRk8zS09WNkxCQkhRRyQlQCN0PWcu

https://make.powerautomate.com/environments/Default-3ca93014-07e0-4508-b403-78b988f99cbf/flows/shared/7047cf4d-4457-4956-9be6-4629a5515b3b/details

https://performance4cz-my.sharepoint.com/personal/pavel_korcak_performance4_cz1/_layouts/15/onedrive.aspx?CT=1756386324681&OR=OWA%2DNT%2DMail&CID=68075efb%2D0214%2Dbbb5%2D168c%2D22f215aa7071&e=5%3A8acd801b2334456aa566e32919633820&sharingv2=true&fromShare=true&at=9&cidOR=Client&id=%2Fpersonal%2Fpavel%5Fkorcak%5Fperformance4%5Fcz1%2FDocuments%2Fcopy%2Fcopy03&FolderCTID=0x012000BE6EFE3FD8E6E84EB5846E9CC34A50C5&view=0

https://performance4cz.sharepoint.com/sites/infrastructure/Sdilene%20dokumenty/Forms/AllItems.aspx?id=%2Fsites%2Finfrastructure%2FSdilene%20dokumenty%2FregistrKL&viewid=127ce7c4%2Dd94a%2D45e0%2D917b%2Dca5b8323f20d&view=7&q=act002538

https://performance4cz.sharepoint.com/sites/infrastructure/Lists/ListCompanyInfra/AllItems.aspx

https://performance4cz.sharepoint.com/sites/infrastructure/Lists/ListAssessment/AllItems.aspx

excel pro TeHum měřidla

popis flow:
kalibrace se zadá do formsů pouze, kdy, kdo ji provedl.
flow přepíše forms do TableAction
uživatel zadá do TableAction naměřené hodnoty
uživatel otevře excel pro TeHum měřidla aktualizuje data přes powerquery, data se natahují z TableAction, TableInfra, ListAssesment a List CompanyInfra
vybere v excelu etalon a id z TableAction podle toho pro co chce dělat kalibrační list
excel sám napočítá hodnoty a vyplní list "Kalibrační list", uživatel ho vyexportuje jako pdf
pdf uživatel nahraje Pavlu Korčákovi do copy03, on ho pak později zkontroluje a podepíše digitálním podpisem vytiskne, zarchivuje a vytištěný předá zákazníkovi
excel se nahraje na sharepoint registrKL
