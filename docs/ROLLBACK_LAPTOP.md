# Rollback — wijzigingen aan de laptop

Regel: **vóór** elke wijziging aan de laptop hier noteren wat er verandert en hoe je het ongedaan maakt. Datum, wat, hoe terugdraaien, status.

## Vooraf bekende wijzigingen uit de STARTGIDS (19 oktober 2026)

| # | Wat verandert | Waar | Ongedaan maken |
|---|---|---|---|
| 1 | Git installeren (alleen als `git --version` niet werkt) | `C:\Program Files\Git` | Instellingen → Apps → Git → Verwijderen, of `winget uninstall --id Git.Git` |
| 2 | Map `C:\Projecten` en de git clone `C:\Projecten\ZoetenInval-werk` | `C:\Projecten` | Verwijder de map `C:\Projecten\ZoetenInval-werk` (en `C:\Projecten` als hij leeg is) in Verkenner |
| 3 | Git-instellingen **alleen voor deze repo** (`user.name`, `user.email`) | `C:\Projecten\ZoetenInval-werk\.git\config` | Verdwijnt met de map; of `git config --unset user.name` en `git config --unset user.email` |
| 4 | Tijdelijke uitpakmap | `C:\Projecten\_uitpak` | Map verwijderen |
| 5 | Python-omgeving voor de tests | `C:\Projecten\ZoetenInval-werk\.venv` | Map `.venv` verwijderen |
| 6 | Testbrowser van Playwright (±200 MB) | `%LOCALAPPDATA%\ms-playwright` | Map `ms-playwright` verwijderen |
| 7 | Inloggegevens voor GitHub in Git Credential Manager (bij de eerste `git push`) | Windows-referentiebeheer (Credential Manager) | Configuratiescherm → Referentiebeheer → Windows-referenties → `git:https://github.com` verwijderen |
| 8 | Kopie van het pakket in OneDrive | `C:\Users\leone\OneDrive\ZoetenIval` | Bestand verwijderen |
| 9 | Tijdelijke Playwright-kopie door `npx playwright install` (19 oktober 2026, per ongeluk gestart) | `%LOCALAPPDATA%\npm-cache\_npx` | Map `_npx` verwijderen, of `npm cache clean --force` |

Niet gewijzigd: je gewone Chrome, Python en Node.js zelf, systeeminstellingen, het register.

## Logboek (aanvullen tijdens het werk)

| Datum | Wat | Terugdraaien | Status |
|---|---|---|---|
| | | | |
