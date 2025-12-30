# Bug-001: Bewertung eines gekauften Artiekels mit Kommentar
## Priorität: Mittel
### Reproduktionsschritte:
1. Produktseite von Birchwood Quarter Pounders öffnen.
2. Scrolle zum Bewertungsbereich.
3. Wähle 4 Sterne aus.
4. Trage Kommentar "Top Produkt" ein.
5. Klicke auf Send.

### Erwatetes Ergebnis: 
Bewertung erscheint korrekt mit 4 Sternen und Kommentar.
### Aktuelles Ergebnis:
Bewertung erscheint mit 4 Sternen und Name aber ohne Kommentar.
### Screenshots / Anhänge:
![screebshots](../screenshots/tc_01_durchführung.png)
![screebshots](../screenshots/tc_01_ergebnis.png)

----

# Bug-002: Versandkosten bei genau 20,00 € mit anschließender änderung auf 18,00 €
## Priorität: Hoch
### Reproduktionsschritte:
1. wähle 10 x Gala äpfel
2. Warenkorb hinzufügen
3. Warenkorb auswählen 
4. Anzahl im Waren korb von 10 auf 9 ändern
5. kosten auflistung überprüfen

### Erwatetes Ergebnis: 
kosten der Ware plus lieferkosten
### Aktuelles Ergebnis:
kosten der Ware ohne lieferkosten
### Screenshots / Anhänge:
![screebshots](../screenshots/tc_09_warenkorb_über.png)
![screebshots](../screenshots/tc_09_warenkorb_weniger.png)