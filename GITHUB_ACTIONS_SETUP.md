# GitHub Actions APK Build Setup

Diese Anleitung zeigt, wie Sie automatische APK-Builds mit GitHub Actions einrichten.

## Vorteile

✅ **Automatisch** - APK wird bei jedem Push gebaut
✅ **GitHub Releases** - APK direkt von GitHub herunterladen
✅ **Keine lokale Installation** - Build läuft auf GitHub-Servern
✅ **Kostenlos** - GitHub Actions ist für öffentliche Repos kostenlos
✅ **Versionierung** - Automatische Releases mit Tags

---

## Einrichtung (5 Minuten)

### Schritt 1: Expo Access Token erstellen

1. **Gehen Sie zu:** https://expo.dev/
2. **Melden Sie sich an** (oder erstellen Sie einen Account)
3. **Klicken Sie auf Ihr Profil** (oben rechts)
4. **Wählen Sie:** "Access Tokens"
5. **Klicken Sie:** "Create Token"
6. **Name:** `GITHUB_ACTIONS` (oder beliebig)
7. **Kopieren Sie den Token** (wird nur einmal angezeigt!)

### Schritt 2: Token zu GitHub hinzufügen

1. **Gehen Sie zu Ihrem Repository:** https://github.com/horaz0815/Inflati
2. **Klicken Sie:** "Settings" (oben rechts)
3. **Linke Sidebar:** "Secrets and variables" → "Actions"
4. **Klicken Sie:** "New repository secret"
5. **Name:** `EXPO_TOKEN`
6. **Value:** [Fügen Sie den Expo Token ein]
7. **Klicken Sie:** "Add secret"

### Schritt 3: Workflow aktivieren

Die Workflows sind bereits im Repository:
- `.github/workflows/build-apk.yml` - Einfacher Build
- `.github/workflows/release-apk.yml` - Build + GitHub Release

**Sie sind sofort einsatzbereit!** 🎉

---

## Verwendung

### Methode 1: Manueller Build (Empfohlen)

**Für einen schnellen Test-Build:**

1. Gehen Sie zu: https://github.com/horaz0815/Inflati/actions
2. Wählen Sie: "Build Android APK"
3. Klicken Sie: "Run workflow"
4. Wählen Sie Branch: `claude/meal-plan-app-A3zKa`
5. Wählen Sie Profile: `preview` (für Tests)
6. Klicken Sie: "Run workflow"

**Dann:**
- ⏱️ Warten Sie 10-15 Minuten
- 📊 Schauen Sie den Workflow-Status an
- 🔗 Am Ende wird ein Link zu expo.dev angezeigt
- 📥 Laden Sie die APK von expo.dev herunter

### Methode 2: Release erstellen (Für Production)

**Für einen offiziellen Release mit GitHub Download:**

1. Gehen Sie zu: https://github.com/horaz0815/Inflati/actions
2. Wählen Sie: "Release APK to GitHub"
3. Klicken Sie: "Run workflow"
4. Geben Sie eine Version ein: `1.0.0`
5. Geben Sie Release Notes ein (optional)
6. Klicken Sie: "Run workflow"

**Dann:**
- ⏱️ Warten Sie 10-15 Minuten
- 🎉 Ein neuer Release wird automatisch erstellt
- 📥 APK ist unter "Releases" verfügbar
- 🔗 Direkter Download-Link: https://github.com/horaz0815/Inflati/releases

### Methode 3: Automatischer Build bei Push

**Automatisch bei jedem Push:**

Wenn Sie Code pushen auf:
- `main`
- `master`
- `claude/meal-plan-app-*`

Dann wird **automatisch** ein Build gestartet!

### Methode 4: Release mit Git Tag

**Versionierte Releases:**

```bash
git tag v1.0.0
git push origin v1.0.0
```

Dies triggert automatisch:
- ✅ APK Build
- ✅ GitHub Release
- ✅ Download-Link

---

## Workflow-Übersicht

### Build APK Workflow (`build-apk.yml`)

**Trigger:**
- Manuell via GitHub UI
- Push auf main/master/claude-branches
- Pull Requests

**Was passiert:**
1. ✅ Code auschecken
2. ✅ Dependencies installieren
3. ✅ Assets erstellen
4. ✅ APK bauen (Expo Cloud)
5. ✅ Link anzeigen

**Output:**
- Link zu expo.dev
- Build-Status
- Workflow-Summary

### Release APK Workflow (`release-apk.yml`)

**Trigger:**
- Manuell via GitHub UI
- Git Tags (v*.*.*)

**Was passiert:**
1. ✅ Code auschecken
2. ✅ Dependencies installieren
3. ✅ Assets erstellen
4. ✅ APK bauen (Expo Cloud)
5. ✅ Auf Build warten (bis zu 30 Min)
6. ✅ APK herunterladen
7. ✅ GitHub Release erstellen
8. ✅ APK hochladen

**Output:**
- GitHub Release mit APK
- Direkter Download-Link
- Automatische Version-Tags

---

## APK herunterladen

### Von expo.dev (Build Workflow)

1. Gehen Sie zu: https://expo.dev/
2. Navigieren Sie zu "Builds"
3. Finden Sie Ihren neuesten Build
4. Klicken Sie "Download"

### Von GitHub Releases (Release Workflow)

1. Gehen Sie zu: https://github.com/horaz0815/Inflati/releases
2. Wählen Sie die gewünschte Version
3. Unter "Assets" finden Sie: `speiseplan-app.apk`
4. Klicken Sie zum Herunterladen

**Direkter Link (neuester Release):**
```
https://github.com/horaz0815/Inflati/releases/latest
```

---

## Workflow-Status prüfen

### Live-Status

Gehen Sie zu: https://github.com/horaz0815/Inflati/actions

Hier sehen Sie:
- 🟢 Laufende Workflows
- ✅ Erfolgreiche Builds
- ❌ Fehlgeschlagene Builds
- ⏸️ Wartende Workflows

### Build-Logs ansehen

1. Klicken Sie auf einen Workflow
2. Klicken Sie auf "build" Job
3. Erweitern Sie die einzelnen Steps
4. Sehen Sie detaillierte Logs

### Notifications

Sie erhalten automatisch E-Mails bei:
- ✅ Erfolgreichem Build
- ❌ Fehlgeschlagenem Build

---

## Troubleshooting

### "EXPO_TOKEN Secret not found"

**Problem:** Expo Token wurde nicht zu GitHub Secrets hinzugefügt

**Lösung:**
1. Erstellen Sie einen Expo Access Token
2. Fügen Sie ihn zu GitHub Secrets hinzu (Name: `EXPO_TOKEN`)
3. Starten Sie den Workflow erneut

### "Build failed" / "eas: command not found"

**Problem:** EAS CLI Installation fehlgeschlagen

**Lösung:**
- Workflow automatisch wiederholen
- Oder manuell lokal bauen: `./build-apk.sh`

### "Timeout waiting for build"

**Problem:** Build dauert länger als 30 Minuten

**Lösung:**
- Gehen Sie zu expo.dev und prüfen Sie den Build-Status
- Laden Sie die APK manuell von expo.dev herunter

### "No assets found"

**Problem:** Asset-Generierung fehlgeschlagen

**Lösung:**
- Assets manuell erstellen und zum Repo hinzufügen
- Oder Python Pillow Installation prüfen

### Build läuft, aber keine APK?

**Für einfachen Build-Workflow:**
- APK ist auf expo.dev verfügbar
- Gehen Sie zu https://expo.dev/ → Builds

**Für Release-Workflow:**
- APK wird automatisch zu GitHub Releases hochgeladen
- Prüfen Sie: https://github.com/horaz0815/Inflati/releases

---

## Kosten

### GitHub Actions
- ✅ **Kostenlos** für öffentliche Repositories
- ✅ 2000 Minuten/Monat für private Repos (Free Plan)

### Expo Builds
- ✅ **30 Builds/Monat kostenlos** (Free Plan)
- ✅ Ausreichend für Tests und kleine Projekte

**Gesamt: KOSTENLOS** für normale Nutzung! 🎉

---

## Best Practices

### 1. Verwenden Sie Tags für Releases

```bash
git tag v1.0.0 -m "Release Version 1.0.0"
git push origin v1.0.0
```

### 2. Semantic Versioning

- `v1.0.0` - Major Release
- `v1.1.0` - Minor Update (neue Features)
- `v1.0.1` - Patch (Bugfixes)

### 3. Release Notes schreiben

Bei manuellen Releases beschreiben Sie:
- Was ist neu?
- Was wurde geändert?
- Bekannte Probleme?

### 4. Test-Builds vs. Production

- **Preview Profile:** Für Tests, schnell, nicht optimiert
- **Production Profile:** Für Releases, optimiert, minimiert

### 5. Firebase vor Release konfigurieren

Erstellen Sie einen Build MIT Firebase-Konfiguration für Production!

---

## Erweiterte Konfiguration

### Build-Profile anpassen

Bearbeiten Sie `eas.json`:

```json
{
  "build": {
    "preview": {
      "android": {
        "buildType": "apk"
      }
    },
    "production": {
      "android": {
        "buildType": "apk"
      }
    }
  }
}
```

### Workflow-Trigger ändern

Bearbeiten Sie `.github/workflows/build-apk.yml`:

```yaml
on:
  push:
    branches:
      - main
      - develop  # Fügen Sie weitere Branches hinzu
```

### Automatische PR-Kommentare

Der Workflow kommentiert automatisch auf Pull Requests mit Build-Status!

---

## Nächste Schritte

1. ✅ **Expo Token erstellen und zu Secrets hinzufügen**
2. ✅ **Ersten Build starten** (Actions → Build Android APK → Run workflow)
3. ✅ **APK herunterladen** von expo.dev oder GitHub Releases
4. ✅ **Auf Smartphone installieren**
5. ✅ **Firebase konfigurieren** (siehe FIREBASE_SETUP.md)
6. ✅ **Production Release erstellen** mit konfiguriertem Firebase

---

## Hilfreiche Links

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Expo EAS Build:** https://docs.expo.dev/build/introduction/
- **Expo Access Tokens:** https://docs.expo.dev/accounts/programmatic-access/
- **Ihr Repository Actions:** https://github.com/horaz0815/Inflati/actions
- **Ihr Repository Releases:** https://github.com/horaz0815/Inflati/releases

---

## Support

Bei Problemen:

1. **Prüfen Sie die Workflow-Logs** in GitHub Actions
2. **Schauen Sie expo.dev** für Build-Details
3. **Erstellen Sie ein Issue** im Repository
4. **Konsultieren Sie:** BUILD_APK.md für lokale Build-Probleme

---

**Viel Erfolg mit automatischen Builds!** 🚀
