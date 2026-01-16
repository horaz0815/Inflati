# Expo Go - App sofort testen

## Methode 1: Lokaler Dev Server (Empfohlen)

### Schritt 1: App starten

```bash
npm install
npm start
```

### Schritt 2: QR-Code scannen

Nach dem Start sehen Sie im Terminal:

```
Metro waiting on exp://192.168.x.x:8081
› Press a │ open Android
› Press i │ open iOS simulator
› Press w │ open web

› Press r │ reload app
› Press m │ toggle menu

To run the app with live reloading, choose one of:
  › Scan the QR code above with Expo Go (Android) or the Camera app (iOS)
  › Press a for Android emulator, or i for iOS simulator.
  › Press w to run on web browser.
```

### Schritt 3: Mit Expo Go öffnen

**Android:**
1. [Expo Go installieren](https://play.google.com/store/apps/details?id=host.exp.exponent)
2. Expo Go öffnen
3. "Scan QR Code" wählen
4. QR-Code aus Terminal scannen

**iOS:**
1. [Expo Go installieren](https://apps.apple.com/app/expo-go/id982107779)
2. Kamera-App öffnen
3. QR-Code aus Terminal scannen
4. "Mit Expo Go öffnen" antippen

---

## Methode 2: Expo Publish (Permanente URL)

### Für eine dauerhafte, teilbare URL:

```bash
# Bei Expo anmelden
npx expo login

# App veröffentlichen
npx expo publish
```

Sie erhalten dann eine URL wie:
```
exp://exp.host/@ihr-username/speiseplan-app
```

Diese URL können Sie teilen und andere können die App mit Expo Go öffnen!

### URL in Browser öffnen:
```
https://expo.dev/@ihr-username/speiseplan-app
```

---

## Methode 3: Tunnel für Remote-Zugriff

Wenn Sie die App von außerhalb Ihres Netzwerks testen möchten:

```bash
npm start -- --tunnel
```

Dies erstellt eine öffentliche URL, die Sie von überall erreichen können.

---

## Expo Go Links

**Download:**
- 📱 [Android - Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
- 🍎 [iOS - Apple App Store](https://apps.apple.com/app/expo-go/id982107779)

**Expo Dashboard:**
- 🌐 https://expo.dev/

---

## Schnellstart

### Ein-Zeilen-Befehl:

```bash
npm install && npm start
```

Dann QR-Code scannen mit Expo Go!

---

## Troubleshooting

### "Unable to connect"
- Stellen Sie sicher, dass Smartphone und Computer im selben WLAN sind
- Oder verwenden Sie: `npm start -- --tunnel`

### "Network response timed out"
- Firewall überprüfen
- Tunnel-Modus verwenden: `npm start -- --tunnel`

### Assets fehlen
```bash
./create-assets.sh
npm start
```

---

## Nach dem Öffnen in Expo Go

Die App läuft jetzt auf Ihrem Smartphone! 🎉

**Aber Achtung:** Firebase muss noch konfiguriert werden, damit alle Features funktionieren.

### Was funktioniert OHNE Firebase:
✅ UI und Design anschauen
✅ Navigation testen
✅ Kamera öffnen (aber nicht uploaden)

### Was BENÖTIGT Firebase:
❌ Admin-Login
❌ Speiseplan hochladen
❌ Speiseplan anzeigen

**Firebase einrichten:** Siehe [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)

---

## Vorteile von Expo Go

✅ **Sofort testen** - Keine APK nötig
✅ **Live Reload** - Änderungen erscheinen sofort
✅ **Schnell** - Perfekt für Entwicklung
✅ **Einfach teilen** - QR-Code an andere senden

## Nachteile

❌ Läuft in Expo Go Container
❌ Einige native Module funktionieren nicht
❌ Branding zeigt "Expo Go"

**Für eine echte App:** APK erstellen (siehe [BUILD_APK.md](./BUILD_APK.md))

---

## URL-Formate

Expo Go unterstützt verschiedene URL-Formate:

```
# Lokal
exp://192.168.1.100:8081

# Tunnel
exp://abc-def.your-username.exp.direct:80

# Published
exp://exp.host/@username/speiseplan-app

# HTTPS (Browser)
https://expo.dev/@username/speiseplan-app
```

---

**Viel Spaß beim Testen!** 📱✨
