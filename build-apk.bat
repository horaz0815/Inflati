@echo off
echo 📱 APK Build für Speiseplan-App
echo ================================
echo.

REM Schritt 1: Assets erstellen
echo Schritt 1/5: Assets erstellen...
if not exist "assets\icon.png" (
    echo Assets werden erstellt...
    call create-assets.bat
    echo.
) else (
    echo ✓ Assets bereits vorhanden
    echo.
)

REM Schritt 2: Dependencies installieren
echo Schritt 2/5: Dependencies überprüfen...
if not exist "node_modules" (
    echo Dependencies werden installiert...
    call npm install
    echo.
) else (
    echo ✓ Dependencies bereits installiert
    echo.
)

REM Schritt 3: EAS CLI prüfen/installieren
echo Schritt 3/5: EAS CLI überprüfen...
where eas >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo EAS CLI wird installiert...
    call npm install -g eas-cli
    echo.
) else (
    echo ✓ EAS CLI bereits installiert
    echo.
)

REM Schritt 4: Bei Expo anmelden
echo Schritt 4/5: Bei Expo anmelden...
echo Bitte melden Sie sich mit Ihrem Expo-Account an
echo (Falls Sie noch keinen haben: https://expo.dev/signup)
echo.
call eas whoami >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    call eas login
) else (
    echo ✓ Bereits angemeldet als:
    call eas whoami
)
echo.

REM Schritt 5: APK bauen
echo Schritt 5/5: APK wird gebaut...
echo.
echo Dies kann 10-15 Minuten dauern ☕
echo Der Build läuft in der Expo Cloud.
echo.

call eas build --platform android --profile preview

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================
    echo ✓ Build erfolgreich!
    echo ================================
    echo.
    echo 📥 APK herunterladen:
    echo.
    echo 1. Öffnen Sie den Link, der oben angezeigt wurde
    echo 2. ODER gehen Sie zu: https://expo.dev/
    echo 3. Navigieren Sie zu 'Builds'
    echo 4. Laden Sie die APK herunter
    echo.
    echo 📱 Auf Smartphone installieren:
    echo 1. Übertragen Sie die APK auf Ihr Android-Gerät
    echo 2. Öffnen Sie die APK-Datei
    echo 3. Erlauben Sie 'Installation aus unbekannten Quellen'
    echo 4. Installieren Sie die App
    echo.
    echo ⚠️  WICHTIG: Konfigurieren Sie Firebase vor dem ersten Start!
    echo    Siehe: FIREBASE_SETUP.md
    echo.
) else (
    echo.
    echo ================================
    echo ✗ Build fehlgeschlagen
    echo ================================
    echo.
    echo Mögliche Lösungen:
    echo 1. Überprüfen Sie die Fehlermeldung oben
    echo 2. Stellen Sie sicher, dass alle Assets vorhanden sind
    echo 3. Führen Sie 'npm install' erneut aus
    echo 4. Siehe BUILD_APK.md für Troubleshooting
    echo.
)

pause
