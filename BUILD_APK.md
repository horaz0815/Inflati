# APK Build-Anleitung für Android

Diese Anleitung zeigt Ihnen, wie Sie eine Test-APK für Ihr Android-Smartphone erstellen.

## Voraussetzungen

- Node.js installiert
- Expo Account (kostenlos)
- Internet-Verbindung

## Methode 1: EAS Build (Empfohlen - Cloud Build)

### Schritt 1: EAS CLI installieren

```bash
npm install -g eas-cli
```

### Schritt 2: Bei Expo anmelden

```bash
eas login
```

Wenn Sie noch keinen Account haben:
1. Gehen Sie zu https://expo.dev/signup
2. Erstellen Sie einen kostenlosen Account
3. Führen Sie `eas login` erneut aus

### Schritt 3: Projekt konfigurieren

```bash
# Im Projektverzeichnis
eas build:configure
```

Wählen Sie:
- Platform: **Android** (mit Leertaste auswählen)
- Drücken Sie Enter

### Schritt 4: Assets erstellen (WICHTIG!)

Die App benötigt Icon- und Splash-Screen-Dateien. Sie haben zwei Optionen:

#### Option A: Schnelle Platzhalter (für Tests)

```bash
# Erstellen Sie den assets Ordner
mkdir -p assets

# Download einfacher Platzhalter (benötigt curl)
# Icon (1024x1024)
curl -o assets/icon.png "https://via.placeholder.com/1024x1024/2C3E2F/8B7355?text=Speiseplan"

# Splash Screen (1284x2778)
curl -o assets/splash.png "https://via.placeholder.com/1284x2778/2C3E2F/8B7355?text=Speiseplan"

# Adaptive Icon (1024x1024)
curl -o assets/adaptive-icon.png "https://via.placeholder.com/1024x1024/2C3E2F/8B7355?text=S"

# Favicon (48x48)
curl -o assets/favicon.png "https://via.placeholder.com/48x48/2C3E2F/8B7355?text=S"
```

#### Option B: Eigene Icons erstellen

Erstellen Sie diese Dateien im `assets/` Ordner:
- `icon.png` (1024x1024 px)
- `splash.png` (1284x2778 px)
- `adaptive-icon.png` (1024x1024 px)
- `favicon.png` (48x48 px)

Tools: Photoshop, GIMP, Figma, Canva, oder Online-Generatoren

### Schritt 5: APK bauen

```bash
# Preview Build (zum Testen)
eas build --platform android --profile preview
```

**Was passiert jetzt:**
1. Ihr Code wird zu Expo-Servern hochgeladen
2. Die APK wird in der Cloud gebaut (5-15 Minuten)
3. Sie erhalten einen Download-Link

### Schritt 6: APK herunterladen

Nach dem Build-Prozess:
1. Sie erhalten einen Download-Link im Terminal
2. **ODER** gehen Sie zu https://expo.dev/accounts/[IHR_USERNAME]/projects/speiseplan-app/builds
3. Klicken Sie auf den neuesten Build
4. Laden Sie die APK herunter

### Schritt 7: APK installieren

**Auf dem Smartphone:**
1. Laden Sie die APK-Datei auf Ihr Android-Smartphone
2. Öffnen Sie die APK-Datei
3. Erlauben Sie "Installation aus unbekannten Quellen" (falls gefragt)
4. Installieren Sie die App

**WICHTIG:** Denken Sie daran, Firebase zu konfigurieren, bevor Sie die App verwenden!

## Methode 2: Lokaler Build mit Expo (Schneller für Development)

### Für lokales Testen OHNE APK-Datei:

```bash
# Dependencies installieren
npm install

# App starten
npm start

# Dann auf Ihrem Smartphone:
# 1. Expo Go App installieren
# 2. QR-Code scannen
# 3. App öffnet sich sofort
```

Dies ist **viel schneller** für Tests, aber die App läuft innerhalb von Expo Go.

## Methode 3: Development Build (Standalone App mit Live-Updates)

Für eine standalone App, die sich wie eine echte App anfühlt, aber schnelle Updates ermöglicht:

```bash
# Development Build erstellen
eas build --profile development --platform android

# Nach Installation auf dem Gerät:
npm start --dev-client
```

## Troubleshooting

### Problem: "Assets not found"

**Lösung:** Stellen Sie sicher, dass alle Assets im `assets/` Ordner vorhanden sind:
```bash
ls -la assets/
# Sollte zeigen: icon.png, splash.png, adaptive-icon.png, favicon.png
```

### Problem: "Build failed" wegen Firebase

**Lösung:** Firebase-Konfiguration ist optional für den ersten Test-Build. Die App wird gebaut, aber Firebase-Features funktionieren erst nach Konfiguration.

### Problem: "Package name already in use"

**Lösung:** Ändern Sie in `app.json` die Package-ID:
```json
"android": {
  "package": "com.IHR_NAME.speiseplan"
}
```

### Problem: "expo-ads-admob" Build-Fehler

**Lösung:** AdMob kann Probleme verursachen. Entfernen Sie es temporär aus `package.json`:
1. Öffnen Sie `package.json`
2. Entfernen Sie die Zeile `"expo-ads-admob": "~13.0.0",`
3. Führen Sie `npm install` erneut aus

## Build-Profile Übersicht

Die `eas.json` enthält drei Profile:

### 1. **preview** (Empfohlen für Tests)
- Erstellt APK-Datei
- Schneller Build
- Perfekt zum Testen auf echten Geräten
```bash
eas build --platform android --profile preview
```

### 2. **development**
- Mit Entwickler-Tools
- Hot Reloading
- Für aktive Entwicklung
```bash
eas build --platform android --profile development
```

### 3. **production**
- Optimiert und minimiert
- Für App Store Veröffentlichung
- Größere Build-Zeit
```bash
eas build --platform android --profile production
```

## Build-Kosten

**Expo EAS Build:**
- Kostenloser Plan: **30 Builds/Monat** (Android + iOS kombiniert)
- Ausreichend für Tests und kleine Projekte
- Upgrades verfügbar bei Bedarf

## Alternative: Lokaler Build mit Android Studio

Falls Sie EAS Build nicht nutzen möchten:

1. Installieren Sie Android Studio
2. Installieren Sie Java JDK
3. Konfigurieren Sie Android SDK
4. Führen Sie aus:
```bash
npx expo run:android
```

**Hinweis:** Deutlich komplexer und erfordert mehr Setup!

## Nach dem Build

### App testen:
1. Installieren Sie die APK auf Ihrem Smartphone
2. **WICHTIG:** Konfigurieren Sie Firebase (siehe `FIREBASE_SETUP.md`)
3. Öffnen Sie die App
4. Testen Sie alle Features

### Was funktioniert OHNE Firebase:
- UI und Design
- Navigation
- Kamera-Auswahl (aber kein Upload)

### Was BENÖTIGT Firebase:
- Admin-Login
- Speiseplan-Upload
- Speiseplan-Anzeige
- Datenspeicherung

## Nächste Schritte

1. **APK gebaut?** ✅
2. **Firebase einrichten** → Siehe `FIREBASE_SETUP.md`
3. **App testen** → Siehe `QUICKSTART.md`
4. **Production Build** → Für App Store Veröffentlichung

## Hilfreiche Links

- **EAS Build Dokumentation**: https://docs.expo.dev/build/introduction/
- **Expo Dashboard**: https://expo.dev/
- **EAS Build Status**: https://expo.dev/accounts/[USERNAME]/builds
- **Troubleshooting Guide**: https://docs.expo.dev/build-reference/troubleshooting/

## QR-Code für Build-Download

Nach dem Build erhalten Sie einen QR-Code, den Sie mit Ihrem Smartphone scannen können, um die APK direkt herunterzuladen!

---

**Viel Erfolg beim Build!** 📱🚀

Bei Problemen:
1. Überprüfen Sie die Build-Logs
2. Stellen Sie sicher, dass alle Assets vorhanden sind
3. Prüfen Sie die `eas.json` Konfiguration
