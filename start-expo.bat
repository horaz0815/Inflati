@echo off
echo 🚀 Speiseplan-App mit Expo Go starten
echo ======================================
echo.

REM Prüfen ob node_modules existiert
if not exist "node_modules" (
    echo 📦 Dependencies werden installiert...
    call npm install
    echo.
)

REM Prüfen ob Assets existieren
if not exist "assets\icon.png" (
    echo ⚠️  Assets fehlen!
    echo.
    echo Assets werden erstellt...
    call create-assets.bat
    echo.
)

echo ✅ Alles bereit!
echo.
echo 📱 So testen Sie die App:
echo.
echo 1. Installieren Sie Expo Go auf Ihrem Smartphone:
echo    📱 Android: https://play.google.com/store/apps/details?id=host.exp.exponent
echo    🍎 iOS: https://apps.apple.com/app/expo-go/id982107779
echo.
echo 2. Scannen Sie den QR-Code der gleich erscheint
echo.
echo 3. Die App öffnet sich automatisch in Expo Go!
echo.
echo ======================================
echo 🔥 Dev Server wird gestartet...
echo.

REM Expo Dev Server starten
call npm start
