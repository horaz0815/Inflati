# Schnellstart-Anleitung

Schneller Einstieg in die Speiseplan-App in 5 Minuten!

## Voraussetzungen

- Node.js installiert
- Ein Google-Konto für Firebase

## 1. Installation (2 Minuten)

```bash
# Dependencies installieren
npm install

# Expo CLI global installieren (falls noch nicht vorhanden)
npm install -g expo-cli
```

## 2. Firebase einrichten (2 Minuten)

### Quick Setup:
1. Gehen Sie zu https://console.firebase.google.com/
2. Erstellen Sie ein neues Projekt
3. Aktivieren Sie:
   - **Authentication** (Email/Password)
   - **Firestore Database**
   - **Storage**
4. Registrieren Sie eine Web-App
5. Kopieren Sie die Firebase-Konfiguration
6. Öffnen Sie `firebase.config.js` und ersetzen Sie die Werte

### Security Rules:

**Firestore Rules** (Firestore → Rules):
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /mealPlans/{document} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

**Storage Rules** (Storage → Rules):
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /mealplans/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

### Admin-Benutzer erstellen:
1. Firebase Console → Authentication → Users
2. Klicken Sie auf "Add user"
3. Erstellen Sie einen Benutzer (z.B. admin@test.de / testpasswort)

## 3. App starten (1 Minute)

```bash
npm start
```

Scannen Sie den QR-Code mit der Expo Go App auf Ihrem Smartphone:
- **Android**: [Expo Go](https://play.google.com/store/apps/details?id=host.exp.exponent)
- **iOS**: [Expo Go](https://apps.apple.com/app/expo-go/id982107779)

## 4. App testen

### Test 1: Admin-Login
1. Klicken Sie auf das Zahnrad ⚙️
2. Geben Sie Admin-Zugangsdaten ein
3. Klicken Sie auf "ANMELDEN"

### Test 2: Speiseplan hochladen
1. Klicken Sie auf "Speiseplan hochladen"
2. Wählen Sie "Galerie" (oder "Kamera" für ein neues Foto)
3. Wählen Sie ein Testbild aus
4. Klicken Sie auf "HOCHLADEN"

### Test 3: Speiseplan anzeigen
1. Gehen Sie zurück zum Hauptbildschirm
2. Der Speiseplan wird angezeigt!

## Fehlerbehebung

### "Firebase: Error (auth/...)"
→ Überprüfen Sie firebase.config.js und Firebase-Einstellungen

### "Module not found"
→ Führen Sie `npm install` erneut aus

### Kamera funktioniert nicht
→ Erteilen Sie Kamera-Berechtigungen auf Ihrem Gerät

## Nächste Schritte

1. **Assets erstellen**: Siehe `assets/README.md`
2. **AdMob einrichten**: Siehe Hauptdokumentation
3. **Production Build**: Siehe README.md → "Build für Production"

## Dokumentation

- **Vollständige Anleitung**: [README.md](./README.md)
- **Firebase Setup**: [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)
- **Assets Guide**: [assets/README.md](./assets/README.md)

---

**Die App läuft? Perfekt! 🎉**

Jetzt können Sie mit der Anpassung beginnen:
- Design in `theme.js` anpassen
- Screens in `screens/` erweitern
- Neue Features hinzufügen

Viel Spaß beim Entwickeln! 🚀
