# Assets

Dieser Ordner enthält alle Bilder und Icons für die Speiseplan-App.

## Benötigte Dateien

Erstellen Sie die folgenden Dateien mit militärischem Design (Olivgrün #2C3E2F):

### 1. icon.png
- **Größe**: 1024 x 1024 px
- **Format**: PNG
- **Verwendung**: Haupt-App-Icon
- **Design**: Quadratisches Icon mit militärischem Look
- **Hintergrund**: Olivgrün #2C3E2F
- **Vordergrund**: Kann ein Messer/Gabel-Symbol oder militärisches Symbol enthalten

### 2. splash.png
- **Größe**: 1284 x 2778 px
- **Format**: PNG
- **Verwendung**: Splash-Screen beim App-Start
- **Design**: Vollbild-Hintergrund mit App-Logo in der Mitte
- **Hintergrund**: Olivgrün #2C3E2F
- **Vordergrund**: App-Logo und Text "SPEISEPLAN"

### 3. adaptive-icon.png
- **Größe**: 1024 x 1024 px
- **Format**: PNG
- **Verwendung**: Android Adaptive Icon
- **Design**: Wie icon.png, aber mit transparentem Hintergrund
- **Hinweis**: Android schneidet das Icon zu verschiedenen Formen (Kreis, Quadrat, etc.)

### 4. favicon.png
- **Größe**: 48 x 48 px
- **Format**: PNG
- **Verwendung**: Web-Favicon
- **Design**: Verkleinerte Version des Icons

## Schnelle Erstellung

### Option 1: Online-Tool verwenden
Nutzen Sie [App Icon Generator](https://www.appicon.co/):
1. Laden Sie ein 1024x1024 px Bild hoch
2. Generieren Sie alle benötigten Größen
3. Laden Sie das Asset-Paket herunter
4. Ersetzen Sie die generierten Dateien in diesem Ordner

### Option 2: Manuell erstellen
Verwenden Sie Bildbearbeitungstools wie:
- Adobe Photoshop
- GIMP (kostenlos)
- Figma (kostenlos)
- Canva (kostenlos)

### Option 3: Platzhalter verwenden
Verwenden Sie temporär farbige Quadrate:

```bash
# Mit ImageMagick (muss installiert sein)
convert -size 1024x1024 xc:#2C3E2F icon.png
convert -size 1284x2778 xc:#2C3E2F splash.png
convert -size 1024x1024 xc:#2C3E2F adaptive-icon.png
convert -size 48x48 xc:#2C3E2F favicon.png
```

## Design-Richtlinien

### Farbpalette
- **Primärfarbe**: #2C3E2F (Olivgrün)
- **Akzentfarbe**: #8B7355 (Sandbraun)
- **Text**: #E8E8E8 (Helles Grau)

### Stil
- Militärisch, funktional
- Klare Linien
- Hoher Kontrast
- Einfache, ikonische Symbole

### Beispiel-Symbole
- 🍽️ Teller und Besteck
- 📅 Kalender
- 🎖️ Militärisches Abzeichen
- 📋 Clipboard mit Speiseplan

## Lizenz

Stellen Sie sicher, dass Sie die Rechte für alle verwendeten Bilder haben.
Kostenlose Icons: [Flaticon](https://www.flaticon.com/), [Icons8](https://icons8.com/)
