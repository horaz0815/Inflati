# 🚀 APK JETZT BAUEN

## Schnellste Methode (3 Befehle)

```bash
# 1. Repository klonen (falls noch nicht geschehen)
git clone https://github.com/horaz0815/Inflati.git
cd Inflati
git checkout claude/meal-plan-app-A3zKa

# 2. Build-Script ausführen
./build-apk.sh
```

**Das war's!** Das Script macht alles automatisch:
- ✅ Assets erstellen
- ✅ Dependencies installieren
- ✅ EAS CLI einrichten
- ✅ Bei Expo anmelden
- ✅ APK bauen

---

## Alternative: Schritt für Schritt

### 1. Assets erstellen

**Option A: Automatisch (empfohlen)**
```bash
./create-assets.sh
```

**Option B: Manuell**
Laden Sie Icons herunter oder erstellen Sie diese:
- `assets/icon.png` (1024x1024px)
- `assets/splash.png` (1284x2778px)
- `assets/adaptive-icon.png` (1024x1024px)
- `assets/favicon.png` (48x48px)

**Option C: Mit Python**
```bash
pip3 install Pillow
python3 create-simple-assets.py
```

### 2. Dependencies installieren

```bash
npm install
```

### 3. EAS CLI installieren

```bash
npm install -g eas-cli
```

### 4. Bei Expo anmelden

```bash
eas login
```

Noch kein Account? → https://expo.dev/signup (kostenlos)

### 5. APK bauen

```bash
npm run build:preview
```

Oder direkt:
```bash
eas build --platform android --profile preview
```

⏱️ **Wartezeit:** 10-15 Minuten

---

## Nach dem Build

### APK herunterladen

1. **Link im Terminal anklicken**
2. **Oder** gehen Sie zu https://expo.dev/
3. Navigieren Sie zu "Builds"
4. Laden Sie die APK herunter

### Auf Smartphone installieren

1. Übertragen Sie die APK auf Ihr Android-Gerät
2. Öffnen Sie die APK-Datei
3. Erlauben Sie "Installation aus unbekannten Quellen"
4. Installieren

---

## ⚠️ Wichtig NACH der Installation

### Firebase konfigurieren

Die App benötigt Firebase, um zu funktionieren!

**Schnellstart:**
1. Erstellen Sie ein Firebase-Projekt: https://console.firebase.google.com/
2. Kopieren Sie die Konfiguration nach `firebase.config.js`
3. Erstellen Sie einen Admin-Benutzer
4. Erstellen Sie einen neuen Build mit Firebase-Konfiguration

**Detaillierte Anleitung:** [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)

---

## Problemlösung

### "Assets not found"
```bash
./create-assets.sh
# oder
python3 create-simple-assets.py
```

### "eas: command not found"
```bash
npm install -g eas-cli
```

### "Build failed"
```bash
# Logs ansehen
eas build --platform android --profile preview
# Oder im Browser: https://expo.dev/accounts/[USERNAME]/builds
```

### "Not logged in"
```bash
eas login
```

---

## Kosten

✅ **Komplett kostenlos** (Free Plan)
- 30 Builds/Monat
- Perfekt für Tests und kleine Projekte

---

## Was funktioniert ohne Firebase?

In der APK OHNE Firebase-Konfiguration:
- ✅ UI und Design ansehen
- ✅ Navigation testen
- ❌ Login nicht möglich
- ❌ Kein Speiseplan-Upload
- ❌ Keine Speiseplan-Anzeige

**Fazit:** Firebase ist essentiell für die App!

---

## Nützliche Befehle

```bash
# Build-Status prüfen
eas build:list

# Bestimmten Build herunterladen
eas build:view [BUILD_ID]

# Production Build (für App Store)
npm run build:production

# Beide Plattformen
npm run build:all
```

---

## Weitere Dokumentation

- **Detaillierte Build-Anleitung:** [BUILD_APK.md](./BUILD_APK.md)
- **Firebase Setup:** [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)
- **Schnellstart:** [APK_SCHNELLSTART.md](./APK_SCHNELLSTART.md)
- **Expo Go:** [EXPO_GO_ANLEITUNG.md](./EXPO_GO_ANLEITUNG.md)

---

**Los geht's! 🚀**

```bash
./build-apk.sh
```
