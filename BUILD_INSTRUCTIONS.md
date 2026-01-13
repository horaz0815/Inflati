# APK Build Anleitung

## Option 1: Mit Android Studio (Empfohlen)

### Schritt 1: Projekt öffnen
1. Android Studio starten
2. "Open an existing project" wählen
3. Den Ordner "Inflati" auswählen
4. Warten, bis Gradle synchronisiert ist

### Schritt 2: APK erstellen
1. In der Menüleiste: **Build → Build Bundle(s) / APK(s) → Build APK(s)**
2. Warten, bis der Build abgeschlossen ist
3. Klicken Sie auf "locate" in der Benachrichtigung

**APK-Speicherort**: `app/build/outputs/apk/debug/app-debug.apk`

### Schritt 3: APK installieren
- Kopieren Sie die APK auf Ihr Android-Gerät
- Öffnen Sie die Datei und installieren Sie die App
- Möglicherweise müssen Sie "Installation aus unbekannten Quellen" aktivieren

## Option 2: Mit Kommandozeile

### Voraussetzungen
- Android SDK installiert
- ANDROID_HOME Umgebungsvariable gesetzt
- Java JDK 17 installiert

### Build-Befehle

```bash
# Im Projektverzeichnis
cd /home/user/Inflati

# Debug APK erstellen
./gradlew assembleDebug

# Die APK finden Sie hier:
# app/build/outputs/apk/debug/app-debug.apk
```

### Release APK erstellen (für Produktion)

```bash
# Release APK erstellen
./gradlew assembleRelease

# Die APK finden Sie hier:
# app/build/outputs/apk/release/app-release.apk
```

**Hinweis**: Für eine Release-APK benötigen Sie einen Keystore zum Signieren der App.

## Option 3: Online Build (ohne lokale Installation)

Sie können auch Online-Dienste wie **GitHub Actions** verwenden:

1. Pushen Sie den Code zu GitHub (bereits erledigt ✓)
2. Erstellen Sie eine GitHub Actions Workflow-Datei
3. GitHub baut die APK automatisch

Siehe: `.github/workflows/build.yml` (falls vorhanden)

## APK-Dateigröße

Die erwartete Größe der Debug-APK: **~15-20 MB**
(inkl. iText PDF-Bibliothek)

## Troubleshooting

### Gradle Sync schlägt fehl
```bash
# Gradle Cache löschen
./gradlew clean

# Gradle neu synchronisieren
./gradlew --refresh-dependencies
```

### Build-Fehler wegen Android SDK
Stellen Sie sicher, dass Android SDK installiert ist:
- Über Android Studio: Tools → SDK Manager
- Benötigte SDK: API Level 34 (Android 14)

### Java Version Probleme
Projekt benötigt Java 17:
```bash
# Java Version prüfen
java -version

# Sollte zeigen: java version "17.x.x"
```

## APK auf Gerät installieren

### Per USB (ADB)
```bash
# Gerät verbinden und USB-Debugging aktivieren
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Per E-Mail/Cloud
1. APK per E-Mail an sich selbst senden
2. Auf Android-Gerät öffnen
3. "Installation aus unbekannten Quellen" erlauben
4. Installieren

### Per QR-Code
1. APK auf einen Webserver hochladen
2. QR-Code für Download-Link generieren
3. Mit Android-Gerät scannen und installieren

## Schnellstart für Entwickler

```bash
# 1. Repository klonen
git clone <repository-url>
cd Inflati

# 2. Android Studio öffnen
# Datei → Öffnen → Inflati-Ordner wählen

# 3. Warten bis Gradle Sync abgeschlossen ist

# 4. Build → Build APK(s)

# 5. Fertig! 🎉
```

## Support

Bei Problemen:
1. Prüfen Sie die Gradle-Logs
2. Stellen Sie sicher, dass Android SDK installiert ist
3. Überprüfen Sie die Java-Version (Java 17 erforderlich)
