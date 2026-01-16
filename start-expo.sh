#!/bin/bash

echo "🚀 Speiseplan-App mit Expo Go starten"
echo "======================================"
echo ""

# Prüfen ob node_modules existiert
if [ ! -d "node_modules" ]; then
    echo "📦 Dependencies werden installiert..."
    npm install
    echo ""
fi

# Prüfen ob Assets existieren
if [ ! -f "assets/icon.png" ]; then
    echo "⚠️  Assets fehlen!"
    echo ""
    echo "Assets werden erstellt..."
    ./create-assets.sh
    echo ""
fi

echo "✅ Alles bereit!"
echo ""
echo "📱 So testen Sie die App:"
echo ""
echo "1. Installieren Sie Expo Go auf Ihrem Smartphone:"
echo "   📱 Android: https://play.google.com/store/apps/details?id=host.exp.exponent"
echo "   🍎 iOS: https://apps.apple.com/app/expo-go/id982107779"
echo ""
echo "2. Scannen Sie den QR-Code der gleich erscheint"
echo ""
echo "3. Die App öffnet sich automatisch in Expo Go!"
echo ""
echo "======================================"
echo "🔥 Dev Server wird gestartet..."
echo ""

# Expo Dev Server starten
npm start
