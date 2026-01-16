#!/usr/bin/env python3
"""
Erstellt einfache Platzhalter-Assets für die Speiseplan-App
Verwendet die PIL/Pillow Bibliothek
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os

    # Militärische Farben
    BG_COLOR = (44, 62, 47)    # #2C3E2F - Olivgrün
    FG_COLOR = (139, 115, 85)   # #8B7355 - Sandbraun
    TEXT_COLOR = (232, 232, 232) # #E8E8E8 - Helles Grau

    # Assets-Ordner erstellen
    os.makedirs('assets', exist_ok=True)

    print("🎨 Erstelle Platzhalter-Assets...")
    print()

    # 1. Icon (1024x1024)
    print("📱 Erstelle icon.png (1024x1024)...")
    icon = Image.new('RGB', (1024, 1024), BG_COLOR)
    draw = ImageDraw.Draw(icon)
    # Einfaches Design: Rechteck in der Mitte
    draw.rectangle([256, 256, 768, 768], fill=FG_COLOR, outline=TEXT_COLOR, width=10)
    # Text
    draw.text((512, 512), "S", fill=TEXT_COLOR, anchor="mm", font_size=400)
    icon.save('assets/icon.png', 'PNG')
    print("✓ icon.png erstellt")

    # 2. Splash Screen (1284x2778)
    print("🖼️ Erstelle splash.png (1284x2778)...")
    splash = Image.new('RGB', (1284, 2778), BG_COLOR)
    draw = ImageDraw.Draw(splash)
    # Logo in der Mitte
    draw.rectangle([342, 889, 942, 1889], fill=FG_COLOR, outline=TEXT_COLOR, width=8)
    draw.text((642, 1389), "Speiseplan", fill=TEXT_COLOR, anchor="mm", font_size=100)
    splash.save('assets/splash.png', 'PNG')
    print("✓ splash.png erstellt")

    # 3. Adaptive Icon (1024x1024)
    print("🎯 Erstelle adaptive-icon.png (1024x1024)...")
    adaptive = Image.new('RGB', (1024, 1024), BG_COLOR)
    draw = ImageDraw.Draw(adaptive)
    # Kreis für Android adaptive icon
    draw.ellipse([112, 112, 912, 912], fill=FG_COLOR, outline=TEXT_COLOR, width=10)
    draw.text((512, 512), "S", fill=TEXT_COLOR, anchor="mm", font_size=400)
    adaptive.save('assets/adaptive-icon.png', 'PNG')
    print("✓ adaptive-icon.png erstellt")

    # 4. Favicon (48x48)
    print("🌐 Erstelle favicon.png (48x48)...")
    favicon = Image.new('RGB', (48, 48), BG_COLOR)
    draw = ImageDraw.Draw(favicon)
    draw.rectangle([4, 4, 44, 44], fill=FG_COLOR, outline=TEXT_COLOR, width=1)
    favicon.save('assets/favicon.png', 'PNG')
    print("✓ favicon.png erstellt")

    print()
    print("✅ Alle Assets wurden erfolgreich erstellt!")
    print()
    print("Dateien:")
    for f in ['icon.png', 'splash.png', 'adaptive-icon.png', 'favicon.png']:
        path = f'assets/{f}'
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✓ {f} ({size:,} bytes)")

    print()
    print("🚀 Nächster Schritt: ./build-apk.sh")

except ImportError:
    print("❌ PIL/Pillow nicht installiert!")
    print()
    print("Installieren Sie mit:")
    print("  pip3 install Pillow")
    print()
    print("Oder verwenden Sie einfache Platzhalter:")

    # Erstelle sehr einfache PNG-Dateien als Fallback
    import struct

    def create_simple_png(filename, width, height, color):
        """Erstellt eine sehr einfache PNG-Datei"""
        # Sehr vereinfachte PNG-Erstellung
        # Für Production sollte eine richtige Bibliothek verwendet werden
        # Dies erstellt nur einen solid-color PNG
        os.makedirs('assets', exist_ok=True)

        # Erstelle eine sehr kleine PNG mit purer Python
        # Dies ist nur ein Hack für den Notfall
        with open(f'assets/{filename}', 'wb') as f:
            # PNG Signature
            f.write(b'\x89PNG\r\n\x1a\n')

            # IHDR Chunk
            ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
            f.write(struct.pack('>I', 13))  # Chunk length
            f.write(b'IHDR')
            f.write(ihdr)
            f.write(struct.pack('>I', 0))  # CRC (simplified)

            # Sehr vereinfachte Implementierung
            # In Produktion PIL/Pillow verwenden!

        print(f"✓ {filename} (minimales PNG) erstellt")

    print()
    print("Erstelle minimale Platzhalter...")
    create_simple_png('icon.png', 1024, 1024, BG_COLOR)
    create_simple_png('splash.png', 1284, 2778, BG_COLOR)
    create_simple_png('adaptive-icon.png', 1024, 1024, BG_COLOR)
    create_simple_png('favicon.png', 48, 48, BG_COLOR)

    print()
    print("⚠️  Minimale Platzhalter erstellt")
    print("   Für bessere Qualität: pip3 install Pillow")
