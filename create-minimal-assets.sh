#!/bin/bash

# Erstellt minimale PNG-Dateien als Platzhalter
# Diese sind sehr einfach, aber funktional für Tests

echo "🎨 Erstelle minimale Assets für Tests..."
echo ""

mkdir -p assets

# Minimale 1x1 PNGs in Olivgrün erstellen und dann skalieren
# Basis64-kodierte minimale PNGs

# Icon 1024x1024 - Olivgrün (#2C3E2F)
echo "📱 Erstelle icon.png..."
cat > assets/icon.png << 'EOF_ICON'
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==
EOF_ICON
base64 -d assets/icon.png > assets/icon_tmp.png 2>/dev/null || echo "Basis-Fallback"
# Falls base64 nicht funktioniert, erstelle sehr einfache PNG-Datei
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x04\x00\x08\x02\x00\x00\x00\x26\x93\x09\x29\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x00\x00\x00\x00IEND\xaeB`\x82' > assets/icon.png

# Splash 1284x2778
echo "🖼️ Erstelle splash.png..."
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x05\x04\x00\x00\x0a\xda\x08\x02\x00\x00\x00\x26\x93\x09\x29\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x00\x00\x00\x00IEND\xaeB`\x82' > assets/splash.png

# Adaptive Icon 1024x1024
echo "🎯 Erstelle adaptive-icon.png..."
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x04\x00\x00\x00\x04\x00\x08\x02\x00\x00\x00\x26\x93\x09\x29\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x00\x00\x00\x00IEND\xaeB`\x82' > assets/adaptive-icon.png

# Favicon 48x48
echo "🌐 Erstelle favicon.png..."
printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x30\x00\x00\x00\x30\x08\x02\x00\x00\x00\x91\x5d\x1f\xe6\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x00\x00\x00\x00IEND\xaeB`\x82' > assets/favicon.png

echo ""
echo "✅ Minimale Assets erstellt!"
echo ""
echo "⚠️  HINWEIS: Dies sind sehr einfache Platzhalter nur für Tests."
echo "   Für Production erstellen Sie professionelle Icons."
echo ""
echo "Dateien im assets/ Ordner:"
ls -lh assets/*.png 2>/dev/null || ls -l assets/*.png

echo ""
echo "🚀 Nächster Schritt: ./build-apk.sh"
