# Inflationsrechner für LibreOffice Calc

Ein praktisches Tool zur Berechnung inflationsangepasster Beträge für verschiedene Lohngruppen.

## Übersicht

Dieses Projekt bietet einen Inflationsrechner als LibreOffice Calc Spreadsheet, der Beträge basierend auf historischen und prognostizierten Inflationsraten anpasst.

## Features

- **Inflationsraten 2011-2025**: Historische Inflationsraten bereits eingetragen
- **Varianten für 2026-2030**: Separate Inflationsraten für verschiedene Lohngruppen
  - **SR+UR**: Lohngruppen 1, 2, 3, 6
  - **HR+GF+WD**: Lohngruppen 4, 5
- **Automatische Berechnung**: Eingabe von Basisjahr und Basisbetrag → sofortige Ergebnisse
- **Anpassbare Raten**: Alle Inflationsraten können individuell angepasst werden

## Verwendung

### Schritt 1: Datei öffnen

Öffnen Sie `Inflationsrechner.ods` mit LibreOffice Calc.

### Schritt 2: Daten eingeben

Im Sheet **"Rechner"**:
- **Zelle B3**: Geben Sie das Basisjahr ein (z.B. 2014)
- **Zelle B4**: Geben Sie den Basisbetrag in Euro ein (z.B. 400)

### Schritt 3: Ergebnisse ablesen

Die Ergebnisse werden automatisch berechnet:
- **Zelle B9**: Angepasster Betrag für SR+UR (LGrp 1,2,3,6)
- **Zelle B10**: Angepasster Betrag für HR+GF+WD (LGrp 4,5)

### Anpassen der Inflationsraten

1. **Historische Raten (2011-2025)**: Sheet **"Inflationsraten"**
   - Spalte A: Jahr
   - Spalte B: Inflationsrate in Prozent

2. **Zukunftsprognosen (2026-2030)**: Sheet **"Varianten"**
   - Spalte A: Jahr
   - Spalte B: SR+UR Rate in Prozent
   - Spalte C: HR+GF+WD Rate in Prozent

## Datei neu generieren

Falls Sie die `.ods`-Datei neu generieren möchten:

```bash
python3 create_inflationsrechner.py
```

## Struktur

```
Inflati/
├── Inflationsrechner.ods      # LibreOffice Calc Spreadsheet
├── create_inflationsrechner.py # Python-Script zur Generierung
└── README.md                   # Diese Datei
```

## Technische Details

Die `.ods`-Datei enthält 4 Sheets:
1. **Rechner**: Hauptansicht mit Eingabe und Ergebnissen
2. **Inflationsraten**: Historische Raten 2011-2025
3. **Varianten**: Separate Raten für verschiedene Lohngruppen 2026-2030
4. **Berechnungen**: Hilfsberechnungen (Multiplikationsfaktoren)

## Berechnungsmethode

Der Rechner berechnet den angepassten Betrag durch:
1. Multiplikation des Basisbetrags mit allen Inflationsfaktoren vom Basisjahr bis 2026
2. Für Jahre vor 2026: Verwendung historischer Raten
3. Für 2026 und später: Verwendung der jeweiligen Variantenraten (SR+UR oder HR+GF+WD)

**Formel**: `Angepasster Betrag = Basisbetrag × ∏(1 + Rate/100)`

## Lizenz

Frei verwendbar für private und kommerzielle Zwecke.
