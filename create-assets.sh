#!/bin/bash

# Script zum Erstellen von Platzhalter-Assets für die Speiseplan-App
# Verwendet placeholder.com für schnelle Testbilder

echo "🎨 Erstelle Platzhalter-Assets für die Speiseplan-App..."

# Assets-Ordner erstellen
mkdir -p assets

# Farben für militärisches Design
BG_COLOR="2C3E2F"  # Olivgrün
FG_COLOR="8B7355"  # Sandbraun

echo "📱 Lade icon.png (1024x1024)..."
curl -o assets/icon.png "https://via.placeholder.com/1024x1024/${BG_COLOR}/${FG_COLOR}?text=Speiseplan"

echo "🖼️ Lade splash.png (1284x2778)..."
curl -o assets/splash.png "https://via.placeholder.com/1284x2778/${BG_COLOR}/${FG_COLOR}?text=Speiseplan+App"

echo "🎯 Lade adaptive-icon.png (1024x1024)..."
curl -o assets/adaptive-icon.png "https://via.placeholder.com/1024x1024/${BG_COLOR}/${FG_COLOR}?text=S"

echo "🌐 Lade favicon.png (48x48)..."
curl -o assets/favicon.png "https://via.placeholder.com/48x48/${BG_COLOR}/${FG_COLOR}?text=S"

echo ""
echo "✅ Alle Assets wurden erstellt!"
echo ""
echo "Dateien im assets/ Ordner:"
ls -lh assets/

echo ""
echo "📝 Hinweis: Dies sind nur Platzhalter für Tests."
echo "   Für Production sollten Sie eigene, professionelle Icons erstellen."
echo ""
echo "🚀 Nächster Schritt: eas build --platform android --profile preview"
