Testfälle – Produktbewertungen 

Nur registrierte Nutzer dürfen Produkte bewerten.

Bewertungen sind nur nach einem Kauf möglich.

Nutzer dürfen ihre Bewertung nicht ändern/löschen, wenn kein Kauf getätigt wurde.

Durchschnittsbewertung wird nur auf der Produktseite, nicht unter dem Produktnamen, angezeigt.

### 1. Berechtigung zur Bewertung
TC01 – Gastnutzer sieht kein Bewertungsformular

Vorbedingung: Nutzer ist nicht eingeloggt

Aktion: Produktseite öffnen

Erwartetes Ergebnis: Bewertungsoption wird nicht angezeigt

TC02 – Gast Nutzer, nach Kauf → Bewertung möglich

Vorbedingung: Eingeloggt, Produkt wurde gekauft

Aktion: Produktseite öffnen

Erwartetes Ergebnis: Meldung: „Bewertungen sind nur nach Kauf möglich“ oder Button deaktiviert

TC03 – Registrierter Nutzer nach Kauf → Bewertung möglich

Vorbedingung: Produkt wurde gekauft

Aktion: Produktseite öffnen

Erwartetes Ergebnis: Bewertungsformular sichtbar

### 2. Bewertung ändern/löschen
TC04 – Nutzer ohne Kauf versucht Bewertung zu ändern

Vorbedingung: Keine Bestellung des Produkts

Aktion: Bewertung ändern/löschen anklicken

Erwartetes Ergebnis: Aktion nicht erlaubt → keine änerung

TC05 – Nutzer nach Kauf ändert Bewertung

Vorbedingung: Produkt wurde gekauft

Aktion: Bewertung bearbeiten

Erwartetes Ergebnis: Änderung erfolgreich gespeichert

TC06 – Nutzer nach Kauf löscht Bewertung

Erwartetes Ergebnis: Bewertung wird entfernt; Durchschnitt neu berechnet

### 3. Durchschnittsbewertung
TC07 – Durchschnittswert wird nur auf der Produktseite angezeigt

Aktion: Produkt in der Suchliste / Kategorie ansehen

Erwartetes Ergebnis: Keine Sternebewertung

TC08 – Durchschnitt wird auf der Produktseite angezeigt

Aktion: Produktseite öffnen

Erwartetes Ergebnis: Sterne-Bewertung sichtbar

Testfälle – Altersverifikation 

Alter muss bei jedem Seitenaufruf bestätigt werden.

Alter wird nicht gespeichert (kein Cookie, keine Speicherung im Profil).

Zum Schutz müssen Nutzer ihr Geburtsdatum eintippen, nicht nur „Ja“ klicken.

### 1. Altersprüfung pro Seitenaufruf
TC-AGE-01 – Altersprüfung erscheint bei jedem Seitenaufruf

Aktion: Produktseite öffnen → Seite neu laden

Erwartetes Ergebnis: Altersabfrage erscheint erneut

### 2. Kein Speichern der Altersangabe
TC-AGE-02 – Keine Speicherung → Nutzer muss erneut prüfen

Aktion: Alter bestätigen → Browser schließen → Seite erneut öffnen

Erwartetes Ergebnis: Altersprüfung erscheint wieder

### 3. Geburtsdatum-Eingabe 
TC-AGE-03 – Nutzer muss Geburtsdatum eingeben

Aktion: Age-Gate anzeigen

Erwartetes Ergebnis: Nur Geburtsdatum-Eingabe möglich

TC-AGE-04 – Minderjähriger wird blockiert

Eingabe: Geburtsdatum unter 18

Erwartetes Ergebnis: Zugriff verweigert

TC-AGE-05 – Volljähriger wird durchgelassen

Eingabe: Geburtsdatum ≥ 18

Erwartetes Ergebnis: Zugriff erlaubt

Testfälle – Versandkostenregel (ab 20 € kostenlos)

Versandkosten entfallen ab einem Bestellwert von 20 €.

Versandkosten aktualisieren sich live, wenn Produkte hinzugefügt wird nicht bei entfernung.

Versandkosten fallen nicht erneut an, wenn der Betrag nachträglich wieder unter 20 € sinkt.

Keine Gutscheine zum Testen verfügbar → Versandlogik ohne Rabatt testen.

Testfälle
### 1. Schwellenwertprüfung 20 €
TC-S-01 – Bestellwert genau 20 € → Versandkosten entfallen

Eingabe: Warenkorbwert = 20 €

Erwartung: 0 € Versandkosten

TC-S-02 – Bestellwert unter 20 € → Versandkosten fallen an

Eingabe: 19,99 €

Erwartung: Versandkosten angezeigt

### 2. Live-Updates der Versandkosten
TC-S-03 – Versandkosten verschwinden, wenn Nutzer über 20 € kommt

Aktion: Produkt hinzufügen → Wert steigt von <20 € auf >20 €

Erwartung: Versandkosten verschwinden 

TC-S-04 – Versandkosten bleiben weg, fallen nincht erneut an

Aktion: Produkt entfernen → Wert fällt von 22 € auf 18 €

Erwartung: sollten erneut an fallen 