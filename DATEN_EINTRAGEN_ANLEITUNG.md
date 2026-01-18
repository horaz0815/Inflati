# ANLEITUNG ZUM EINTRAGEN DER OFFIZIELLEN GEHALTSDATEN 2025

## Schritt-für-Schritt Anleitung

### 1. Offizielle Daten beschaffen

Öffnen Sie eine dieser Quellen:
- https://www.goed.at/themen/gehaltstabellen-2025/militaerischer-dienst
- https://www.fsggoed.at/wp-content/uploads/sites/6/2024/11/Gehaltstabellen-2025.pdf

### 2. Datei öffnen

Öffnen Sie: `app/src/main/java/at/bundesheer/gehalt/MainActivity.java`

### 3. GRUNDGEHÄLTER eintragen

Suchen Sie die Methode `initializeSalaryData()` (ab Zeile 48)

#### M1 - Berufsoffiziere (Zeilen 55-77)
Tragen Sie die Werte für § 85 oder § 89 GehG ein:

```java
m1Salaries.put(1, ????.??);  // Stufe 1 - HIER WERT EINTRAGEN
m1Salaries.put(2, ????.??);  // Stufe 2 - HIER WERT EINTRAGEN
m1Salaries.put(3, ????.??);  // Stufe 3
m1Salaries.put(4, ????.??);  // Stufe 4
m1Salaries.put(5, ????.??);  // Stufe 5
m1Salaries.put(6, ????.??);  // Stufe 6
m1Salaries.put(7, ????.??);  // Stufe 7
m1Salaries.put(8, ????.??);  // Stufe 8
m1Salaries.put(9, ????.??);  // Stufe 9
m1Salaries.put(10, ????.??); // Stufe 10
m1Salaries.put(11, ????.??); // Stufe 11
m1Salaries.put(12, ????.??); // Stufe 12
m1Salaries.put(13, ????.??); // Stufe 13
m1Salaries.put(14, ????.??); // Stufe 14
m1Salaries.put(15, ????.??); // Stufe 15
m1Salaries.put(16, ????.??); // Stufe 16
m1Salaries.put(17, ????.??); // Stufe 17
m1Salaries.put(18, ????.??); // Stufe 18
m1Salaries.put(19, ????.??); // Stufe 19
m1Salaries.put(20, ????.??); // daz (kleine Dienstalterzulage)
m1Salaries.put(21, ????.??); // DAZ (große Dienstalterzulage)
```

#### M2 - Berufsunteroffiziere (Zeilen 80-102)
Analog zu M1 die Werte eintragen.

#### M3 - Chargen (Zeilen 105-127)
Analog zu M1 und M2 die Werte eintragen.

### 4. FUNKTIONSZULAGEN eintragen

Ab Zeile 133 finden Sie die Funktionszulagen.

#### MBO 1 - Offiziere (6 Funktionsgruppen × 4 Stufen)

Für JEDE Funktionsgruppe (1-6) die 4 Stufen eintragen:

```java
// MBO 1 - Funktionsgruppe 1
Map<Integer, Double> stufen = new HashMap<>();
stufen.put(1, ????.??); // FG 1, Stufe 1 - HIER WERT EINTRAGEN
stufen.put(2, ????.??); // FG 1, Stufe 2
stufen.put(3, ????.??); // FG 1, Stufe 3
stufen.put(4, ????.??); // FG 1, Stufe 4
mbo1.put(1, stufen);
```

Wiederholen Sie dies für:
- Funktionsgruppen 2, 3, 4, 5, 6 (jeweils 4 Stufen)

#### MBO 2 - Offiziere (9 Funktionsgruppen × 4 Stufen)

Für JEDE Funktionsgruppe (1-9) die 4 Stufen eintragen.

#### MUO 1 - Unteroffiziere (7 Funktionsgruppen × 4 Stufen)

Für JEDE Funktionsgruppe (1-7) die 4 Stufen eintragen.

## ZUSAMMENFASSUNG: Wie viele Werte müssen eingetragen werden?

### Grundgehälter:
- M1: 21 Werte (Stufen 1-19 + daz + DAZ)
- M2: 21 Werte
- M3: 21 Werte
**Summe Grundgehälter: 63 Werte**

### Funktionszulagen:
- MBO 1: 6 Gruppen × 4 Stufen = 24 Werte
- MBO 2: 9 Gruppen × 4 Stufen = 36 Werte
- MUO 1: 7 Gruppen × 4 Stufen = 28 Werte
**Summe Funktionszulagen: 88 Werte**

### GESAMT: 151 Werte

## ALTERNATIVE: Code-Generator

Wenn Sie die Daten in einer strukturierten Form haben (z.B. Excel, CSV),
kann ich Ihnen ein Python-Script erstellen, das automatisch den Java-Code generiert.

## Nach dem Eintragen

1. Speichern Sie die Datei
2. Pushen Sie zu GitHub:
   ```bash
   git add app/src/main/java/at/bundesheer/gehalt/MainActivity.java
   git commit -m "Add official 2025 salary data"
   git push origin claude/military-salary-calculator-IvL1h
   ```
3. GitHub Actions baut automatisch eine neue APK mit den echten Daten!

## Benötigen Sie Hilfe?

Wenn Sie mir die Daten zur Verfügung stellen können (als Text, Screenshot, oder
beschreiben welche Werte Sie haben), kann ich sie für Sie eintragen!
