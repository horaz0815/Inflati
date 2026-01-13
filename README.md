# KIOWA Flottensteuerung V47

🚁 **Professionelles Flottenmanagement-System für LibreOffice Calc**

Ein umfassendes System zur lückenlosen Überwachung von Zellen-Stunden (LSN), Triebwerks-Stunden (TW-LSN), Wartungsintervallen und Kraftstoff-Logistik für Luftfahrzeuge.

## 📋 Inhaltsverzeichnis

- [System-Übersicht](#system-übersicht)
- [Flotte](#flotte)
- [Installation](#installation)
- [Blattstruktur](#blattstruktur)
- [Verwendung](#verwendung)
- [Technische Details](#technische-details)

---

## 🎯 System-Übersicht

Das KIOWA-System bietet:

- ✅ Lückenlose Überwachung von Flugstunden (Zelle und Triebwerk)
- ✅ Automatische Wartungsintervall-Berechnung
- ✅ Kraftstoff-Logistik (Inland/Ausland)
- ✅ Landungen und Triebwerks-Cycles Tracking
- ✅ Zentrale Kommandozentrale (OVERVIEW)
- ✅ Statistische Auswertungen pro Monat/Jahr
- ✅ Wartungsplanung mit Kalenderwochen

---

## ✈️ Flotte

**Aktive Flotte (12 Einheiten):**

- 3C-OA, 3C-OB, 3C-OC, 3C-OD, 3C-OE
- 3C-OH, 3C-OI, 3C-OJ, 3C-OK, 3C-OL
- RES1, RES2 (Reserveplätze)

> **Hinweis:** Die Kennungen 3C-OF und 3C-OG wurden systemweit entfernt und existieren in keiner Liste oder Formel.

---

## 🚀 Installation

### Voraussetzungen

- LibreOffice Calc (Version 6.0 oder höher)
- Python 3.6+ (nur für Neugenerierung)

### Verwendung

1. Öffnen Sie `KIOWA_V47.ods` mit LibreOffice Calc
2. Das System ist sofort einsatzbereit

### Datei neu generieren

Falls Sie die Datei neu generieren möchten:

```bash
python3 create_kiowa.py
```

---

## 📊 Blattstruktur

### 1. Einzelblätter (Logbücher)

**12 Blätter:** `3C-OA`, `3C-OB`, ..., `RES1`, `RES2`

Jedes Blatt dient als Primärquelle für alle Flugdaten eines Luftfahrzeugs.

#### Spalten-Struktur

| Spalte | Bezeichnung | Beschreibung |
|--------|-------------|--------------|
| **A** | Monat | Monatsbezeichnung (Januar-Dezember) |
| **B** | Tag | Tag (1-31, jahresunabhängig) |
| **C** | HH | Flugzeit Stunden |
| **D** | MM | Flugzeit Minuten |
| **E** | LDG | Anzahl Landungen |
| **F** | CYC | Triebwerks-Cycles |
| **G** | Fuel-INL | Kraftstoff Inland (Liter) |
| **H** | Fuel-AUSL | Kraftstoff Ausland (Liter) |
| **I** | REMARKS | Bemerkungen (Freitext) |
| **L** | Zellen-LSN HH | Zellenstunden (kumuliert) |
| **M** | Zellen-LSN MM | Zellenminuten (kumuliert) |
| **N** | TW-LSN HH | Triebwerksstunden (kumuliert) |
| **O** | TW-LSN MM | Triebwerksminuten (kumuliert) |
| **P** | TW-CORR HH | Korrektur Stunden (Triebwerkstausch) |
| **Q** | TW-CORR MM | Korrektur Minuten (Triebwerkstausch) |

#### Spezialzeilen

- **Zeile 2 (ÜBERTRAG):** Manuelle Eingabe des Vorjahres-Übertrags
- **Zeile 3 (SUMME):** Automatische Berechnung aller Werte inkl. Übertrag
- **Zeilen 4-369:** Tageseinträge für alle 365 Tage

#### HH:MM Logik

Alle Zeitberechnungen verwenden die 60-Minuten-Übertragsregel:

```
Stunden = Basis_HH + INT(Minuten/60)
Minuten = MOD(Basis_MM; 60)
```

**Beispiel:**
- 5 Stunden 75 Minuten = 6 Stunden 15 Minuten

---

### 2. STATISTIK

**Monatliche und jährliche Aggregation aller Flugdaten.**

#### Struktur (8-Zeilen-Block pro Maschine)

1. Flugzeit HH
2. Flugzeit MM
3. Landungen
4. Cycles
5. Fuel-INL
6. Fuel-AUSL
7. TW-LSN (Stand Monatsende)
8. *(Leerzeile)*

Am Ende: **FLOTTEN-GESAMTSUMME** über alle 12 Maschinen.

---

### 3. OVERVIEW

**Die zentrale Kommandozentrale für den täglichen Betrieb.**

#### Spalten

| Spalte | Bezeichnung | Beschreibung |
|--------|-------------|--------------|
| 1 | Kennzeichen | Flugzeug-ID (OA-OL, RES) |
| 2 | Flugklarheit | Dropdown: VB, BEB, VUB |
| 3 | BDL | Auto-Eintrag "BDL" bei >14 Tage Inaktivität |
| 4 | KONFIG | Konfiguration (Platzhalter) |
| 5 | Standort | Manuell: Aktueller Standort |
| 6 | LSN IST | Aktueller Zellenstand (HH:MM) |
| 7 | TW-LSN IST | Aktueller TW-Stand (HH:MM) |
| 8 | Steuerung offen (Aktuell) | Soll - Ist aktueller Monat |
| 9 | Steuerung offen (Nächstes) | Soll - Ist nächster Monat |
| 10 | COUNTDOWN WE | Stunden bis nächster Werft-Check |
| 11 | ANMERKUNGEN | Freitext |
| 12 | Wartung (Stunden) | Stunden bis nächste Wartung |
| 13 | Wartung (Planung) | Geplante Wartung (KW) |

---

### 4. STEUERUNG

**Definition der Vortragswerte und monatlichen Soll-Flugstunden.**

#### Spalten

- Kennzeichen
- Vortrag Zelle HH/MM
- Vortrag TW HH/MM
- Monatssoll Januar - Dezember (12 Spalten)

---

### 5. WARTUNGEN

**Wartungsintervall-Berechnung in 25h-Schritten bis 12.000 Stunden.**

#### Wartungstypen

- **25WE** - 25-Stunden-Wartung
- **50WE** - 50-Stunden-Wartung
- **75WE** - 75-Stunden-Wartung
- **100WE** - 100-Stunden-Wartung
- **300WE** - 300-Stunden-Wartung
- **1200WE** - 1200-Stunden-Wartung

Für jede Maschine wird die Differenz zum nächsten Check berechnet.

---

### 6. WE KW

**Terminplanung: Zuordnung von Wartungsereignissen zu Kalenderwochen.**

#### Spalten

- KW (Kalenderwoche 1-53)
- Kennzeichen
- Wartungstyp
- LSN Soll
- Bemerkungen

---

## 🔧 Verwendung

### Täglicher Betrieb

1. **Flugdaten eintragen** (in Einzelblättern):
   - Öffnen Sie das Blatt des entsprechenden Flugzeugs (z.B. `3C-OA`)
   - Suchen Sie die Zeile mit dem aktuellen Datum
   - Tragen Sie ein:
     - C/D: Flugzeit (HH:MM)
     - E: Landungen
     - F: Cycles
     - G/H: Kraftstoff (Inland/Ausland)
     - I: Bemerkungen

2. **Überblick prüfen** (OVERVIEW):
   - Wechseln Sie zum `OVERVIEW`-Blatt
   - Prüfen Sie LSN/TW-LSN IST-Stände
   - Beachten Sie BDL-Warnungen
   - Überprüfen Sie COUNTDOWN WE

3. **Statistiken** (STATISTIK):
   - Monatliche Auswertungen werden automatisch berechnet
   - Flotten-Gesamtsummen am Ende

### Jahreswechsel

1. Notieren Sie die Werte aus Zeile 3 (SUMME) jedes Einzelblatts
2. Tragen Sie diese in Zeile 2 (ÜBERTRAG) des neuen Jahres ein
3. Die Berechnungen erfolgen automatisch

### Triebwerkstausch

Bei einem Triebwerkstausch:

1. Öffnen Sie das entsprechende Einzelblatt
2. Tragen Sie die Korrekturwerte in Spalten **P** (HH) und **Q** (MM) ein
3. Die TW-LSN wird automatisch angepasst

---

## ⚙️ Technische Details

### Formeln

#### Zellen-LSN Berechnung (Zeile 3)

```
HH: =L2 + SUM(C4:C369) + INT((M2 + SUM(D4:D369))/60)
MM: =MOD(M2 + SUM(D4:D369); 60)
```

#### TW-LSN Berechnung (mit Korrektur)

```
HH: =N2 + SUM(C4:C369) + INT((O2 + SUM(D4:D369))/60) + P2 + INT((O2 + Q2)/60)
MM: =MOD(O2 + SUM(D4:D369) + Q2; 60)
```

#### Tägliche LSN (fortlaufend)

```
HH: =IF(C{row}=""; ""; L2 + SUM(C$4:C{row}) + INT((M2 + SUM(D$4:D{row}))/60))
MM: =IF(C{row}=""; ""; MOD(M2 + SUM(D$4:D{row}); 60))
```

### Datenstruktur

- **365 Zeilen** pro Einzelblatt (jahresunabhängig, kein Schaltjahr)
- **Automatische Berechnung** bei jeder Eingabe
- **Referenzierung** zwischen Blättern für OVERVIEW und STATISTIK

---

## 📁 Projektstruktur

```
KIOWA/
├── KIOWA_V47.ods          # Haupt-Spreadsheet
├── create_kiowa.py        # Python-Generator
└── README.md              # Diese Datei
```

---

## 🛠️ Anpassungen

### Neue Maschine hinzufügen

1. Editieren Sie `create_kiowa.py`
2. Fügen Sie das Kennzeichen zu `FLEET` hinzu
3. Generieren Sie die Datei neu: `python3 create_kiowa.py`

### Wartungsintervalle anpassen

Im Blatt `WARTUNGEN` können Sie die Intervalle manuell anpassen.

---

## 📝 System-Regeln

1. **HH:MM Logik:** Alle Zeitberechnungen erfolgen über INT() und MOD()-Funktionen
2. **Keine negativen Werte:** Korrekturen erfolgen über TW-CORR
3. **Jahresunabhängig:** Das System funktioniert für jedes Jahr (365 Tage)
4. **Zentrale Datenquelle:** Einzelblätter sind die Primärquelle, alle anderen Blätter referenzieren darauf

---

## 🎓 Tipps & Best Practices

- **Regelmäßige Backups:** Sichern Sie die Datei täglich
- **Konsistente Eingabe:** Tragen Sie Daten zeitnah ein
- **Überprüfung:** Nutzen Sie OVERVIEW für tägliche Kontrollen
- **BDL-Warnung:** Achten Sie auf Bodenlauf-Anforderungen (>14 Tage Inaktivität)
- **Wartungsplanung:** Planen Sie Wartungen frühzeitig im WE KW-Blatt

---

## 📞 Support

Bei Fragen oder Problemen:
1. Überprüfen Sie die Formeln in Zeile 3 der Einzelblätter
2. Stellen Sie sicher, dass Vortragswerte korrekt eingetragen sind
3. Regenerieren Sie die Datei bei Strukturproblemen

---

## 📜 Version

**KIOWA V47** - Flottensteuerung für LibreOffice Calc
Erstellt: Januar 2026

---

## ⚖️ Lizenz

Frei verwendbar für private und kommerzielle Zwecke.

---

**🚁 Gute Flüge!**
