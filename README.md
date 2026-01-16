# Speiseplan App

[![Build APK](https://github.com/horaz0815/Inflati/actions/workflows/build-apk.yml/badge.svg)](https://github.com/horaz0815/Inflati/actions/workflows/build-apk.yml)
[![Release APK](https://github.com/horaz0815/Inflati/actions/workflows/release-apk.yml/badge.svg)](https://github.com/horaz0815/Inflati/actions/workflows/release-apk.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Eine moderne Cross-Platform Mobile App für Android und iOS zur Anzeige von wöchentlichen Speiseplänen mit militärischem Design.

## 🚀 Quick Start

### APK direkt herunterladen
- **[Neuester Release](https://github.com/horaz0815/Inflati/releases/latest)** - APK für Android
- **[Alle Releases](https://github.com/horaz0815/Inflati/releases)** - Versionshistorie

### APK selbst bauen
- **[Lokaler Build](./JETZT_APK_BAUEN.md)** - APK auf Ihrem Computer bauen
- **[GitHub Actions Build](./GITHUB_APK_SCHNELLSTART.md)** - APK automatisch auf GitHub bauen
- **[Expo Go Test](./EXPO_GO_ANLEITUNG.md)** - Sofort testen ohne Build

### Setup & Konfiguration
- **[Firebase Setup](./FIREBASE_SETUP.md)** - Backend konfigurieren (erforderlich!)
- **[Schnellstart Guide](./QUICKSTART.md)** - In 5 Minuten loslegen

## Features

- 📅 **Wochenansicht**: Speisepläne werden pro Kalenderwoche angezeigt
- 📸 **Kamera-Upload**: Admin-Bereich zum Hochladen von Speiseplänen per Kamera
- 🔒 **Authentifizierung**: Sicherer Admin-Bereich mit Firebase Authentication
- 💰 **Monetarisierung**: Google AdMob Integration für Werbeeinnahmen
- 🎨 **Militärisches Design**: Modernes, dunkles UI mit militärischen Farben (Olivgrün, Grau)
- 📱 **Cross-Platform**: Läuft auf Android und iOS
- ☁️ **Cloud-Backend**: Firebase Firestore für Daten, Firebase Storage für Bilder

## Technologie-Stack

- **Framework**: React Native mit Expo
- **Navigation**: React Navigation
- **Backend**: Firebase (Firestore, Storage, Authentication)
- **Monetarisierung**: Google AdMob
- **Kamera**: Expo Image Picker & Expo Camera
- **UI**: React Native, Expo Linear Gradient

## Voraussetzungen

- Node.js (v16 oder höher)
- npm oder yarn
- Expo CLI
- Ein Firebase-Projekt
- Ein Google AdMob-Konto (optional für Werbung)

## Installation

### 1. Repository klonen und Dependencies installieren

```bash
git clone <repository-url>
cd Inflati
npm install
```

### 2. Firebase einrichten

#### a) Firebase-Projekt erstellen

1. Gehen Sie zu [Firebase Console](https://console.firebase.google.com/)
2. Erstellen Sie ein neues Projekt
3. Aktivieren Sie die folgenden Services:
   - **Authentication** (Email/Password Provider aktivieren)
   - **Firestore Database**
   - **Storage**

#### b) Firebase-Konfiguration

1. Gehen Sie zu Projekteinstellungen → Ihre Apps
2. Erstellen Sie eine Web-App
3. Kopieren Sie die Firebase-Konfiguration
4. Öffnen Sie `firebase.config.js` und ersetzen Sie die Platzhalter:

```javascript
const firebaseConfig = {
  apiKey: "IHR_API_KEY",
  authDomain: "ihr-projekt.firebaseapp.com",
  projectId: "ihr-projekt-id",
  storageBucket: "ihr-projekt.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef123456"
};
```

#### c) Firestore Security Rules

Gehen Sie zu Firestore → Rules und verwenden Sie:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /mealPlans/{document} {
      // Alle können lesen
      allow read: if true;
      // Nur authentifizierte Benutzer können schreiben
      allow write: if request.auth != null;
    }
  }
}
```

#### d) Storage Security Rules

Gehen Sie zu Storage → Rules und verwenden Sie:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /mealplans/{allPaths=**} {
      // Alle können lesen
      allow read: if true;
      // Nur authentifizierte Benutzer können schreiben
      allow write: if request.auth != null;
    }
  }
}
```

#### e) Admin-Benutzer erstellen

1. Gehen Sie zu Authentication → Users
2. Klicken Sie auf "Add user"
3. Erstellen Sie einen Benutzer mit Email und Passwort
4. Diese Zugangsdaten verwenden Sie später für den Admin-Login

### 3. Google AdMob einrichten (Optional)

#### a) AdMob-Konto erstellen

1. Gehen Sie zu [Google AdMob](https://admob.google.com/)
2. Erstellen Sie ein Konto
3. Fügen Sie eine App hinzu (für Android und iOS)

#### b) Banner Ad-Einheit erstellen

1. Erstellen Sie eine Banner-Ad-Einheit für jede Plattform
2. Kopieren Sie die Ad-Unit IDs

#### c) AdMob in der App konfigurieren

1. Öffnen Sie `components/AdBanner.js`
2. Entfernen Sie die Kommentare bei der echten Implementierung
3. Ersetzen Sie die Platzhalter-IDs mit Ihren AdMob-IDs:

```javascript
const ADMOB_BANNER_ID = Platform.select({
  ios: 'ca-app-pub-xxxxxxxxxxxxx/yyyyyyyyyy',
  android: 'ca-app-pub-xxxxxxxxxxxxx/yyyyyyyyyy',
});
```

### 4. App Assets erstellen

Erstellen Sie folgende Dateien im `assets`-Verzeichnis:

- `icon.png` (1024x1024 px) - App-Icon
- `splash.png` (1284x2778 px) - Splash-Screen
- `adaptive-icon.png` (1024x1024 px) - Android Adaptive Icon
- `favicon.png` (48x48 px) - Web Favicon

Tipp: Verwenden Sie Online-Tools wie [App Icon Generator](https://www.appicon.co/) oder erstellen Sie eigene Bilder mit militärischem Design (Olivgrün #2C3E2F als Hintergrund).

## App starten

### Entwicklungsmodus

```bash
# Expo Dev Server starten
npm start

# oder direkt auf Android
npm run android

# oder direkt auf iOS
npm run ios
```

### QR-Code scannen

1. Installieren Sie die Expo Go App auf Ihrem Smartphone:
   - [Android](https://play.google.com/store/apps/details?id=host.exp.exponent)
   - [iOS](https://apps.apple.com/app/expo-go/id982107779)

2. Scannen Sie den QR-Code, der im Terminal erscheint

## Verwendung

### Für Endbenutzer

1. **Speiseplan ansehen**:
   - App öffnen
   - Aktuelle Kalenderwoche wird automatisch angezeigt
   - Mit Pfeiltasten zwischen Wochen navigieren

2. **Werbung**:
   - Werbebanner erscheinen am unteren Bildschirmrand
   - Unterstützen Sie die App durch Ansehen der Werbung

### Für Administratoren

1. **Anmelden**:
   - Klicken Sie auf das Zahnrad-Symbol (⚙️)
   - Geben Sie Admin-Email und Passwort ein
   - Klicken Sie auf "ANMELDEN"

2. **Speiseplan hochladen**:
   - Klicken Sie auf "Speiseplan hochladen"
   - Wählen Sie "Kamera" oder "Galerie"
   - Machen Sie ein Foto des Speiseplans oder wählen Sie ein vorhandenes aus
   - Überprüfen Sie Woche und Jahr (automatisch vorausgefüllt)
   - Optional: Fügen Sie Hinweise hinzu
   - Klicken Sie auf "HOCHLADEN"

3. **Abmelden**:
   - Gehen Sie zurück zum Admin-Panel
   - Klicken Sie auf "Abmelden"

## Projektstruktur

```
Inflati/
├── App.js                          # Haupt-App-Datei mit Navigation
├── app.json                        # Expo-Konfiguration
├── babel.config.js                 # Babel-Konfiguration
├── firebase.config.js              # Firebase-Konfiguration
├── theme.js                        # Militärisches Design-Theme
├── package.json                    # Dependencies
│
├── screens/                        # App-Bildschirme
│   ├── HomeScreen.js              # Hauptbildschirm mit Speiseplan
│   ├── AdminScreen.js             # Admin-Login und Panel
│   └── UploadMealPlanScreen.js    # Speiseplan-Upload
│
├── components/                     # Wiederverwendbare Komponenten
│   └── AdBanner.js                # Google AdMob Banner
│
└── assets/                         # Bilder und Icons
    ├── icon.png
    ├── splash.png
    ├── adaptive-icon.png
    └── favicon.png
```

## Build für Production

### Android APK erstellen

```bash
# EAS Build installieren (einmalig)
npm install -g eas-cli

# Bei Expo anmelden
eas login

# Projekt konfigurieren
eas build:configure

# Android Build erstellen
eas build --platform android
```

### iOS Build erstellen

```bash
# iOS Build erstellen (benötigt Apple Developer Account)
eas build --platform ios
```

### App in Stores veröffentlichen

1. **Google Play Store**:
   - Erstellen Sie ein Developer-Konto ($25 einmalig)
   - Laden Sie die APK/AAB hoch
   - Füllen Sie Store-Listing aus
   - Reichen Sie zur Überprüfung ein

2. **Apple App Store**:
   - Erstellen Sie ein Developer-Konto ($99/Jahr)
   - Laden Sie die IPA hoch
   - Füllen Sie Store-Listing aus
   - Reichen Sie zur Überprüfung ein

## Design-Konzept

### Farbschema (Militärisch)

- **Primär**: Olivgrün (#3C5233, #2C3E2F)
- **Sekundär**: Militärgrau (#5C6B5C)
- **Akzent**: Sandbraun (#8B7355)
- **Hintergrund**: Sehr dunkles Grün (#1A1F1A)
- **Text**: Helles Grau (#E8E8E8)

### UI-Elemente

- Dunkles Theme mit hohem Kontrast
- Kantige Borders mit militärischem Look
- Klare Typografie mit großem Lettertracking
- Funktionale, minimalistische Icons

## Troubleshooting

### Firebase-Fehler

**Problem**: "Firebase: Error (auth/wrong-password)"
- **Lösung**: Überprüfen Sie Email und Passwort

**Problem**: "Firebase: Error (auth/network-request-failed)"
- **Lösung**: Überprüfen Sie Ihre Internetverbindung

### Kamera funktioniert nicht

**Problem**: Kamera öffnet sich nicht
- **Lösung**: Stellen Sie sicher, dass Kamera-Berechtigungen in `app.json` korrekt sind
- Überprüfen Sie, ob Sie die Berechtigungen auf dem Gerät erteilt haben

### Build-Fehler

**Problem**: "Module not found"
- **Lösung**: Löschen Sie `node_modules` und installieren Sie neu:
  ```bash
  rm -rf node_modules
  npm install
  ```

## Datenbank-Schema

### Firestore Collection: `mealPlans`

```javascript
{
  week: Number,           // Kalenderwoche (1-53)
  year: Number,           // Jahr (z.B. 2024)
  imageUrl: String,       // URL zum Speiseplan-Bild
  notes: String,          // Optional: Hinweise
  createdAt: Timestamp    // Erstellungszeitpunkt
}
```

## Sicherheit

- Firebase Authentication für Admin-Zugriff
- Firestore Security Rules beschränken Schreibzugriff
- Storage Security Rules beschränken Upload-Zugriff
- Keine sensiblen Daten im Code (verwenden Sie Umgebungsvariablen)

## Performance

- Bilder werden automatisch komprimiert (quality: 0.8)
- Lazy Loading für große Speiseplan-Bilder
- Caching durch Firebase
- Optimierte Bundle-Größe durch Expo

## Zukünftige Erweiterungen

- [ ] Push-Notifications für neue Speisepläne
- [ ] Favoriten-Funktion für Gerichte
- [ ] Mehrsprachigkeit (Deutsch/Englisch)
- [ ] Offline-Modus mit lokaler Speicherung
- [ ] Kalender-Integration
- [ ] Ernährungshinweise (vegetarisch, vegan, Allergene)
- [ ] Bewertungssystem für Gerichte

## Lizenz

MIT License - Frei verwendbar für kommerzielle und private Zwecke.

## Support

Bei Fragen oder Problemen:
- Erstellen Sie ein Issue im Repository
- Kontaktieren Sie den Entwickler

## Credits

Entwickelt mit React Native, Expo und Firebase.
Design inspiriert von militärischen UI-Konzepten.

---

**Viel Erfolg mit Ihrer Speiseplan-App!** 🎖️
