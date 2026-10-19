# CLAUDE.md — Zoeten Inval telsysteem

Dit bestand leest Claude Code bij elke start. Lees het volledig, daarna `docs/DRAAIBOEK_VOORTGANG.md` (laatste blok onderaan = overdrachtsblok).

> **LET OP: deze repository is OPENBAAR** (GitHub Pages in het gratis plan vraagt dat). Alles wat je commit, kan iedereen lezen en staat bovendien op de website. Zet hier dus nooit wachtwoorden, tokens, sleutelbestanden, e-mailadressen van personen, de beheerders-UID of persoonlijke foto's/filmpjes in. Zulke dingen horen in `lokaal/` (staat in `.gitignore`).

## 1. Wat dit project is

Een tegelsysteem (web-app) om bestellingen in café **Zoeten Inval** (café van Leo's zoon) te tellen op de gsm van het personeel (~6 toestellen), met:

- tegels per drank met prijs; tikken = 1 stuk bijtellen; optellijst, totaal, wisselgeld;
- **gedeelde klantrekeningen** ("op de rekening van Jan") over alle gsm's heen, afrekenen en wissen;
- **kaartbeheer** door 1 à 2 beheerders (prijzen/artikelen/categorieën wijzigen), personeel kan niet bewerken;
- **toogscherm** (optioneel, standaard UIT): "Stuur naar toog" op de gsm, en op een tablet achter de toog `…/?toog` met kaarten per bestelling en één tik "Geleverd".

Alles is **één bestand: `index.html`** (HTML + CSS + JavaScript, geen build, geen frameworks). Gehost op GitHub Pages, gegevens in Firebase Realtime Database (gratis Spark-plan).

- Live adres: https://lnelen61.github.io/zoeten-inval/
- Toogtablet: https://lnelen61.github.io/zoeten-inval/?toog
- Repository: https://github.com/lnelen61/zoeten-inval (branch `main`, map `/ (root)`)
- Firebase-project: `zoeten-inval-telsysteem` (Realtime Database, regio europe-west1, Spark/gratis)

## 2. Huidige versie en stand

- **Versie: v1.0** (zie `VERSION` en `CHANGELOG.md`), gemaakt 19 oktober 2026.
- Gebouwd en getest: tegels (laag, 1 lijn naam + 1 lijn prijs, lange namen krimpen), klantrekeningen, beheer kaart, toogscherm (gsm + tablet), schakelaar "Toogscherm aan" onderaan in Beheer kaart.
- Het pakket bevat de nieuwste `index.html`; die staat ook al in GitHub (gepubliceerd op 19 oktober 2026).
- Uitgebreide stand en beslissingen: `docs/DRAAIBOEK_VOORTGANG.md`. Techniek: `docs/ARCHITECTUUR.md`.

## 3. Mappenstructuur

```
C:\Projecten\ZoetenInval-werk\        <- git clone van de repository (NIET in OneDrive)
  index.html                          <- de hele app (moet in de root blijven: GitHub Pages)
  CLAUDE.md                           <- dit bestand
  STARTGIDS_Claude_Code.md            <- eenmalige installatie en start
  VERSION, CHANGELOG.md               <- versienummer en wijzigingslogboek
  .gitignore, .gitattributes
  docs\
    ARCHITECTUUR.md                   <- gegevensstructuur, auth, werking, openbaar vs. geheim
    DRAAIBOEK_VOORTGANG.md            <- voortgang + overdrachtsblok onderaan
    ROLLBACK_LAPTOP.md                <- elke wijziging aan de laptop + hoe ongedaan maken
  firebase\
    rules.json                        <- de beveiligingsregels (handmatig te publiceren in de Firebase-console)
  tests\
    check_syntax.mjs                  <- controle 1 (Node)
    smoke_test.py, mock_firebase.js   <- controle 2 (Playwright, nagebootste Firebase)
    requirements.txt
  lokaal\                             <- STAAT IN .gitignore, gaat nooit naar GitHub
    BEHEERGEGEVENS.md                 <- niet-geheime beheergegevens (gebruikersnaam, UID, links)
    archief\                          <- oude versies en wegwerpbestanden
  .venv\                              <- Python-omgeving voor de tests (gitignored)
```

Alles op GitHub Pages is openbaar bereikbaar op `https://lnelen61.github.io/zoeten-inval/<pad>`, dus ook `docs\` en `tests\`. Dat is bewust acceptabel omdat er niets gevoeligs in staat.

## 4. Versieregels

- Formaat `vMAJOR.MINOR`. MINOR omhoog voor elke wijziging die live gaat (v1.0 → v1.1 …). MAJOR alleen bij een wijziging die de gegevensstructuur in Firebase of de werkwijze van het personeel breekt.
- Bij elke wijziging die gepubliceerd wordt: `VERSION` aanpassen, `CHANGELOG.md` aanvullen, voortgang in `docs/DRAAIBOEK_VOORTGANG.md` noteren, committen, **taggen** (`git tag v1.1`), pushen met tags.
- Nooit force-pushen op `main`. Een kapotte versie herstel je met `git revert` (zie STARTGIDS), niet met geschiedenis herschrijven.
- Commit-berichten in het Nederlands, kort, bv. `v1.1: knop Stuur naar toog groter`.

## 5. Hoe testen (altijd vóór committen)

Vanuit de projectmap `C:\Projecten\ZoetenInval-werk` (PowerShell):

1. Syntaxis (geen installatie nodig):
   ```
   node tests\check_syntax.mjs
   ```
   Verwacht: `OK: 1 script-blok(ken) syntactisch geldig`
2. Rooktest in een echte browser met nagebootste Firebase:
   ```
   .\.venv\Scripts\python.exe tests\smoke_test.py
   ```
   Verwacht: 19 regels die met `OK` beginnen en op het einde `ALLES OK (19 controles)`. Bij een fout begint de regel met `FOUT` en is de exitcode 1.
3. Handmatig op de echte site (niet te automatiseren, want de echte Firebase wordt niet in de tests gebruikt): na het pushen 1–2 minuten wachten, dan op een gsm de tegel openen en een testbestelling doen; bij toogwijzigingen ook op de tablet kijken. Testklant "Test" achteraf wissen.

**Wat de tests NIET dekken:** echte Firebase-verbinding, aanmelden als beheerder, de beveiligingsregels, meerdere toestellen tegelijk, geluid, iOS/Safari-gedrag. Zeg dat altijd eerlijk als je een wijziging als "getest" meldt.

Lokale blik op de pagina zonder Firebase kan met `python -m http.server 8000` in de projectmap en `http://localhost:8000/` (zonder Firebase blijft de pagina op de standaardkaart staan en werkt delen niet).

## 6. Vaste conventies voor de code

- **Eén bestand** `index.html`; geen build, geen npm-pakketten in de app. Firebase compat-SDK 10.14.1 via de gstatic-CDN (app, auth, database).
- Taal van de interface: **Nederlands (Vlaams)**. Variabelen en functies mogen Nederlands of Engels zijn, maar blijf consequent in het bestaande.
- **Elke variabele krijgt commentaar** dat zegt waarvoor ze dient (Leo is een zelfverklaard halve amateur en moet de code kunnen lezen).
- Kleuren via CSS-tokens op `:root`, met donkere modus; tegels laag houden (1 lijn naam, 1 lijn prijs, ~51 px).
- Prijzen in **centen** (gehele getallen). Vrije prijs staat in de database als `-1` en in de UI als `null`.
- Het blok `firebaseConfig` bovenaan het script nooit aanpassen zonder opdracht (een fout daar legt alles plat).
- Luisteraars op Firebase worden bij elke wijziging van de aanmeldstatus opnieuw gestart (`liveRefs`, `startListening()`); houd dat zo.
- localStorage-sleutels op de gsm: `zi-device`, `zi-order`, `zi-cust`, `zi-custid`, `zi-prices`, `zi-naam`. Wijzig de betekenis niet zonder migratie.
- Open bestellingen op de toogtablet verdwijnen **nooit** door tijd; alleen geleverde bestellingen ouder dan 3 dagen worden door de tablet gewist. Er zijn bewust **geen** dagtotaal en geen totaal-van-alle-rekeningen (alleen het bedrag per open klant).
- Geen afhankelijkheden toevoegen, geen externe scripts behalve de drie Firebase-bestanden.

## 7. Geheimen, openbare gegevens en media

**Mag openbaar (staat al in `index.html`):** de Firebase-webconfiguratie (`apiKey`, `authDomain`, `databaseURL`, `projectId`, `storageBucket`, `messagingSenderId`, `appId`). Dat is een adres, geen sleutel: de toegang wordt bewaakt door de regels in `firebase/rules.json` en door Firebase Authentication.

**Nooit in de repo of in de zip:**
- Firebase-serviceaccountsleutels (JSON), Admin-SDK-sleutels, tokens, GitHub-tokens;
- het beheerderswachtwoord en andere wachtwoorden;
- e-mailadressen van personen, de beheerders-UID;
- persoonlijke foto's of filmpjes (er zitten er geen in het pakket; de menufoto's uit het begin van het project zijn niet meegeleverd, de actuele kaart zit in Firebase onder `cafe/kaart` en als standaardkaart `BASE_MENU` in `index.html`).

**Waar het wél staat:**
- `lokaal\BEHEERGEGEVENS.md` (gitignored): beheerdersgebruikersnaam, UID, links naar de Firebase-console en het overdrachtsdocument. **Zonder wachtwoorden.**
- Het beheerderswachtwoord kent Leo; het staat niet in bestanden. Vergeten wachtwoord: Firebase-console → Authentication → Users → ⋮ → Reset password of gebruiker verwijderen en opnieuw maken.

**Hoe Claude Code ermee omgaat:** nooit vragen om wachtwoorden of sleutels in de chat; nooit zelf een sleutel aanmaken of in een bestand zetten; voor alles in de Firebase-console geeft Leo de stappen zelf uit (Claude Code geeft de opdrachten, Leo klikt). Controleer vóór elke commit met `git status` en `git diff --cached` dat er niets uit `lokaal\` of met een geheim in zit. Als je per ongeluk een geheim hebt gecommit: niet pushen, `git reset --soft HEAD~1`, bestand uit de index halen. Is het al gepusht: sleutel meteen intrekken in de console en Leo waarschuwen.

## 8. Publiceren

1. Tests draaien (punt 5), `VERSION` en `CHANGELOG.md` bijwerken.
2. `git add -A`, `git status` nakijken (niets uit `lokaal\`), `git commit -m "v1.x: korte omschrijving"`, `git tag v1.x`.
3. `git push origin main --follow-tags`. De eerste keer opent Git Credential Manager de browser om bij GitHub in te loggen; er wordt geen token in de repo bewaard.
4. GitHub Pages bouwt opnieuw (1–2 minuten). Controle: `https://github.com/lnelen61/zoeten-inval/actions`. De gsm's krijgen de nieuwe versie zodra ze de tegel opnieuw openen.
5. **Regels** in Firebase wijzigen gaat NIET via git: kopieer `firebase/rules.json` naar Firebase-console → Realtime Database → Regels → Publiceren (op een laptop kopiëren, op een iPad kunnen slimme aanhalingstekens de regels breken).
6. Terug naar een vorige versie: `git revert <commit>` en pushen.

## 9. Open punten

- Zoon van Leo als tweede beheerder toevoegen (gebruiker maken in Firebase Authentication én zijn UID zetten onder `cafe/beheerders` met waarde `true`; stappen in `docs/ARCHITECTUUR.md`).
- Eigenaarschap van het Firebase-project en het GitHub-account later overdragen (stappen in het overdrachtsdocument; **nooit** de repo "transferen" naar een ander account: het adres verandert dan en de tegels breken).
- Reservekopie: JSON-export van de database (Firebase-console → Data → ⋮ → Export JSON) en een kopie van `index.html` buiten GitHub bewaren.
- `spraaktest.html` is geschrapt (Nederlands bij Stembediening van iOS niet beschikbaar). Staat het nog in de repo, dan verwijderen (`git rm spraaktest.html`).
- Optioneel/later: bijkomende features op vraag van Leo; wifi/4G moet overal in het café goed zijn, ook op het terras.

## 10. Werkafspraken met Leo (altijd volgen)

- **Nederlands.** Kort, praktisch, bottom-line eerst.
- **Stap voor stap: één stap per bericht**, telkens met de **volledige opdracht** erbij (nooit "de opdracht van daarnet"). Een korte "ok" van Leo volstaat als bevestiging; vraag geen screenshot tenzij iets onduidelijk is of mislukt.
- **Eerst documenteren, dan de volgende stap.** Bevindingen en wijzigingen eerst in de projectdocumenten (`docs\DRAAIBOEK_VOORTGANG.md`, `CHANGELOG.md`), dan pas de volgende stap of opdracht. Leo heeft geen eigen geheugen en rekent op die bestanden.
- **Vóór elke wijziging op de laptop** (installeren, activeren, instellingen) eerst in `docs\ROLLBACK_LAPTOP.md` noteren wat er verandert én hoe je het ongedaan maakt.
- **Leo beslist wanneer we stoppen.** Zeg nooit "de laatste stap voor vandaag"; bied na een stap gewoon aan wat er nog openstaat.
- **Variabelen in code uitleggen met commentaar** (wat is het, waarvoor dient het).
- Directe, eerlijke feedback; zeg wat je getest hebt en wat niet.
- Leo gebruikt een iPhone (recente iOS) en een iPad; iOS-instructies moeten op de huidige iOS-menu's gebaseerd zijn. Staptekst voor Firebase/GitHub-console: telkens de exacte Engelse knoplabels vermelden zoals ze in de console staan.
- Leo is niet de enige gebruiker van deze gegevens: personeel gebruikt de tegels live in het café. Test dus nooit op de echte rekeningen zonder het te zeggen, en ruim testgegevens (klant "Test") achteraf op.
