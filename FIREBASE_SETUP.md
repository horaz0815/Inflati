# Firebase Setup-Anleitung

Diese Anleitung führt Sie Schritt für Schritt durch die Firebase-Einrichtung für die Speiseplan-App.

## 1. Firebase-Projekt erstellen

### Schritt 1: Firebase Console öffnen
1. Gehen Sie zu https://console.firebase.google.com/
2. Melden Sie sich mit Ihrem Google-Konto an
3. Klicken Sie auf "Projekt hinzufügen"

### Schritt 2: Projekt konfigurieren
1. **Projektname**: Geben Sie einen Namen ein (z.B. "Speiseplan-App")
2. **Google Analytics**: Optional, kann später aktiviert werden
3. Klicken Sie auf "Projekt erstellen"
4. Warten Sie, bis das Projekt erstellt wurde

## 2. Firebase Services aktivieren

### A. Authentication einrichten

1. **Klicken Sie auf "Authentication"** im linken Menü
2. Klicken Sie auf "Get Started"
3. Wählen Sie **"Email/Password"** als Sign-in-Methode
4. **Aktivieren Sie** "Email/Password"
5. Klicken Sie auf "Speichern"

### B. Firestore Database einrichten

1. **Klicken Sie auf "Firestore Database"** im linken Menü
2. Klicken Sie auf "Create database"
3. Wählen Sie **"Start in production mode"** (wir fügen später eigene Rules hinzu)
4. Wählen Sie einen **Cloud Firestore-Standort** (z.B. europe-west3 für Deutschland)
5. Klicken Sie auf "Aktivieren"

#### Firestore Security Rules setzen

1. Klicken Sie auf den Tab **"Rules"**
2. Ersetzen Sie die Regeln mit:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Meal Plans Collection
    match /mealPlans/{document} {
      // Jeder kann lesen
      allow read: if true;
      // Nur authentifizierte Benutzer können erstellen/ändern/löschen
      allow create, update, delete: if request.auth != null;
    }
  }
}
```

3. Klicken Sie auf **"Veröffentlichen"**

### C. Storage einrichten

1. **Klicken Sie auf "Storage"** im linken Menü
2. Klicken Sie auf "Get Started"
3. Wählen Sie **"Start in production mode"**
4. Wählen Sie denselben **Standort** wie bei Firestore
5. Klicken Sie auf "Fertig"

#### Storage Security Rules setzen

1. Klicken Sie auf den Tab **"Rules"**
2. Ersetzen Sie die Regeln mit:

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Meal Plan Bilder
    match /mealplans/{allPaths=**} {
      // Jeder kann lesen
      allow read: if true;
      // Nur authentifizierte Benutzer können hochladen
      allow write: if request.auth != null;
    }
  }
}
```

3. Klicken Sie auf **"Veröffentlichen"**

## 3. Web-App registrieren und Konfiguration erhalten

### Schritt 1: Web-App hinzufügen
1. Gehen Sie zurück zur **Projektübersicht** (Klicken Sie auf das Firebase-Logo oben links)
2. Klicken Sie auf das **Web-Symbol** (</>) unter "Fügen Sie eine App hinzu..."
3. **App-Spitzname**: Geben Sie einen Namen ein (z.B. "Speiseplan Web")
4. **Firebase Hosting**: NICHT aktivieren (nicht benötigt)
5. Klicken Sie auf **"App registrieren"**

### Schritt 2: Firebase-Konfiguration kopieren
1. Sie sehen nun die Firebase SDK-Konfiguration
2. Kopieren Sie den gesamten `firebaseConfig` Block:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "speiseplan-app-xxxxx.firebaseapp.com",
  projectId: "speiseplan-app-xxxxx",
  storageBucket: "speiseplan-app-xxxxx.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abc123def456"
};
```

### Schritt 3: Konfiguration in die App einfügen
1. Öffnen Sie die Datei `firebase.config.js` in Ihrem Projekt
2. Ersetzen Sie die Platzhalter-Werte mit Ihren echten Werten:

```javascript
const firebaseConfig = {
  apiKey: "IHR_API_KEY",              // Ersetzen!
  authDomain: "ihr-projekt.firebaseapp.com",  // Ersetzen!
  projectId: "ihr-projekt-id",        // Ersetzen!
  storageBucket: "ihr-projekt.appspot.com",   // Ersetzen!
  messagingSenderId: "123456789",     // Ersetzen!
  appId: "1:123456789:web:abcdef123456"  // Ersetzen!
};
```

## 4. Admin-Benutzer erstellen

### Schritt 1: Benutzer manuell hinzufügen
1. Gehen Sie zu **"Authentication"** → **"Users"**
2. Klicken Sie auf **"Add user"**
3. **E-Mail**: Geben Sie Ihre Admin-E-Mail ein (z.B. admin@speiseplan.de)
4. **Passwort**: Wählen Sie ein sicheres Passwort (min. 6 Zeichen)
5. Klicken Sie auf **"Add user"**

### Schritt 2: Zugangsdaten notieren
Notieren Sie sich die E-Mail und das Passwort sicher - diese benötigen Sie zum Anmelden in der App!

## 5. Android-Konfiguration (für Production Builds)

### Wenn Sie einen Android Build erstellen möchten:

1. **SHA-1 Key generieren**:
```bash
# Für Debug
keytool -list -v -alias androiddebugkey -keystore ~/.android/debug.keystore

# Für Release (nach Keystore-Erstellung)
keytool -list -v -alias YOUR_ALIAS -keystore YOUR_KEYSTORE.jks
```

2. **SHA-1 zu Firebase hinzufügen**:
   - Gehen Sie zu Projekteinstellungen → Ihre Apps
   - Wählen Sie Ihre Android-App
   - Scrollen Sie zu "SHA certificate fingerprints"
   - Fügen Sie den SHA-1 Key hinzu

3. **google-services.json herunterladen**:
   - Scrollen Sie in den Projekteinstellungen nach unten
   - Klicken Sie auf "google-services.json herunterladen"
   - Speichern Sie die Datei im Root-Verzeichnis Ihres Projekts

## 6. iOS-Konfiguration (für Production Builds)

### Wenn Sie einen iOS Build erstellen möchten:

1. **iOS-App in Firebase hinzufügen**:
   - Gehen Sie zur Projektübersicht
   - Klicken Sie auf das iOS-Symbol
   - Bundle ID: `com.speiseplan.app` (oder Ihre eigene)
   - App-Spitzname: "Speiseplan iOS"

2. **GoogleService-Info.plist herunterladen**:
   - Laden Sie die Datei herunter
   - Speichern Sie sie im Root-Verzeichnis Ihres Projekts

## 7. Testen der Firebase-Verbindung

### Test 1: App starten
```bash
npm start
```

Die App sollte ohne Fehler starten.

### Test 2: Admin-Login testen
1. Öffnen Sie die App
2. Klicken Sie auf das Zahnrad-Symbol (⚙️)
3. Geben Sie die Admin-Credentials ein
4. Klicken Sie auf "ANMELDEN"
5. Sie sollten erfolgreich angemeldet werden

### Test 3: Speiseplan hochladen
1. Nach dem Login, klicken Sie auf "Speiseplan hochladen"
2. Wählen Sie ein Testbild
3. Klicken Sie auf "HOCHLADEN"
4. Das Bild sollte erfolgreich hochgeladen werden

### Test 4: Speiseplan anzeigen
1. Gehen Sie zurück zum Hauptbildschirm
2. Der hochgeladene Speiseplan sollte angezeigt werden

## 8. Firestore-Datenstruktur prüfen

Nach dem ersten Upload sollten Sie die Daten in Firebase sehen können:

1. Gehen Sie zu **"Firestore Database"**
2. Sie sollten eine Collection **"mealPlans"** sehen
3. Klicken Sie darauf, um die Dokumente zu sehen
4. Jedes Dokument sollte folgende Felder haben:
   - `week` (number): Kalenderwoche
   - `year` (number): Jahr
   - `imageUrl` (string): URL zum Bild
   - `notes` (string): Optionale Hinweise
   - `createdAt` (timestamp): Erstellungszeitpunkt

## 9. Storage-Struktur prüfen

1. Gehen Sie zu **"Storage"**
2. Sie sollten einen Ordner **"mealplans"** sehen
3. Darin sollten Unterordner nach Jahren organisiert sein
4. In den Jahresordnern sollten die hochgeladenen Bilder sein

## Troubleshooting

### Problem: "Firebase: Error (auth/user-not-found)"
**Lösung**: Der Benutzer existiert nicht. Erstellen Sie einen Benutzer in Authentication → Users.

### Problem: "Firebase: Error (auth/wrong-password)"
**Lösung**: Falsches Passwort. Überprüfen Sie das Passwort oder setzen Sie es in Firebase zurück.

### Problem: "Firebase: Missing or insufficient permissions"
**Lösung**: Security Rules sind zu restriktiv. Überprüfen Sie die Rules in Firestore/Storage.

### Problem: "Firebase: Network request failed"
**Lösung**: Internetverbindung prüfen oder Firebase-Konfiguration überprüfen.

### Problem: "No such file or directory: 'firebase.config.js'"
**Lösung**: Stellen Sie sicher, dass die Datei existiert und die Firebase-Konfiguration eingefügt wurde.

## Sicherheitshinweise

1. **Niemals** Firebase-Konfiguration in öffentliche Repositories committen
2. Verwenden Sie **Umgebungsvariablen** für sensible Daten
3. Aktivieren Sie **App Check** in Production für zusätzliche Sicherheit
4. Überprüfen Sie regelmäßig die **Firebase Usage** auf ungewöhnliche Aktivitäten
5. Setzen Sie **Firestore Quotas** um unerwartete Kosten zu vermeiden

## Kosten

Firebase hat einen **kostenlosen "Spark" Plan** mit folgenden Limits:
- **Firestore**: 1 GB Speicher, 50.000 Reads/Tag
- **Storage**: 5 GB Speicher, 1 GB Download/Tag
- **Authentication**: Unbegrenzte Benutzer

Für die meisten kleinen bis mittleren Apps ist der kostenlose Plan ausreichend.

## Weiterführende Links

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Firebase Storage Security](https://firebase.google.com/docs/storage/security/start)
- [Firebase Pricing](https://firebase.google.com/pricing)

---

**Viel Erfolg mit Ihrem Firebase-Setup!** 🔥
