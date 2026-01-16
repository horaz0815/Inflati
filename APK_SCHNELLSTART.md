# APK Schnellstart 🚀

## In 5 Schritten zur Test-APK

### 1️⃣ Assets erstellen

**Linux/Mac:**
```bash
./create-assets.sh
```

**Windows:**
```bash
create-assets.bat
```

**Oder manuell:**
```bash
npm run create-assets
```

### 2️⃣ EAS CLI installieren und anmelden

```bash
npm install -g eas-cli
eas login
```

> Noch kein Account? → https://expo.dev/signup (kostenlos)

### 3️⃣ Projekt konfigurieren

```bash
eas build:configure
```

Wählen Sie: **Android** (mit Leertaste)

### 4️⃣ APK bauen

```bash
npm run build:preview
```

**Oder:**
```bash
eas build --platform android --profile preview
```

⏱️ **Build dauert ca. 10-15 Minuten**

### 5️⃣ APK herunterladen & installieren

1. **Link öffnen** (wird im Terminal angezeigt)
2. **APK herunterladen** auf Ihr Smartphone
3. **Installieren** (evtl. "Unbekannte Quellen" erlauben)

---

## Alternative: Sofort testen (ohne APK)

```bash
npm install
npm start
```

Dann:
1. **Expo Go App** installieren ([Android](https://play.google.com/store/apps/details?id=host.exp.exponent) | [iOS](https://apps.apple.com/app/expo-go/id982107779))
2. **QR-Code scannen**
3. **App öffnet sich** ✨

---

## Wichtig: Firebase konfigurieren

Bevor die App funktioniert:

1. Firebase-Projekt erstellen → [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)
2. Konfiguration in `firebase.config.js` eintragen
3. Admin-Benutzer in Firebase erstellen

**Schnellstart:** Siehe [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)

---

## Build-Status prüfen

```bash
# Im Browser
https://expo.dev/
```

Oder direkt nach dem Build den angezeigten Link öffnen.

---

## Probleme?

### "Assets not found"
```bash
# Assets erstellen
./create-assets.sh
```

### "Build failed"
```bash
# Logs ansehen
eas build --platform android --profile preview --local
```

### "Package name conflict"
In `app.json` ändern:
```json
"android": {
  "package": "com.DEIN_NAME.speiseplan"
}
```

---

## Nützliche Befehle

```bash
# Preview Build (zum Testen)
npm run build:preview

# Production Build
npm run build:production

# iOS + Android
npm run build:all

# Build-Liste anzeigen
eas build:list
```

---

## Kosten

✅ **Kostenlos:** 30 Builds/Monat im Free Plan
🚀 Mehr als genug für Tests!

---

**Detaillierte Anleitung:** [BUILD_APK.md](./BUILD_APK.md)

**Viel Erfolg!** 🎉
