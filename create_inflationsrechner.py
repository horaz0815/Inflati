#!/usr/bin/env python3
"""
Inflationsrechner für LibreOffice Calc
Erstellt eine .ods-Datei mit Inflationsberechnungen
"""

from zipfile import ZipFile
from datetime import datetime
import os

def create_ods_file(filename="Inflationsrechner.ods"):
    """Erstellt eine ODS-Datei für den Inflationsrechner"""

    # Inflationsraten 2011-2025
    rates = {
        2011: 2.60, 2012: 4.91, 2013: 4.00, 2014: 3.50, 2015: 2.00,
        2016: 17.75, 2017: 1.60, 2018: 2.80, 2019: 4.15, 2020: 2.82,
        2021: 2.25, 2022: 3.80, 2023: 9.69, 2024: 9.72, 2025: 4.31
    }

    # Varianten für 2026-2030
    variants = {
        2026: {"SR+UR": 3.07, "HR+GF+WD": 3.90},
        2027: {"SR+UR": 0.00, "HR+GF+WD": 0.00},
        2028: {"SR+UR": 0.00, "HR+GF+WD": 0.00},
        2029: {"SR+UR": 0.00, "HR+GF+WD": 0.00},
        2030: {"SR+UR": 0.00, "HR+GF+WD": 0.00}
    }

    # XML-Inhalte für ODS-Datei
    mimetype = "application/vnd.oasis.opendocument.spreadsheet"

    manifest = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.spreadsheet"/>
  <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="settings.xml" manifest:media-type="text/xml"/>
</manifest:manifest>'''

    meta = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                      xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
                      xmlns:dc="http://purl.org/dc/elements/1.1/"
                      office:version="1.2">
  <office:meta>
    <meta:generator>Python ODS Generator</meta:generator>
    <dc:title>Inflationsrechner</dc:title>
    <dc:description>Berechnung inflationsangepasster Beträge</dc:description>
    <dc:date>{datetime.now().isoformat()}</dc:date>
  </office:meta>
</office:document-meta>'''

    settings = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                          xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"
                          office:version="1.2">
  <office:settings>
    <config:config-item-set config:name="ooo:view-settings">
      <config:config-item config:name="VisibleAreaTop" config:type="int">0</config:config-item>
      <config:config-item config:name="VisibleAreaLeft" config:type="int">0</config:config-item>
    </config:config-item-set>
  </office:settings>
</office:document-settings>'''

    styles = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                        xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
                        xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
                        office:version="1.2">
  <office:styles>
    <style:style style:name="Default" style:family="table-cell"/>
  </office:styles>
  <office:automatic-styles/>
  <office:master-styles/>
</office:document-styles>'''

    # Content.xml - Hauptinhalt der Tabelle
    content_header = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                         xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
                         xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                         xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
                         xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
                         xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
                         office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="ce1" style:family="table-cell" style:parent-style-name="Default">
      <style:text-properties fo:font-weight="bold" fo:font-size="14pt"/>
    </style:style>
    <style:style style:name="ce2" style:family="table-cell" style:parent-style-name="Default">
      <style:table-cell-properties fo:background-color="#667eea"/>
      <style:text-properties fo:color="#ffffff" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="ce3" style:family="table-cell" style:parent-style-name="Default">
      <style:table-cell-properties fo:background-color="#e8eaf6"/>
    </style:style>
    <number:number-style style:name="N0">
      <number:number number:decimal-places="2" number:min-integer-digits="1"/>
    </number:number-style>
    <style:style style:name="ce4" style:family="table-cell" style:parent-style-name="Default" style:data-style-name="N0">
      <style:table-cell-properties fo:background-color="#f5f5f5"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:spreadsheet>
'''

    # Rechner-Sheet erstellen
    rechner_sheet = '''      <table:table table:name="Rechner" table:style-name="ta1">
        <!-- Header -->
        <table:table-row>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>💶 INFLATIONSRECHNER</text:p>
          </table:table-cell>
          <table:table-cell/>
        </table:table-row>
        <table:table-row>
          <table:table-cell/>
        </table:table-row>

        <!-- Eingabebereich -->
        <table:table-row>
          <table:table-cell table:style-name="ce1" office:value-type="string">
            <text:p>Basisjahr:</text:p>
          </table:table-cell>
          <table:table-cell office:value-type="float" office:value="2014">
            <text:p>2014</text:p>
          </table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="ce1" office:value-type="string">
            <text:p>Basisbetrag (€):</text:p>
          </table:table-cell>
          <table:table-cell office:value-type="float" office:value="400">
            <text:p>400</text:p>
          </table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell/>
        </table:table-row>

        <!-- Ergebnisse -->
        <table:table-row>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>ANGEPASSTE BETRÄGE FÜR 2026</text:p>
          </table:table-cell>
          <table:table-cell/>
        </table:table-row>
        <table:table-row>
          <table:table-cell/>
        </table:table-row>

        <table:table-row>
          <table:table-cell table:style-name="ce1" office:value-type="string">
            <text:p>SR+UR (LGrp 1,2,3,6):</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="ce4" table:formula="of:=Rechner.B4*Berechnungen.B2" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
        </table:table-row>

        <table:table-row>
          <table:table-cell table:style-name="ce1" office:value-type="string">
            <text:p>HR+GF+WD (LGrp 4,5):</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="ce4" table:formula="of:=Rechner.B4*Berechnungen.C2" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
        </table:table-row>

      </table:table>
'''

    # Inflationsraten-Sheet
    rates_sheet = '''      <table:table table:name="Inflationsraten" table:style-name="ta1">
        <table:table-row>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>Jahr</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>Rate (%)</text:p>
          </table:table-cell>
        </table:table-row>
'''

    for year in range(2011, 2026):
        rate = rates[year]
        rates_sheet += f'''        <table:table-row>
          <table:table-cell office:value-type="float" office:value="{year}">
            <text:p>{year}</text:p>
          </table:table-cell>
          <table:table-cell office:value-type="float" office:value="{rate}">
            <text:p>{rate}</text:p>
          </table:table-cell>
        </table:table-row>
'''

    rates_sheet += '''      </table:table>
'''

    # Varianten-Sheet
    variants_sheet = '''      <table:table table:name="Varianten" table:style-name="ta1">
        <table:table-row>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>Jahr</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>SR+UR (%)</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>HR+GF+WD (%)</text:p>
          </table:table-cell>
        </table:table-row>
'''

    for year in range(2026, 2031):
        sr_rate = variants[year]["SR+UR"]
        hr_rate = variants[year]["HR+GF+WD"]
        variants_sheet += f'''        <table:table-row>
          <table:table-cell office:value-type="float" office:value="{year}">
            <text:p>{year}</text:p>
          </table:table-cell>
          <table:table-cell office:value-type="float" office:value="{sr_rate}">
            <text:p>{sr_rate}</text:p>
          </table:table-cell>
          <table:table-cell office:value-type="float" office:value="{hr_rate}">
            <text:p>{hr_rate}</text:p>
          </table:table-cell>
        </table:table-row>
'''

    variants_sheet += '''      </table:table>
'''

    # Berechnungs-Sheet (versteckte Hilfsberechnungen)
    calc_sheet = '''      <table:table table:name="Berechnungen" table:style-name="ta1">
        <table:table-row>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>Beschreibung</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>Faktor SR+UR</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="ce2" office:value-type="string">
            <text:p>Faktor HR+GF+WD</text:p>
          </table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell office:value-type="string">
            <text:p>Multiplikationsfaktor für Basisjahr → 2026</text:p>
          </table:table-cell>
          <table:table-cell table:formula="of:=IF(Rechner.B3=2026,1,IF(Rechner.B3&lt;2026,PRODUCT((1+OFFSET(Inflationsraten.$B$1,Rechner.B3-2010,0,MIN(2026,2025)-Rechner.B3,1)/100))*(1+INDEX(Varianten.$B:$B,Rechner.B3-2025)/100)^MAX(0,Rechner.B3-2025),1/PRODUCT((1+OFFSET(Inflationsraten.$B$1,2026-2010,0,Rechner.B3-2026,1)/100))))" office:value-type="float">
            <text:p>1</text:p>
          </table:table-cell>
          <table:table-cell table:formula="of:=IF(Rechner.B3=2026,1,IF(Rechner.B3&lt;2026,PRODUCT((1+OFFSET(Inflationsraten.$B$1,Rechner.B3-2010,0,MIN(2026,2025)-Rechner.B3,1)/100))*(1+INDEX(Varianten.$C:$C,Rechner.B3-2025)/100)^MAX(0,Rechner.B3-2025),1/PRODUCT((1+OFFSET(Inflationsraten.$B$1,2026-2010,0,Rechner.B3-2026,1)/100))))" office:value-type="float">
            <text:p>1</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>
'''

    content_footer = '''    </office:spreadsheet>
  </office:body>
</office:document-content>'''

    # Alles zusammenfügen
    content = content_header + rechner_sheet + rates_sheet + variants_sheet + calc_sheet + content_footer

    # ODS-Datei erstellen (ist eigentlich eine ZIP-Datei)
    with ZipFile(filename, 'w') as ods:
        ods.writestr('mimetype', mimetype)
        ods.writestr('META-INF/manifest.xml', manifest)
        ods.writestr('meta.xml', meta)
        ods.writestr('settings.xml', settings)
        ods.writestr('styles.xml', styles)
        ods.writestr('content.xml', content)

    print(f"✓ {filename} wurde erfolgreich erstellt!")
    return filename

if __name__ == "__main__":
    create_ods_file()
