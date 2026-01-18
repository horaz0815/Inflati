# Inflati

![Build Status](https://github.com/horaz0815/Inflati/actions/workflows/build-apk.yml/badge.svg)

Dieses Repository enthält mehrere Rechner-Anwendungen:

## 📱 Militär Gehaltsrechner (Android App)

Eine vollständige Android-App zur Berechnung von Gehältern für österreichisches Bundesheer-Personal.

**[→ Zur App-Dokumentation](README_MILITARY_CALCULATOR.md)**

**[→ APK Download Anleitung](APK_DOWNLOAD_ANLEITUNG.md)**

### Quick Start - APK herunterladen:
1. [GitHub Actions](https://github.com/horaz0815/Inflati/actions) öffnen
2. Neuesten Build auswählen
3. "app-debug.zip" unter Artifacts herunterladen
4. Auf Android-Gerät installieren

### Features:
- Verwendungsgruppen: M1, M2, M3
- Gehaltsstufen: 1-8
- Funktionszulagen: F1-F5
- Automatische Gehaltsberechnung
- Benutzerfreundliches UI

---

## 💶 Inflationsrechner (Web App)

Ein HTML/JavaScript-basierter Inflationsrechner.

**Datei:** [v66.html](v66.html)

### Features:
- Wertanpassung nach Inflationsraten
- Konfigurierbare Inflationsraten
- Verschiedene Varianten (SR+UR, HR+GF+WD)

---

## 🔧 Entwicklung

### Android App bauen:
```bash
./gradlew assembleDebug
```

### Automatischer Build:
Bei jedem Push wird automatisch durch GitHub Actions eine APK gebaut und als Artifact bereitgestellt.

---

## 📄 Lizenz

Diese Anwendungen dienen nur zu Informationszwecken. Gehaltsdaten sollten mit offiziellen Quellen abgeglichen werden.