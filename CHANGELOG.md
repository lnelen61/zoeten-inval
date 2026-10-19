# Wijzigingslogboek

Formaat: nieuwste bovenaan. Versieregels: zie CLAUDE.md punt 4.

## v1.0 — 19 oktober 2026 (eerste versie in het werkpakket)

Stand van alles wat tot dan gebouwd was:
- Tegelsysteem met gedeelde klantrekeningen, beheer van de kaart, vrije prijs ("Dagartikel").
- Anonieme aanmelding voor personeel; beheerder via gebruikersnaam + wachtwoord (Firebase Authentication), beheerderslijst in de database.
- Toogscherm: naam per gsm, knop "Stuur naar toog" (standaard uit, schakelaar onderaan in Beheer kaart), tablet via `?toog` met één rij kaarten (oudste links, geleverd grijs rechts, recentst geleverd het eerst), geluid bij nieuwe bestelling, regel schrappen met het minteken.
- Tegels ongeveer half zo hoog; lange namen krimpen tot ze op één lijn passen.
- Instructiezin bovenaan verwijderd; "Beheer kaart" onderaan de pagina.
- Dagtotaal en totaal-van-alle-open-rekeningen bewust verwijderd (totalen alleen per open klant).
- Open bestellingen op de tablet verdwijnen nooit door tijd; geleverde bestellingen ouder dan 3 dagen worden door de tablet gewist.
- Beveiligingsregels uitgebreid met `instellingen` en `bestellingen` (zie `firebase/rules.json`).
