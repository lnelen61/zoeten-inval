# STARTGIDS Claude Code — Zoeten Inval

Voor Leo, op de Windows-laptop. Alle opdrachten zijn voor **PowerShell** (rechtsklik op Start → Terminal). Eén stap per keer; na elke stap volstaat "ok" in je chat met Claude. Elke stap die iets op de laptop installeert of aanmaakt staat ook in `docs\ROLLBACK_LAPTOP.md` met de manier om het ongedaan te maken.

## 1. Mappen

| Wat | Waar |
|---|---|
| Werkmap (git clone van de repo, niet in OneDrive) | `C:\Projecten\ZoetenInval-werk` |
| Afgewerkte bestanden en kopie van het pakket | `C:\Users\leone\OneDrive\ZoetenIval` |
| Tijdelijke uitpakmap (mag na gebruik weg) | `C:\Projecten\_uitpak` |

Je hebt al: Python 3.12, Node.js LTS, ffmpeg en Claude Code (ffmpeg heb je voor dit project niet nodig).

## 2. Eenmalig installeren

**Eerst lezen:** pak de zip eerst uit (stap 4, onderdeel "Expand-Archive") of open `docs\ROLLBACK_LAPTOP.md` in de zip. Daar staat vooraf **alles** wat deze gids op je laptop zet, met de opdracht om het ongedaan te maken. Je kunt het dus voor je begint nalezen.

### Stap 2.1 — Is Git aanwezig?

```
git --version
```
Verwacht: `git version 2.x.x.windows.x` (Claude Code op Windows heeft Git meestal al aan boord). Staat er een foutmelding ("niet herkend"), installeer dan Git:
```
winget install --id Git.Git -e --source winget
```
Sluit daarna de terminal en open hem opnieuw, en voer `git --version` nog eens uit.

## 3. De werkmap maken (git clone)

```
New-Item -ItemType Directory -Force -Path C:\Projecten | Out-Null
git clone https://github.com/lnelen61/zoeten-inval.git C:\Projecten\ZoetenInval-werk
cd C:\Projecten\ZoetenInval-werk
git config user.name "lnelen61"
git config user.email "lnelen61@users.noreply.github.com"
git status
```
Verwacht: `On branch main` en `Your branch is up to date with 'origin/main'`. De map bevat nu alleen wat in GitHub staat (o.a. `index.html`).

## 4. Het pakket in de werkmap zetten

Het pakket is `ZoetenIval-werkpakket-v1.0.zip` in `C:\Users\leone\OneDrive\ZoetenIval`.

```
Expand-Archive -Path "C:\Users\leone\OneDrive\ZoetenIval\ZoetenIval-werkpakket-v1.0.zip" -DestinationPath C:\Projecten\_uitpak -Force
robocopy C:\Projecten\_uitpak\ZoetenIval-werkpakket-v1.0 C:\Projecten\ZoetenInval-werk /E /XD .git
```
Robocopy geeft exitcodes onder 8 als het gelukt is (dus `0` tot `7` is goed). Daarna:

```
cd C:\Projecten\ZoetenInval-werk
git status
git diff --stat
```
`git status` toont de nieuwe bestanden (`CLAUDE.md`, `docs\`, `tests\`, …). `lokaal\` en `.venv\` mogen NIET in die lijst staan (ze worden genegeerd). `git diff --stat` toont of `index.html` verschilt van wat in GitHub staat; verschilt het, dan is de versie in het pakket nieuwer (bv. de schakelaar onderaan in Beheer kaart nog niet gepubliceerd).

## 5. Test-omgeving klaarzetten (eenmalig)

```
cd C:\Projecten\ZoetenInval-werk
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests\requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```
Dat downloadt ongeveer 150–200 MB (een testbrowser, alleen voor Playwright; je gewone Chrome verandert niet). Het staat in `docs\ROLLBACK_LAPTOP.md` met de verwijderopdrachten. Werkt `python` niet, probeer dan `py -3.12 -m venv .venv`.

## 6. Eén controle-opdracht die bewijst dat alles werkt

```
node tests\check_syntax.mjs; .\.venv\Scripts\python.exe tests\smoke_test.py
```
Verwacht: eerst `OK: 1 script-blok(ken) syntactisch geldig`, dan een reeks regels die met `OK` beginnen, en tot slot:
```
ALLES OK (19 controles)
```
Staat er ergens `FOUT`, stop dan en vraag Claude Code om de oorzaak te zoeken (zonder iets te wijzigen tot jij "ok" zegt).

## 7. Claude Code starten

```
cd C:\Projecten\ZoetenInval-werk
claude
```
Claude Code leest automatisch `CLAUDE.md`. Een goede eerste vraag: *"Lees CLAUDE.md en docs\DRAAIBOEK_VOORTGANG.md, en zeg me in vijf zinnen wat de stand is en wat er openstaat."*

## 8. Publiceren (kort; details in CLAUDE.md punt 8)

```
git status
git add -A
git commit -m "v1.1: korte omschrijving"
git tag v1.1
git push origin main --follow-tags
```
De eerste keer vraagt Git Credential Manager om in te loggen bij GitHub in je browser. Na 1–2 minuten staat de nieuwe versie online; de gsm's krijgen ze bij het opnieuw openen van de tegel. De regels in Firebase (`firebase\rules.json`) publiceer je apart in de Firebase-console.

## 9. Terug naar de vorige versie

```
git log --oneline -5
git revert HEAD
git push origin main
```

## 10. Als iets niet werkt

| Melding | Oorzaak en oplossing |
|---|---|
| `git` niet herkend | Terminal heropenen, anders stap 2.1 |
| `Permission denied` / loginvenster bij push | Inloggen bij GitHub als `lnelen61` in het venster dat opent |
| Rooktest: `playwright`-fout over ontbrekende browser | `.\.venv\Scripts\python.exe -m playwright install chromium` opnieuw |
| `Expand-Archive` meldt dat het bestand bestaat | `-Force` staat al in de opdracht; controleer of de zip in de OneDrive-map staat |
| Pagina toont oude versie op gsm | Tegel helemaal afsluiten en opnieuw openen, 2 minuten wachten na het pushen |
