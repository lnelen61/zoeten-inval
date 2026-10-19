# Architectuur — Zoeten Inval telsysteem

Stand v1.0 (19 oktober 2026). Geen persoonlijke gegevens in dit bestand: de repo is openbaar.

## Onderdelen

| Onderdeel | Waar | Wat het doet |
|---|---|---|
| De app | `index.html` in de repo, gepubliceerd via GitHub Pages (branch `main`, map root) | Alle schermen en logica in één bestand |
| De gegevens | Firebase Realtime Database, project `zoeten-inval-telsysteem`, regio europe-west1, Spark (gratis) | Kaart, instellingen, open rekeningen, bestellingen, afgerekende rekeningen |
| Aanmelden | Firebase Authentication | Personeel: anoniem (automatisch). Beheerder: gebruikersnaam + wachtwoord |
| Beveiliging | Regels in Firebase (`firebase/rules.json`, handmatig te publiceren in de console) | Wie wat mag lezen/schrijven |

De gsm's halen de pagina op bij GitHub en praten daarna rechtstreeks met Firebase. GitHub en Firebase praten niet met elkaar. Alle toestellen (gsm's en toogtablet) hoeven niet in hetzelfde wifi-netwerk te zitten; internet (wifi of 4G/5G) volstaat.

Firebase-webconfiguratie (openbaar, staat in `index.html`): `authDomain zoeten-inval-telsysteem.firebaseapp.com`, `databaseURL https://zoeten-inval-telsysteem-default-rtdb.europe-west1.firebasedatabase.app`, `projectId zoeten-inval-telsysteem`. De `apiKey` is een adres, geen geheim.

## Gegevensstructuur (alles onder `cafe`)

| Pad | Inhoud | Lezen | Schrijven |
|---|---|---|---|
| `cafe/kaart` | Lijst van categorieën `{cat, sub, cls, items:[[naam, prijs in centen]]}`. Vrije prijs = `-1` (in de UI `null`). | elk aangemeld toestel | alleen beheerders |
| `cafe/instellingen/toogscherm` | `true` of `false` (afwezig = uit) | elk aangemeld toestel | alleen beheerders |
| `cafe/rekeningen/<id>` | Open rekening `{name, items:[[naam, prijs]], updated, bezig, bezigSinds}`; `bezig` = toestel dat ze aan het afrekenen is (claim via transactie, na 10 min als vastgelopen beschouwd) | elk aangemeld toestel | elk aangemeld toestel |
| `cafe/afgerekend/<id>` | Afgeronde rekening `{name, items, total, ts, device}` | elk aangemeld toestel | elk aangemeld toestel |
| `cafe/bestellingen/<id>` | Toogbestelling `{door (medewerker), klant, items:[[naam, prijs]], ts, status ("open"/"geleverd"), geleverdTs, rekeningId, device}` | elk aangemeld toestel | elk aangemeld toestel |
| `cafe/beheerders/<UID>` | `true` voor elke beheerder-UID | niemand via de app | niemand via de app (alleen de eigenaar in de console) |

Index: de app vraagt `cafe/bestellingen` volledig op (kleine hoeveelheid). Geleverde bestellingen ouder dan 3 dagen worden door de tablet gewist.

## Aanmelden en rollen

- **Personeel:** `signInAnonymously()` bij het openen; Firebase ruimt anonieme gebruikers die 30 dagen niet gebruikt zijn automatisch op (Auto clean-up staat aan). Een gsm meldt zich daarna vanzelf opnieuw aan; de gegevens staan in de database.
- **Beheerder:** knop "Beheer kaart" onderaan → gebruikersnaam + wachtwoord. De pagina plakt `@zoeten-inval-telsysteem.firebaseapp.com` achter een gebruikersnaam zonder `@`; er wordt nooit echte mail verstuurd. Beheerder-zijn = de UID staat onder `cafe/beheerders` met waarde `true` (Boolean).
- **Eigenaar:** wie het Firebase-project (Google-account) en de GitHub-repo beheert.
- `isAdmin` in de app = niet-anonieme gebruiker; de **regels** beslissen echt of schrijven mag.

### Een beheerder toevoegen (twee stappen, in de Firebase-console, door een eigenaar)

1. Authentication → Users → Add user: e-mail = gebruikersnaam + `@zoeten-inval-telsysteem.firebaseapp.com`, wachtwoord naar keuze (minstens 6 tekens). Kopieer daarna de **User UID** van die rij.
2. Realtime Database → Data → `cafe` → `beheerders`: **+** → naam = de UID, type **Boolean**, waarde **true**. (Op een iPad: Boolean kies je in de keuzelijst bij het type; hoofdletters in `beheerders` vermijden.)

Zonder stap 2 kan de gebruiker wel aanmelden, maar krijgt hij bij Bewaren "Geen rechten".

## Werking van de app (waar zit wat in index.html)

- **Tegels:** `buildTiles()` bouwt per categorie een raster; `fitNames()` verkleint lange namen tot ze op één lijn passen; een tik doet `order.push(naam)` en `render()`.
- **Kaart:** `BASE_MENU` is de ingebouwde standaardkaart (alleen gebruikt als `cafe/kaart` leeg is); `MENU` is de actieve kaart uit de database; `menuForDb()`/`validMenu()` zetten om en controleren bij Bewaren.
- **Rekeningen:** `saveTab()` (transactie: bij een bestaande naam wordt bijgeteld), `openTab()` (claimt de rekening), `settle()` (schrijft naar `afgerekend` en verwijdert de open rekening). `baseItems` onthoudt wat er bij het openen al op stond.
- **Toog:** `sendToog()` → `saveTab(items)` bewaart op de rekening en schrijft een nieuwe `cafe/bestellingen`-regel met alleen het **nieuwe** deel. De tablet (`?toog`, `IS_TOOG`) luistert op `cafe/bestellingen`, toont `renderToog()` (één rij kaarten), "Geleverd" zet status en `geleverdTs`; `removeFromBestelling()` schrapt een regel in bestelling én rekening; `beep()` geeft geluid na een tik op "Geluid aan".
- **Live luisteraars:** `startListening()` start alle Firebase-luisteraars (`liveRefs`) en wordt bij elke wijziging van de aanmeldstatus opnieuw uitgevoerd; anders blijven luisteraars na uit-/inloggen als beheerder dood.
- **Op de gsm bewaard (localStorage):** `zi-device`, `zi-order`, `zi-cust`, `zi-custid`, `zi-prices`, `zi-naam`.

## Beveiliging: wat is dit (niet)

Wie het adres kent, kan rekeningen zien, wijzigen en wissen (bewuste afweging: eenvoud boven toegangscontrole voor het personeel). De kaart en de toogschakelaar kan alleen een beheerder wijzigen. Wil de eigenaar de toegang verder dichtzetten, dan kan dat met Firebase App Check of met een personeelslogin (elke werknemer een gebruiker); dat is een bewuste keuze die later kan.

## Kosten en limieten (stand oktober 2026)

Spark-plan: 100 gelijktijdige verbindingen, 1 GB opslag, 10 GB downloads per maand; het café gebruikt ~6 verbindingen en enkele MB per jaar. GitHub Pages: gratis voor openbare repo's. **Niet upgraden naar Blaze** (kredietkaart nodig, niet nodig).

## Back-up en herstel

- Broncode: elke commit in GitHub is een versie; daarnaast een kopie van `index.html` buiten GitHub bewaren.
- Database: Firebase-console → Realtime Database → Data → ⋮ → Export JSON; terugzetten met Import JSON op dezelfde plaats. Doe dit na elke grote kaartwijziging.

## Als iets stopt

- GitHub Pages weg → `index.html` op een andere gratis hosting zetten; tegels moeten dan eenmalig opnieuw op het beginscherm.
- Firebase weg → de pagina moet naar een andere database verwezen worden.
- Gsm toont "geen verbinding": wifi of 4G nakijken; een lopende bestelling blijft lokaal op de gsm staan.
