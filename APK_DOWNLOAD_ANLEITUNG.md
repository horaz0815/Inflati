# APK Download Anleitung

Die Android APK wird automatisch bei jedem Push durch GitHub Actions gebaut.

## 🚀 APK Herunterladen

### Methode 1: Von GitHub Actions (Einfachste Methode)

1. Gehen Sie zu Ihrem GitHub Repository: `https://github.com/horaz0815/Inflati`

2. Klicken Sie oben auf den Tab **"Actions"**

3. Sie sehen eine Liste aller Workflow-Runs. Klicken Sie auf den neuesten erfolgreichen Build (grünes Häkchen ✓)

4. Scrollen Sie nach unten zum Abschnitt **"Artifacts"**

5. Laden Sie die gewünschte APK herunter:
   - **app-debug** - Debug-Version der APK (empfohlen zum Testen)
   - **app-release-unsigned** - Release-Version (unsigned)
   - **build-info** - Build-Informationen

6. Entpacken Sie die heruntergeladene ZIP-Datei

7. Die APK-Datei ist jetzt bereit zur Installation!

### Methode 2: Direkter Link (nach erstem Build)

Nach dem ersten erfolgreichen Build können Sie die APK direkt über:
```
https://github.com/horaz0815/Inflati/actions
```

herunterladen.

## 📱 APK auf Android installieren

### Voraussetzungen:
- Android-Gerät mit Android 5.0 (Lollipop) oder höher
- Installation aus unbekannten Quellen muss erlaubt sein

### Installationsschritte:

1. **APK auf Ihr Gerät übertragen**
   - Per USB-Kabel kopieren
   - Per E-Mail senden und auf dem Gerät öffnen
   - Mit Cloud-Speicher (Google Drive, Dropbox) übertragen
   - Direkt auf dem Gerät herunterladen

2. **Unbekannte Quellen erlauben** (falls noch nicht aktiviert)
   - Öffnen Sie **Einstellungen**
   - Gehen Sie zu **Sicherheit** oder **Apps & Benachrichtigungen**
   - Aktivieren Sie **Installation aus unbekannten Quellen** oder **Unbekannte Apps installieren**
   - Wählen Sie die App aus, mit der Sie die APK öffnen (z.B. Dateimanager, Chrome)

3. **APK installieren**
   - Tippen Sie auf die APK-Datei
   - Bestätigen Sie die Installation
   - Warten Sie, bis die Installation abgeschlossen ist
   - Tippen Sie auf **Öffnen** oder finden Sie die App im App-Drawer

## 🔄 Automatischer Build-Prozess

Der GitHub Actions Workflow wird automatisch gestartet bei:

- **Push** auf einen `claude/**` Branch
- **Push** auf `main` oder `master` Branch
- **Pull Request** auf `main` oder `master`
- **Manuellem Trigger** (über GitHub Actions Tab)

### Build-Schritte:

1. ✓ Code auschecken
2. ✓ JDK 17 einrichten
3. ✓ Gradle Wrapper ausführbar machen
4. ✓ Debug APK bauen
5. ✓ Release APK bauen (optional)
6. ✓ APKs als Artifacts hochladen

## 📊 Build-Status überprüfen

Sie können den Build-Status auf mehrere Arten überprüfen:

1. **GitHub Actions Tab** - Zeigt alle Builds und deren Status
2. **Commit-Historie** - Häkchen (✓) oder Kreuz (✗) neben jedem Commit
3. **Pull Request** - Build-Status wird automatisch angezeigt

## 🔧 Fehlerbehebung

### "Installation blockiert"
**Lösung:** Aktivieren Sie die Installation aus unbekannten Quellen für die App, mit der Sie die APK öffnen.

### "App wurde nicht installiert"
**Mögliche Ursachen:**
- Nicht genug Speicherplatz
- Inkompatible Android-Version (min. Android 5.0 erforderlich)
- Beschädigte APK-Datei (erneut herunterladen)

### "Build fehlgeschlagen"
**Lösung:**
- Überprüfen Sie die Logs im GitHub Actions Tab
- Stellen Sie sicher, dass alle Gradle-Konfigurationen korrekt sind
- Bei Problemen: Issue im Repository erstellen

## 💡 Tipps

- **Debug vs. Release:** Die Debug-APK ist größer, enthält aber Debug-Informationen, die bei der Fehlersuche helfen.
- **Automatische Updates:** Bei jedem neuen Push wird eine neue APK gebaut. Schauen Sie regelmäßig nach Updates!
- **Artifacts-Aufbewahrung:** GitHub speichert Artifacts standardmäßig 90 Tage lang.

## 📝 Version identifizieren

Um zu sehen, welche Version Sie installiert haben:
1. Öffnen Sie die App
2. Die Version steht im Titel oder in den App-Informationen
3. Alternativ: Laden Sie die `build-info.txt` aus den Artifacts herunter

## 🎯 Schnellstart

**Für Eilige:**
1. https://github.com/horaz0815/Inflati/actions → Neuester Build → Artifacts → app-debug.zip herunterladen
2. ZIP entpacken
3. APK auf Android-Gerät installieren
4. Fertig! 🎉

---

Bei Fragen oder Problemen öffnen Sie bitte ein Issue im Repository.
