#!/usr/bin/env python3
"""
KIOWA Flottensteuerung V47 - Military Modern Edition
Generiert eine LibreOffice Calc Datei für die Überwachung von Flugzeug-Flotten
Design: Military Modern Style mit abgestimmter Farbpalette
"""

from zipfile import ZipFile
from datetime import datetime
import xml.etree.ElementTree as ET

# Flotte: 12 aktive Einheiten (3C-OF und 3C-OG werden ignoriert)
FLEET = ['3C-OA', '3C-OB', '3C-OC', '3C-OD', '3C-OE', '3C-OH',
         '3C-OI', '3C-OJ', '3C-OK', '3C-OL', 'RES1', 'RES2']

# Monatsnamen und Tage pro Monat (365 Tage, kein Schaltjahr)
MONTHS = [
    ('Januar', 31), ('Februar', 28), ('März', 31), ('April', 30),
    ('Mai', 31), ('Juni', 30), ('Juli', 31), ('August', 31),
    ('September', 30), ('Oktober', 31), ('November', 30), ('Dezember', 31)
]

WARTUNGSTYPEN = ['25WE', '50WE', '75WE', '100WE', '300WE', '1200WE']

# Military Modern Color Palette
COLORS = {
    'dark_slate': '#2C3E50',      # Dunkles Schiefergrau - Haupt-Header
    'military_green': '#4A5D23',  # Militär-Grün - Wichtige Header
    'olive': '#556B2F',           # Olivgrün - Sekundäre Elemente
    'steel_gray': '#5D6D7E',      # Stahlgrau - Berechnete Werte
    'light_gray': '#ECF0F1',      # Hellgrau - Eingabefelder
    'warning_orange': '#D35400',  # Warnorange - Warnungen
    'danger_red': '#C0392B',      # Gefahr-Rot - Kritische Warnungen
    'success_green': '#27AE60',   # Erfolg-Grün - Positive Werte
    'dark_green': '#1E8449',      # Dunkelgrün - Summen
    'charcoal': '#34495E',        # Anthrazit - Alternative Header
    'sand': '#D7DBDD',            # Sand - Alternative Eingabe
    'black': '#1C2833',           # Schwarz - Text auf hellen Hintergründen
    'white': '#FFFFFF',           # Weiß - Text auf dunklen Hintergründen
    'amber': '#F39C12',           # Bernstein - Vortrag/Wichtig
}


def get_military_styles():
    """Erstellt das Styles-XML mit Military Modern Design"""

    return '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                        xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
                        xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
                        office:version="1.2">
  <office:styles>
    <style:style style:name="Default" style:family="table-cell">
      <style:table-cell-properties fo:border="0.05pt solid #2C3E50"/>
      <style:text-properties style:font-name="Liberation Sans" fo:font-size="10pt"/>
    </style:style>
  </office:styles>
  <office:automatic-styles/>
  <office:master-styles/>
</office:document-styles>'''


def get_content_styles():
    """Erstellt die Content-Styles mit Military Modern Design"""

    return f'''  <office:automatic-styles>
    <!-- Main Header Style - Dark Slate -->
    <style:style style:name="header" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['dark_slate']}"
                                    fo:border="0.5pt solid {COLORS['black']}"
                                    fo:padding="0.08cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"
                           fo:font-size="11pt"
                           style:font-name="Liberation Sans"/>
    </style:style>

    <!-- Military Green Header -->
    <style:style style:name="header_green" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['military_green']}"
                                    fo:border="0.5pt solid {COLORS['black']}"
                                    fo:padding="0.08cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"
                           fo:font-size="12pt"
                           style:font-name="Liberation Sans"/>
    </style:style>

    <!-- Overview Title -->
    <style:style style:name="title" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['black']}"
                                    fo:border="1pt solid {COLORS['military_green']}"
                                    fo:padding="0.1cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"
                           fo:font-size="14pt"
                           style:font-name="Liberation Sans"/>
    </style:style>

    <!-- Input Field Style - Light Gray -->
    <style:style style:name="input" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['light_gray']}"
                                    fo:border="0.5pt solid {COLORS['steel_gray']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['black']}"
                           fo:font-size="10pt"/>
    </style:style>

    <!-- Calculated Field Style - Steel Gray -->
    <style:style style:name="calculated" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['steel_gray']}"
                                    fo:border="0.5pt solid {COLORS['dark_slate']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-size="10pt"
                           fo:font-weight="bold"/>
    </style:style>

    <!-- Vortrag Style - Amber Warning -->
    <style:style style:name="vortrag" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['amber']}"
                                    fo:border="1pt solid {COLORS['warning_orange']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['black']}"
                           fo:font-weight="bold"
                           fo:font-size="11pt"/>
    </style:style>

    <!-- Summe Style - Dark Green -->
    <style:style style:name="summe" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['dark_green']}"
                                    fo:border="1pt solid {COLORS['success_green']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"
                           fo:font-size="11pt"/>
    </style:style>

    <!-- Remarks Style - White with border -->
    <style:style style:name="remarks" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['white']}"
                                    fo:border="0.5pt solid {COLORS['steel_gray']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['black']}"
                           fo:font-size="9pt"
                           fo:font-style="italic"/>
    </style:style>

    <!-- Date Cell Style - Sand -->
    <style:style style:name="date" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['sand']}"
                                    fo:border="0.5pt solid {COLORS['steel_gray']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['black']}"
                           fo:font-size="9pt"/>
    </style:style>

    <!-- LSN Display Style - Olive -->
    <style:style style:name="lsn_display" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['olive']}"
                                    fo:border="0.5pt solid {COLORS['military_green']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"
                           fo:font-size="12pt"
                           style:font-name="Liberation Mono"/>
    </style:style>

    <!-- Warning Style - Orange -->
    <style:style style:name="warning" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['warning_orange']}"
                                    fo:border="1pt solid {COLORS['danger_red']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"
                           fo:font-size="11pt"/>
    </style:style>

    <!-- Aircraft ID Style - Charcoal -->
    <style:style style:name="aircraft_id" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['charcoal']}"
                                    fo:border="1pt solid {COLORS['dark_slate']}"
                                    fo:padding="0.08cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"
                           fo:font-size="11pt"
                           style:font-name="Liberation Mono"/>
    </style:style>

    <!-- Success Style - Green -->
    <style:style style:name="success" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['success_green']}"
                                    fo:border="0.5pt solid {COLORS['dark_green']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"/>
    </style:style>

    <!-- Number Display - Monospace -->
    <style:style style:name="number" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['light_gray']}"
                                    fo:border="0.5pt solid {COLORS['steel_gray']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['black']}"
                           fo:font-size="10pt"
                           style:font-name="Liberation Mono"/>
    </style:style>

    <!-- Month Header Style -->
    <style:style style:name="month_header" style:family="table-cell">
      <style:table-cell-properties fo:background-color="{COLORS['military_green']}"
                                    fo:border="0.5pt solid {COLORS['black']}"
                                    fo:padding="0.05cm"/>
      <style:text-properties fo:color="{COLORS['white']}"
                           fo:font-weight="bold"
                           fo:font-size="9pt"/>
    </style:style>
  </office:automatic-styles>'''


def create_logbook_sheet(aircraft_id):
    """Erstellt ein Logbuch-Blatt für ein Flugzeug mit Military Design"""

    sheet_xml = f'''      <table:table table:name="{aircraft_id}" table:style-name="ta1">
        <!-- Titel-Zeile -->
        <table:table-row table:style-name="ro1">
          <table:table-cell table:number-columns-spanned="17" table:style-name="title" office:value-type="string">
            <text:p>🚁 LOGBUCH {aircraft_id} - KIOWA V47</text:p>
          </table:table-cell>
        </table:table-row>

        <!-- Kopfzeile -->
        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Monat</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Tag</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>HH</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>MM</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>LDG</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>CYC</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>Fuel-INL</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>Fuel-AUSL</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>REMARKS</text:p>
          </table:table-cell>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Zellen-LSN HH</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Zellen-LSN MM</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>TW-LSN HH</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>TW-LSN MM</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>TW-CORR HH</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>TW-CORR MM</text:p>
          </table:table-cell>
        </table:table-row>
'''

    # Zeile 3: Übertrag (manuell einzutragen) - VORTRAG in Bernstein
    sheet_xml += '''        <table:table-row>
          <table:table-cell table:style-name="vortrag" office:value-type="string">
            <text:p>⚠ ÜBERTRAG</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="vortrag"/>
          <table:table-cell table:style-name="vortrag"/>
          <table:table-cell table:style-name="vortrag"/>
          <table:table-cell table:style-name="vortrag"/>
          <table:table-cell table:style-name="vortrag"/>
          <table:table-cell table:style-name="vortrag"/>
          <table:table-cell table:style-name="vortrag"/>
          <table:table-cell table:style-name="vortrag"/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
        </table:table-row>
'''

    # Zeile 4: SUMME mit Formeln - in Dunkelgrün
    sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="summe" office:value-type="string">
            <text:p>✓ SUMME</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe"/>
          <table:table-cell table:style-name="summe" table:formula="of:=SUM({aircraft_id}.C5:{aircraft_id}.C370)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe" table:formula="of:=SUM({aircraft_id}.D5:{aircraft_id}.D370)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe" table:formula="of:=SUM({aircraft_id}.E5:{aircraft_id}.E370)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe" table:formula="of:=SUM({aircraft_id}.F5:{aircraft_id}.F370)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe" table:formula="of:=SUM({aircraft_id}.G5:{aircraft_id}.G370)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe" table:formula="of:=SUM({aircraft_id}.H5:{aircraft_id}.H370)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe"/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell table:style-name="lsn_display" table:formula="of:={aircraft_id}.L3+SUM({aircraft_id}.C5:{aircraft_id}.C370)+INT(({aircraft_id}.M3+SUM({aircraft_id}.D5:{aircraft_id}.D370))/60)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="lsn_display" table:formula="of:=MOD({aircraft_id}.M3+SUM({aircraft_id}.D5:{aircraft_id}.D370);60)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="lsn_display" table:formula="of:={aircraft_id}.N3+SUM({aircraft_id}.C5:{aircraft_id}.C370)+INT(({aircraft_id}.O3+SUM({aircraft_id}.D5:{aircraft_id}.D370))/60)+{aircraft_id}.P3+INT(({aircraft_id}.O3+{aircraft_id}.Q3)/60)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="lsn_display" table:formula="of:=MOD({aircraft_id}.O3+SUM({aircraft_id}.D5:{aircraft_id}.D370)+{aircraft_id}.Q3;60)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe"/>
          <table:table-cell table:style-name="summe"/>
        </table:table-row>
'''

    # Datumszeilen für alle 365 Tage
    row_num = 5
    for month_name, days in MONTHS:
        for day in range(1, days + 1):
            sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="date" office:value-type="string">
            <text:p>{month_name}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="date" office:value-type="float" office:value="{day}">
            <text:p>{day}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="remarks"/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell table:style-name="calculated" table:formula="of:=IF({aircraft_id}.C{row_num}=&quot;&quot;;&quot;&quot;;{aircraft_id}.L3+SUM({aircraft_id}.C$5:{aircraft_id}.C{row_num})+INT(({aircraft_id}.M3+SUM({aircraft_id}.D$5:{aircraft_id}.D{row_num}))/60))" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=IF({aircraft_id}.C{row_num}=&quot;&quot;;&quot;&quot;;MOD({aircraft_id}.M3+SUM({aircraft_id}.D$5:{aircraft_id}.D{row_num});60))" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=IF({aircraft_id}.C{row_num}=&quot;&quot;;&quot;&quot;;{aircraft_id}.N3+SUM({aircraft_id}.C$5:{aircraft_id}.C{row_num})+INT(({aircraft_id}.O3+SUM({aircraft_id}.D$5:{aircraft_id}.D{row_num}))/60)+{aircraft_id}.P3+INT(({aircraft_id}.O3+{aircraft_id}.Q3)/60))" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=IF({aircraft_id}.C{row_num}=&quot;&quot;;&quot;&quot;;MOD({aircraft_id}.O3+SUM({aircraft_id}.D$5:{aircraft_id}.D{row_num})+{aircraft_id}.Q3;60))" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
        </table:table-row>
'''
            row_num += 1

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_overview_sheet():
    """Erstellt das OVERVIEW-Blatt mit Military Design"""

    sheet_xml = '''      <table:table table:name="OVERVIEW" table:style-name="ta1">
        <!-- Titel -->
        <table:table-row>
          <table:table-cell table:number-columns-spanned="13" table:style-name="title" office:value-type="string">
            <text:p>⚙ KIOWA V47 - KOMMANDOZENTRALE</text:p>
          </table:table-cell>
        </table:table-row>

        <!-- Header -->
        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Kennzeichen</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Flugklarheit</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>BDL</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>KONFIG</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Standort</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>LSN IST</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>TW-LSN IST</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Steuerung offen (Aktuell)</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Steuerung offen (Nächstes)</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>COUNTDOWN WE</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>ANMERKUNGEN</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Wartung (Stunden)</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Wartung (Planung)</text:p>
          </table:table-cell>
        </table:table-row>
'''

    row_num = 3
    for aircraft in FLEET:
        sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="aircraft_id" office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="string">
            <text:p>VB</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="warning" table:formula="of:=IF(TODAY()-DATE(2024;1;1)&gt;14;&quot;BDL&quot;;&quot;&quot;)" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="lsn_display" table:formula="of:={aircraft}.L4&amp;&quot;:&quot;&amp;TEXT({aircraft}.M4;&quot;00&quot;)" office:value-type="string">
            <text:p>0:00</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="lsn_display" table:formula="of:={aircraft}.N4&amp;&quot;:&quot;&amp;TEXT({aircraft}.O4;&quot;00&quot;)" office:value-type="string">
            <text:p>0:00</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated"/>
          <table:table-cell table:style-name="calculated"/>
          <table:table-cell table:style-name="warning"/>
          <table:table-cell table:style-name="remarks"/>
          <table:table-cell table:style-name="calculated"/>
          <table:table-cell table:style-name="calculated"/>
        </table:table-row>
'''
        row_num += 1

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_statistik_sheet():
    """Erstellt das STATISTIK-Blatt mit Military Design"""

    sheet_xml = '''      <table:table table:name="STATISTIK" table:style-name="ta1">
        <!-- Titel -->
        <table:table-row>
          <table:table-cell table:number-columns-spanned="14" table:style-name="title" office:value-type="string">
            <text:p>📊 STATISTIK - FLOTTEN-AUSWERTUNG</text:p>
          </table:table-cell>
        </table:table-row>

        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Kennzeichen</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Parameter</text:p>
          </table:table-cell>
'''

    # Spalten für jeden Monat + Jahressumme
    for month_name, _ in MONTHS:
        sheet_xml += f'''          <table:table-cell table:style-name="month_header" office:value-type="string">
            <text:p>{month_name[:3].upper()}</text:p>
          </table:table-cell>
'''
    sheet_xml += '''          <table:table-cell table:style-name="header_green" office:value-type="string">
            <text:p>JAHR</text:p>
          </table:table-cell>
        </table:table-row>
'''

    # Für jedes Flugzeug einen 8-Zeilen-Block
    for aircraft in FLEET:
        # Zeile 1: Flugzeit HH
        sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="aircraft_id" office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Flugzeit HH</text:p>
          </table:table-cell>
'''
        for i in range(13):
            sheet_xml += '''          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
        sheet_xml += '        </table:table-row>\n'

        # Weitere Zeilen
        for param in ['Flugzeit MM', 'Landungen', 'Cycles', 'Fuel-INL', 'Fuel-AUSL', 'TW-LSN Monatsende']:
            sheet_xml += f'''        <table:table-row>
          <table:table-cell/>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>{param}</text:p>
          </table:table-cell>
'''
            for i in range(13):
                sheet_xml += '''          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
            sheet_xml += '        </table:table-row>\n'

        # Leerzeile
        sheet_xml += '''        <table:table-row>
          <table:table-cell/>
        </table:table-row>
'''

    # Flotten-Gesamtsumme
    sheet_xml += '''        <table:table-row>
          <table:table-cell table:style-name="summe" office:value-type="string">
            <text:p>FLOTTE GESAMT</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="summe" office:value-type="string">
            <text:p>Flugzeit HH</text:p>
          </table:table-cell>
'''
    for i in range(13):
        sheet_xml += '''          <table:table-cell table:style-name="summe" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
    sheet_xml += '''        </table:table-row>
      </table:table>
'''

    return sheet_xml


def create_steuerung_sheet():
    """Erstellt das STEUERUNG-Blatt mit Military Design"""

    sheet_xml = '''      <table:table table:name="STEUERUNG" table:style-name="ta1">
        <!-- Titel -->
        <table:table-row>
          <table:table-cell table:number-columns-spanned="17" table:style-name="title" office:value-type="string">
            <text:p>⚡ STEUERUNG - SOLL-VORGABEN</text:p>
          </table:table-cell>
        </table:table-row>

        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Kennzeichen</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Vortrag Zelle HH</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Vortrag Zelle MM</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Vortrag TW HH</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Vortrag TW MM</text:p>
          </table:table-cell>
'''

    # Spalten für Monatssoll
    for month_name, _ in MONTHS:
        sheet_xml += f'''          <table:table-cell table:style-name="month_header" office:value-type="string">
            <text:p>{month_name[:3].upper()} Soll</text:p>
          </table:table-cell>
'''

    sheet_xml += '''        </table:table-row>
'''

    # Zeilen für jedes Flugzeug
    for aircraft in FLEET:
        sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="aircraft_id" office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
        # Monatssoll-Werte
        for _ in range(12):
            sheet_xml += '''          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
        sheet_xml += '        </table:table-row>\n'

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_wartungen_sheet():
    """Erstellt das WARTUNGEN-Blatt mit Military Design"""

    sheet_xml = '''      <table:table table:name="WARTUNGEN" table:style-name="ta1">
        <!-- Titel -->
        <table:table-row>
          <table:table-cell table:number-columns-spanned="10" table:style-name="title" office:value-type="string">
            <text:p>🔧 WARTUNGEN - INTERVALL-ÜBERSICHT</text:p>
          </table:table-cell>
        </table:table-row>

        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>LSN-Stufe</text:p>
          </table:table-cell>
'''

    # Spalten für jedes Flugzeug (vereinfacht, nur ein paar)
    for aircraft in FLEET[:6]:
        sheet_xml += f'''          <table:table-cell table:style-name="aircraft_id" office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
'''

    sheet_xml += '''        </table:table-row>
'''

    # Zeilen für LSN-Stufen (25h Schritte, nur bis 500h zur Demo)
    for lsn in range(0, 501, 25):
        sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="float" office:value="{lsn}">
            <text:p>{lsn}h</text:p>
          </table:table-cell>
'''
        for _ in range(6):
            sheet_xml += '''          <table:table-cell table:style-name="calculated"/>
'''
        sheet_xml += '        </table:table-row>\n'

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_we_kw_sheet():
    """Erstellt das WE KW-Blatt mit Military Design"""

    sheet_xml = '''      <table:table table:name="WE KW" table:style-name="ta1">
        <!-- Titel -->
        <table:table-row>
          <table:table-cell table:number-columns-spanned="5" table:style-name="title" office:value-type="string">
            <text:p>📅 WARTUNGSPLANUNG - KALENDERWOCHEN</text:p>
          </table:table-cell>
        </table:table-row>

        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>KW</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Kennzeichen</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Wartungstyp</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>LSN Soll</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Bemerkungen</text:p>
          </table:table-cell>
        </table:table-row>
'''

    # Zeilen für Kalenderwochen 1-53
    for kw in range(1, 54):
        sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="float" office:value="{kw}">
            <text:p>KW {kw:02d}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="number"/>
          <table:table-cell table:style-name="remarks"/>
        </table:table-row>
'''

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_kiowa_ods(filename="KIOWA_V47.ods"):
    """Hauptfunktion: Erstellt die KIOWA ODS-Datei mit Military Modern Design"""

    print("🚁 Erstelle KIOWA Flottensteuerung V47 - MILITARY MODERN EDITION...")

    # Basis-XML-Strukturen
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
    <meta:generator>KIOWA Generator V47 - Military Modern Edition</meta:generator>
    <dc:title>KIOWA V47 Flottensteuerung - Military Modern</dc:title>
    <dc:description>Flottenüberwachung für 12 Luftfahrzeuge - Military Modern Design</dc:description>
    <dc:date>{datetime.now().isoformat()}</dc:date>
  </office:meta>
</office:document-meta>'''

    settings = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                          xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"
                          office:version="1.2">
  <office:settings/>
</office:document-settings>'''

    styles = get_military_styles()

    # Content-Header mit Military Styles
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                         xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
                         xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                         xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
                         xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
                         xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
                         office:version="1.2">
'''

    content += get_content_styles()

    content += '''  <office:body>
    <office:spreadsheet>
'''

    # Sheets generieren
    print("\n  ✓ Erstelle OVERVIEW (Kommandozentrale)...")
    content += create_overview_sheet()

    print("  ✓ Erstelle Einzelblätter für Flotte...")
    for aircraft in FLEET:
        content += create_logbook_sheet(aircraft)
        print(f"    - {aircraft}")

    print("  ✓ Erstelle STATISTIK...")
    content += create_statistik_sheet()

    print("  ✓ Erstelle STEUERUNG...")
    content += create_steuerung_sheet()

    print("  ✓ Erstelle WARTUNGEN...")
    content += create_wartungen_sheet()

    print("  ✓ Erstelle WE KW...")
    content += create_we_kw_sheet()

    # Content-Footer
    content += '''    </office:spreadsheet>
  </office:body>
</office:document-content>'''

    # ODS-Datei erstellen
    print(f"\n  ✓ Schreibe {filename}...")
    with ZipFile(filename, 'w') as ods:
        ods.writestr('mimetype', mimetype)
        ods.writestr('META-INF/manifest.xml', manifest)
        ods.writestr('meta.xml', meta)
        ods.writestr('settings.xml', settings)
        ods.writestr('styles.xml', styles)
        ods.writestr('content.xml', content)

    print(f"\n✅ {filename} wurde erfolgreich erstellt!")
    print(f"\n🎨 MILITARY MODERN DESIGN:")
    print(f"   - Farbschema: Militärgrün, Anthrazit, Stahlgrau")
    print(f"   - Warnfarben: Orange, Bernstein")
    print(f"   - Erfolgsfarben: Dunkelgrün")
    print(f"   - Moderne Typography mit Liberation Sans/Mono")
    print(f"   - Professionelle Rahmen und Padding")
    print(f"\n📊 System-Übersicht:")
    print(f"   - OVERVIEW (Kommandozentrale)")
    print(f"   - 12 Einzelblätter (Logbücher)")
    print(f"   - STATISTIK (Aggregation)")
    print(f"   - STEUERUNG (Sollwerte)")
    print(f"   - WARTUNGEN (Wartungsintervalle)")
    print(f"   - WE KW (Terminplanung)")

    return filename


if __name__ == "__main__":
    create_kiowa_ods()
