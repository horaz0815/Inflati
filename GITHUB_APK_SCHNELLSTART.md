# 🚀 APK auf GitHub bauen - Schnellstart

## In 3 Schritten zur APK

### 1️⃣ Expo Token erstellen (2 Minuten)

1. Gehen Sie zu: **https://expo.dev/**
2. Melden Sie sich an (kostenlos)
3. Profil → **Access Tokens** → **Create Token**
4. **Kopieren Sie den Token**

### 2️⃣ Token zu GitHub hinzufügen (1 Minute)

1. Gehen Sie zu: **https://github.com/horaz0815/Inflati/settings/secrets/actions**
2. Klicken Sie: **New repository secret**
3. Name: `EXPO_TOKEN`
4. Value: [Fügen Sie den Token ein]
5. **Add secret**

### 3️⃣ Build starten (30 Sekunden)

1. Gehen Sie zu: **https://github.com/horaz0815/Inflati/actions**
2. Wählen Sie: **"Build Android APK"**
3. Klicken Sie: **"Run workflow"**
4. Branch: `claude/meal-plan-app-A3zKa`
5. Profile: `preview`
6. **Run workflow**

---

## ⏱️ Warten (10-15 Minuten)

Während der Build läuft:
- ☕ Kaffee holen
- 📱 expo.dev vorbereiten
- 📖 Firebase-Anleitung lesen

---

## 📥 APK herunterladen

### Option A: Von expo.dev

1. **https://expo.dev/** → Builds
2. Neuester Build
3. **Download**

### Option B: Von GitHub Releases (bei Release-Workflow)

1. **https://github.com/horaz0815/Inflati/releases**
2. Neuester Release
3. Assets → **speiseplan-app.apk**

---

## 📱 Installieren

1. APK auf Android-Smartphone übertragen
2. APK-Datei öffnen
3. "Unbekannte Quellen" erlauben
4. Installieren

---

## ⚠️ Wichtig

**Firebase muss konfiguriert werden!**

Siehe: [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)

---

## 🎯 Alternative Workflows

### Schneller Test-Build
```
Actions → Build Android APK → Run workflow
```

### Production Release
```
Actions → Release APK to GitHub → Run workflow
```

### Automatischer Build
```
git push
# Build startet automatisch!
```

### Versionsbasierter Release
```bash
git tag v1.0.0
git push origin v1.0.0
# APK wird automatisch als Release veröffentlicht!
```

---

## 🆘 Probleme?

**"EXPO_TOKEN not found"**
→ Schritt 2 wiederholen (Token zu Secrets hinzufügen)

**"Build failed"**
→ Workflow-Logs ansehen: Actions → [Workflow] → build

**"Keine APK gefunden"**
→ Gehen Sie zu expo.dev → Builds

**"Timeout"**
→ Prüfen Sie expo.dev manuell, Build läuft eventuell noch

---

## 💰 Kosten

✅ **KOSTENLOS**
- GitHub Actions: Kostenlos für öffentliche Repos
- Expo Builds: 30/Monat kostenlos

---

## 📚 Mehr Infos

**Detaillierte Anleitung:** [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md)

**Status prüfen:** https://github.com/horaz0815/Inflati/actions

**Releases:** https://github.com/horaz0815/Inflati/releases

---

**Los geht's!** 🎉

1. Token erstellen
2. Zu GitHub hinzufügen
3. Workflow starten
4. APK herunterladen
5. Installieren
