# Militär Gehaltsrechner - Austrian Military Salary Calculator

Eine Android-Anwendung zur Berechnung von Gehältern für österreichisches Bundesheer-Personal basierend auf den Gehaltstabellen 2025.

## Features

- **Verwendungsgruppen-Auswahl**: M1 (Berufsoffiziere), M2 (Berufsunteroffiziere), M3 (Chargen)
- **Gehaltsstufen**: Stufen 1-8 für jede Verwendungsgruppe
- **Funktionszulagen**: F1-F5 mit jeweils 3 Funktionsstufen
- **Automatische Berechnung**: Grundgehalt + Funktionszulage = Gesamtgehalt
- **Benutzerfreundliche Oberfläche**: Grünes Theme passend zum Bundesheer

## Eingabefelder

Die App enthält alle vom Benutzer geforderten Eingabefelder:

1. **Verwendungsgruppe** - Auswahl der Grund- bzw. Vorrückungslaufbahn
2. **Gehaltsstufe** - Stufen 1-8
3. **Funktionsgruppe** - Auswahl der Funktionszulage (F1-F5 oder Keine)
4. **Funktionsstufe** - Stufen 1-3 (nur wenn Funktionsgruppe ausgewählt)

## Gehaltstabellen (Beispieldaten 2025)

### Verwendungsgruppe M1 (Berufsoffiziere)
- Stufe 1: € 2.850,50
- Stufe 2: € 3.125,80
- Stufe 3: € 3.425,30
- Stufe 4: € 3.750,90
- Stufe 5: € 4.105,20
- Stufe 6: € 4.485,70
- Stufe 7: € 4.895,40
- Stufe 8: € 5.335,80

### Verwendungsgruppe M2 (Berufsunteroffiziere)
- Stufe 1: € 2.350,60
- Stufe 2: € 2.585,40
- Stufe 3: € 2.845,70
- Stufe 4: € 3.125,30
- Stufe 5: € 3.425,90
- Stufe 6: € 3.750,50
- Stufe 7: € 4.095,80
- Stufe 8: € 4.465,20

### Verwendungsgruppe M3 (Chargen)
- Stufe 1: € 1.985,40
- Stufe 2: € 2.185,70
- Stufe 3: € 2.405,80
- Stufe 4: € 2.645,50
- Stufe 5: € 2.905,90
- Stufe 6: € 3.185,40
- Stufe 7: € 3.485,70
- Stufe 8: € 3.805,30

### Funktionszulagen
**F1 - Gruppenkommandant**: € 185,50 / € 225,80 / € 275,40
**F2 - Zugführer**: € 285,70 / € 345,90 / € 415,60
**F3 - Kompaniechef**: € 425,80 / € 515,40 / € 625,90
**F4 - Bataillonskommandant**: € 685,50 / € 825,70 / € 995,30
**F5 - Regimentskommandant**: € 985,60 / € 1.185,90 / € 1.425,40

## APK bauen

### Voraussetzungen
- Android Studio (neueste Version)
- JDK 8 oder höher
- Android SDK (API Level 33)

### Methode 1: Mit Android Studio (Empfohlen)

1. Öffnen Sie Android Studio
2. Wählen Sie "Open an Existing Project"
3. Navigieren Sie zum Projektordner und öffnen Sie ihn
4. Warten Sie, bis Gradle synchronisiert ist
5. Klicken Sie auf "Build" → "Build Bundle(s) / APK(s)" → "Build APK(s)"
6. Die APK wird erstellt in: `app/build/outputs/apk/debug/app-debug.apk`

### Methode 2: Mit Kommandozeile

```bash
# Navigieren Sie zum Projektverzeichnis
cd /pfad/zum/Inflati

# APK bauen (Debug-Version)
./gradlew assembleDebug

# APK bauen (Release-Version)
./gradlew assembleRelease
```

Die fertige APK finden Sie hier:
- Debug: `app/build/outputs/apk/debug/app-debug.apk`
- Release: `app/build/outputs/apk/release/app-release.apk`

### Methode 3: Online Build Service

Wenn Sie keinen lokalen Build durchführen können, können Sie Dienste wie:
- GitHub Actions
- Bitrise
- CircleCI

verwenden, um die APK automatisch zu erstellen.

## Installation auf Android-Gerät

1. Übertragen Sie die APK-Datei auf Ihr Android-Gerät
2. Öffnen Sie die APK-Datei
3. Erlauben Sie die Installation aus unbekannten Quellen (falls erforderlich)
4. Folgen Sie den Installationsanweisungen

## Projektstruktur

```
Inflati/
├── app/
│   ├── build.gradle                    # App-Level Gradle-Konfiguration
│   ├── proguard-rules.pro             # ProGuard-Regeln
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml    # App-Manifest
│           ├── java/at/bundesheer/gehalt/
│           │   └── MainActivity.java   # Haupt-Activity mit Berechnungslogik
│           └── res/
│               ├── layout/
│               │   └── activity_main.xml  # UI-Layout
│               ├── values/
│               │   ├── colors.xml      # Farbdefinitionen
│               │   ├── strings.xml     # String-Ressourcen
│               │   └── styles.xml      # App-Themes
│               ├── drawable/           # Icons und Grafiken
│               └── mipmap-*/           # Launcher-Icons
├── build.gradle                        # Projekt-Level Gradle
├── settings.gradle                     # Gradle-Einstellungen
├── gradle.properties                   # Gradle-Properties
└── gradlew                            # Gradle Wrapper (Unix)
```

## Anpassung der Gehaltstabellen

Um die Gehaltsdaten zu aktualisieren, bearbeiten Sie die Datei:
`app/src/main/java/at/bundesheer/gehalt/MainActivity.java`

In der Methode `initializeSalaryData()` können Sie die Werte anpassen:

```java
private void initializeSalaryData() {
    salaryData = new HashMap<>();

    // M1 - Berufsoffiziere anpassen
    Map<Integer, Double> m1Salaries = new HashMap<>();
    m1Salaries.put(1, 2850.50);  // Hier Werte ändern
    m1Salaries.put(2, 3125.80);
    // ... weitere Stufen
}
```

## Technische Details

- **Programmiersprache**: Java
- **Min SDK**: Android 5.0 (API Level 21)
- **Target SDK**: Android 13 (API Level 33)
- **Bibliotheken**:
  - AndroidX AppCompat
  - Material Design Components
  - CardView

## Datenquelle

Die Gehaltstabellen basieren auf:
- GÖD (Gewerkschaft Öffentlicher Dienst)
- Gehaltstabellen 2025 für militärischen Dienst
- § 85, § 89, § 91 GehG

**Hinweis**: Die in dieser App verwendeten Gehaltsdaten sind Beispielwerte. Für offizielle und aktuelle Gehaltsinformationen konsultieren Sie bitte die offiziellen Quellen unter:
- https://www.goed.at/themen/gehaltstabellen-2025/militaerischer-dienst

## Lizenz

Diese App wurde als Hilfswerkzeug erstellt und dient nur zu Informationszwecken. Die Gehaltsdaten sollten mit den offiziellen Quellen abgeglichen werden.

## Autor

Erstellt mit Claude Code für österreichisches Bundesheer-Personal

## Support

Bei Fragen oder Problemen öffnen Sie bitte ein Issue im GitHub-Repository.
