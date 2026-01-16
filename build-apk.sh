#!/bin/bash

echo "📱 APK Build für Speiseplan-App"
echo "================================"
echo ""

# Farben für Output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Schritt 1: Assets erstellen
echo -e "${YELLOW}Schritt 1/5: Assets erstellen...${NC}"
if [ ! -f "assets/icon.png" ]; then
    echo "Assets werden erstellt..."
    ./create-assets.sh
    echo ""
else
    echo -e "${GREEN}✓ Assets bereits vorhanden${NC}"
    echo ""
fi

# Schritt 2: Dependencies installieren
echo -e "${YELLOW}Schritt 2/5: Dependencies überprüfen...${NC}"
if [ ! -d "node_modules" ]; then
    echo "Dependencies werden installiert..."
    npm install
    echo ""
else
    echo -e "${GREEN}✓ Dependencies bereits installiert${NC}"
    echo ""
fi

# Schritt 3: EAS CLI prüfen/installieren
echo -e "${YELLOW}Schritt 3/5: EAS CLI überprüfen...${NC}"
if ! command -v eas &> /dev/null; then
    echo "EAS CLI wird installiert..."
    npm install -g eas-cli
    echo ""
else
    echo -e "${GREEN}✓ EAS CLI bereits installiert${NC}"
    echo ""
fi

# Schritt 4: Bei Expo anmelden
echo -e "${YELLOW}Schritt 4/5: Bei Expo anmelden...${NC}"
echo "Bitte melden Sie sich mit Ihrem Expo-Account an"
echo "(Falls Sie noch keinen haben: https://expo.dev/signup)"
echo ""
eas whoami &> /dev/null
if [ $? -ne 0 ]; then
    eas login
else
    echo -e "${GREEN}✓ Bereits angemeldet als:${NC}"
    eas whoami
fi
echo ""

# Schritt 5: APK bauen
echo -e "${YELLOW}Schritt 5/5: APK wird gebaut...${NC}"
echo ""
echo "Dies kann 10-15 Minuten dauern ☕"
echo "Der Build läuft in der Expo Cloud."
echo ""

eas build --platform android --profile preview

# Build-Status prüfen
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}✓ Build erfolgreich!${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "📥 APK herunterladen:"
    echo ""
    echo "1. Öffnen Sie den Link, der oben angezeigt wurde"
    echo "2. ODER gehen Sie zu: https://expo.dev/"
    echo "3. Navigieren Sie zu 'Builds'"
    echo "4. Laden Sie die APK herunter"
    echo ""
    echo "📱 Auf Smartphone installieren:"
    echo "1. Übertragen Sie die APK auf Ihr Android-Gerät"
    echo "2. Öffnen Sie die APK-Datei"
    echo "3. Erlauben Sie 'Installation aus unbekannten Quellen'"
    echo "4. Installieren Sie die App"
    echo ""
    echo -e "${YELLOW}⚠️  WICHTIG: Konfigurieren Sie Firebase vor dem ersten Start!${NC}"
    echo "   Siehe: FIREBASE_SETUP.md"
    echo ""
else
    echo ""
    echo -e "${RED}================================${NC}"
    echo -e "${RED}✗ Build fehlgeschlagen${NC}"
    echo -e "${RED}================================${NC}"
    echo ""
    echo "Mögliche Lösungen:"
    echo "1. Überprüfen Sie die Fehlermeldung oben"
    echo "2. Stellen Sie sicher, dass alle Assets vorhanden sind"
    echo "3. Führen Sie 'npm install' erneut aus"
    echo "4. Siehe BUILD_APK.md für Troubleshooting"
    echo ""
    exit 1
fi
