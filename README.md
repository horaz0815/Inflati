# Weiner Gebäudeservice - Angebots-App

Android-App für die Erstellung von Reinigungsangeboten während Kundenbesichtigungen.

## Features

- **Kundenverwaltung**: Erfassung aller relevanten Kundendaten (Name, Adresse, Kontaktdaten)
- **Reinigungsbereiche**: Hinzufügen mehrerer Reinigungsbereiche mit Details:
  - Bereichsname
  - Fläche in m²
  - Art der Reinigung (Büro, Sanitär, Treppen, Glas, Sonder)
  - Reinigungshäufigkeit (täglich, wöchentlich, etc.)
  - Preis pro m²
- **Automatische Kalkulation**: Berechnung monatlicher und jährlicher Gesamtpreise
- **PDF-Generierung**: Professionelle Angebote als PDF nach Firmenvorlage
- **E-Mail-Versand**: Direkter Versand des Angebots per E-Mail an Kunden

## Technische Details

- **Sprache**: Kotlin
- **Minimum SDK**: 24 (Android 7.0)
- **Target SDK**: 34 (Android 14)
- **PDF-Bibliothek**: iText 7
- **UI**: Material Design Components

## Projektstruktur

```
app/
├── src/main/
│   ├── java/com/weiner/quotesapp/
│   │   ├── models/              # Datenmodelle
│   │   │   ├── Customer.kt
│   │   │   ├── CleaningArea.kt
│   │   │   └── Quote.kt
│   │   ├── adapters/            # RecyclerView Adapter
│   │   │   └── CleaningAreaAdapter.kt
│   │   ├── utils/               # Hilfsfunktionen
│   │   │   └── PdfGenerator.kt
│   │   └── MainActivity.kt      # Hauptaktivität
│   ├── res/
│   │   ├── layout/              # UI Layouts
│   │   ├── values/              # Strings, Colors, Themes
│   │   └── xml/                 # FileProvider Konfiguration
│   └── AndroidManifest.xml
└── build.gradle

```

## Installation & Build

1. Klonen Sie das Repository:
```bash
git clone <repository-url>
```

2. Öffnen Sie das Projekt in Android Studio

3. Synchronisieren Sie Gradle:
   - Android Studio führt dies automatisch aus
   - Oder manuell: File → Sync Project with Gradle Files

4. Bauen Sie die App:
```bash
./gradlew assembleDebug
```

5. Installieren Sie die App auf einem Gerät oder Emulator:
```bash
./gradlew installDebug
```

## Verwendung

### Angebot erstellen

1. **Kundendaten eingeben**:
   - Name
   - Adresse
   - PLZ/Ort
   - E-Mail
   - Telefonnummer

2. **Reinigungsbereiche hinzufügen**:
   - Klicken Sie auf "Bereich hinzufügen"
   - Geben Sie die Details ein
   - Speichern Sie den Bereich

3. **Angebot generieren**:
   - Überprüfen Sie die Gesamtkosten
   - Klicken Sie auf "Angebot erstellen"
   - Das PDF wird automatisch geöffnet

4. **Per E-Mail versenden**:
   - Klicken Sie auf "Per E-Mail senden"
   - Wählen Sie Ihre E-Mail-App
   - Senden Sie das Angebot

### Preiskalkulation

Die App berechnet automatisch die monatlichen Kosten basierend auf:
- Fläche (m²) × Preis pro m² × Häufigkeitsfaktor

**Häufigkeitsfaktoren**:
- Täglich: 22 (Arbeitstage/Monat)
- 3x pro Woche: 13
- 2x pro Woche: 8
- Wöchentlich: 4
- 14-tägig: 2
- Monatlich: 1

## Anpassungen

### Firmendaten ändern

Bearbeiten Sie `app/src/main/java/com/weiner/quotesapp/utils/PdfGenerator.kt`:

```kotlin
private fun addCompanyHeader(document: Document) {
    val companyName = Paragraph("Ihre Firma GmbH")
    val companyInfo = Paragraph(
        "Ihre Straße 123\n" +
        "Ihre PLZ Ort\n" +
        "Tel: +49 ...\n" +
        "E-Mail: ..."
    )
    // ...
}
```

### Reinigungsarten anpassen

Bearbeiten Sie `app/src/main/res/values/strings.xml`:

```xml
<string-array name="area_types">
    <item>Ihre Reinigungsart 1</item>
    <item>Ihre Reinigungsart 2</item>
    <!-- ... -->
</string-array>
```

### Farben anpassen

Bearbeiten Sie `app/src/main/res/values/colors.xml`:

```xml
<color name="primary">#1976D2</color>
<color name="accent">#FF9800</color>
```

## Berechtigungen

Die App benötigt folgende Berechtigungen:
- `WRITE_EXTERNAL_STORAGE` (nur Android 12 und älter)
- `READ_EXTERNAL_STORAGE` (nur Android 12 und älter)
- `INTERNET` (für E-Mail-Versand)

## Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue im Repository.

## Lizenz

© 2024 Weiner Gebäudeservice GmbH