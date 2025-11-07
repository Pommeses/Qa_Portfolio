# Testplan – GroceryMate

---

## 1. Produktanalyse

### Zielsetzung
Das Ziel der Seite **GroceryMate** ist es, Nutzern Online Lebensmittel und Alkohol zu verkaufen. Dies soll **schnell und einfach** möglich sein und über einen **leichten und übersichtlichen Zugang** verfügen.

### Zielnutzergruppe
Das Angebot richtet sich an **Endverbraucher aller Altersgruppen**, wobei **Altersbeschränkungen für bestimmte Produkte** berücksichtigt werden müssen.

### Hardware- und Software-Spezifikationen

**Hardwareanforderungen:**
- Geräte: PCs, Laptops, Smartphones, Tablets  
- Spezifikationen:  
  - Standardkonfigurationen für Android- und iOS-Geräte  
  - Desktops mit mindestens 4 GB RAM und 2 GHz Prozessor  

**Softwareanforderungen:**
- Betriebssysteme: Windows, macOS, Android, iOS  
- Browser: Chrome, Firefox, Safari, Edge  
- Abhängigkeiten: Backend-Dienste, Zahlungsschnittstellen  

### Funktionalität des Produkts
- Registrierung und Login  
- Produktsuche über Suchleiste  
- Filterung und Sortierung von Produkten  
- Favoritenfunktion  
- Navigationsmenü mit Seiten: Home, Shop, Favorites, Contact  

---

## 2. Teststrategie entwerfen

### Testumfang
- Registrierung und Login  
- Produktsuche über Suchleiste  
- Filterung und Sortierung von Produkten  
- Favoritenfunktion  
- Navigationsmenü mit Seiten: Home, Shop, Favorites, Contact  
- Altersvalidierung  

**Außerhalb des Umfangs:**
- Kaufoptionen  
- Zahlungsprozesse  
- Backend-Datenbankoperationen  
- Integration von Drittanbietern  

### Geplante Testarten
- Funktionstests  

---

## Risiken und Gegenmaßnahmen

| Bereich / Test        | Risiko                                                   | Gegenmaßnahme |
|------------------------|----------------------------------------------------------|----------------|
| Navigation             | Falsche Verknüpfungen                                   | Hauptbuttons durchgehen |
| Produktsuche           | Falsches oder nicht angezeigtes Produkt                 | Suchfunktion mit verschiedenen Produkten überprüfen |
| Registrierung/Login    | Account wird nicht angezeigt oder existiert mehrfach    | Verschiedene Accounts mit ähnlichen/glichen Namen anlegen |
| Altersverifikation     | Zugriff auf beschränkte Produkte unabhängig vom Alter   | Tests mit verschiedenen Altersangaben durchführen |
| Favoritenfunktion      | Produkte werden nicht oder falsch gespeichert           | Mit unterschiedlichen Produkten Hinzufügen und Entfernen testen |

**Weitere Risiken:**
- Entwicklungsverzögerungen → Zeitpuffer im Zeitplan einplanen  
- Fehlende Testdaten → Erstellen von Mock-Daten  
- Ressourcenengpässe → Ersatzpersonen identifizieren  

**Testlogistik:**  
Alle Positionen: **Felix Mönig**

---

## 3. Testziele definieren

### Ziele

**Funktionalität:**  
- Sicherstellen, dass alle Hauptfunktionen wie vorgesehen arbeiten.  

**Benutzeroberfläche (GUI):**  
- Überprüfung der Funktionalität und Übersichtlichkeit der Seite bzw. Buttons.  

### Erwartete Ergebnisse
- Alle Buttons (Home, Shop, Favorites, Contact) führen auf die korrekte Seite.  
- Die Suchfunktion liefert relevante Produkte passend zur Eingabe.  
- Login funktioniert und keine Doppel-Accounts sind möglich.  
- Altersverifikation blockiert nur Minderjährige.  
- Hinzufügen/Entfernen von Favoriten funktioniert korrekt.  
- Die Anwendung reagiert schnell und ohne merkbare Verzögerungen.  

---

## 4. Testkriterien definieren

### Aussetzungskriterien
- Kritische Fehler, die das Testen blockieren.  
- Ausfall der Testumgebung oder Ressourcenmangel.  

### Abnahmekriterien (Exit Criteria)
- Alle geplanten Testfälle wurden durchgeführt.  
- Ausführungsquote: mindestens **95 %** der Testfälle ausgeführt.  
- Bestehensquote: mindestens **90 %** der ausgeführten Testfälle bestanden.  
- Kritische und hochpriorisierte Fehler wurden behoben und geschlossen.  
- Keine offenen Fehler der Schwere 1 oder 2.  
- Performanzkennzahlen erfüllt.  
- Sicherheitsprobleme gelöst.  
- **UAT** abgeschlossen und freigegeben.  

---

## 5. Ressourcenplanung

**Personelle Ressourcen:**
- QA Engineer: **Felix Mönig**  
- Endanwender für UAT: **Felix Mönig**

**Hardware:**
- MacBook (Desktop)

**Software:**
- Browser: Chrome  
- Betriebssystem: macOS  
- Tools: GitHub für Testdokumentation  

**Infrastruktur:**
- Testumgebung: [https://grocerymate.masterschool.com/store/favs](https://grocerymate.masterschool.com/store/favs)  
- Automatisierungs-Tools: bisher keine, funktionale Tests manuell  

---

## 6. Testumgebung planen

**Testgeräte:**
- MacBook (Desktop)  
- Desktop-Browser: Chrome  

**Umgebungen:**
- Entwicklung (DEV)  
- Test (TEST)  
- Abnahme (ACC – Acceptance)  
- Produktion (PROD)  

**Zusätzliche Hinweise:**
- Tests manuell über Browser  
- Screenshots und Notizen dienen der Dokumentation  
- Keine automatisierten Tools aktuell, nur manuelle Durchführung  

---

## 7. Zeitplan und Aufwandsschätzung

| Aktivität | Startdatum | Enddatum | Umgebung | Verantwortlich | Geplanter Aufwand |
|------------|------------|-----------|------------|------------------|
| Testplanung | 03.11.2025 | 03.11.2025 | Alle | QA | 20 Stunden |
| Testfalldesign | 03.11.2025 | 03.11.2025 | Alle | QA | 60 Stunden |
| Funktionale Tests (Navigation, Suche, Login, Altersverifikation, Favoriten) | – | – | TEST | QA | 30 Stunden |
| Dokumentation der Testergebnisse | – | – | TEST | QA | 80 Stunden |
| Review und Abschlussbewertung | – | – | TEST | QA | 40 Stunden |
| Abnahmetest (UAT) | – | – | ACC | QA | 20 Stunden |

**Gesamter Aufwand:** ca. **250 Stunden**

---

## 8. Testartefakte (Test-Deliverables)

Folgende Dokumente und Ergebnisse werden im Rahmen des Testprozesses für GroceryMate erstellt und bereitgestellt:

- Testplandokument  
- Testfälle und Testskripte  
- Testdaten  
- Testberichte  
- Fehlerberichte  
- UAT-Freigabedokumentation (Sign-off)
