#!/usr/bin/env python3
"""
KIOWA Flottensteuerung V47 - Military Modern Edition mit Demo-Daten
Generiert eine LibreOffice Calc Datei für die Überwachung von Flugzeug-Flotten
Design: Military Modern Style mit abgestimmter Farbpalette
Demo: Mit realistischen Beispieldaten befüllt
"""

from zipfile import ZipFile
from datetime import datetime
import random

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
    'dark_slate': '#2C3E50',
    'military_green': '#4A5D23',
    'olive': '#556B2F',
    'steel_gray': '#5D6D7E',
    'light_gray': '#ECF0F1',
    'warning_orange': '#D35400',
    'danger_red': '#C0392B',
    'success_green': '#27AE60',
    'dark_green': '#1E8449',
    'charcoal': '#34495E',
    'sand': '#D7DBDD',
    'black': '#1C2833',
    'white': '#FFFFFF',
    'amber': '#F39C12',
}

# Demo-Daten: Vortragswerte für jedes Flugzeug (LSN ab 7000h)
DEMO_VORTRAG = {
    '3C-OA': {'zelle_hh': 7245, 'zelle_mm': 30, 'tw_hh': 7245, 'tw_mm': 30},
    '3C-OB': {'zelle_hh': 7512, 'zelle_mm': 15, 'tw_hh': 7512, 'tw_mm': 15},
    '3C-OC': {'zelle_hh': 7089, 'zelle_mm': 45, 'tw_hh': 7089, 'tw_mm': 45},
    '3C-OD': {'zelle_hh': 7678, 'zelle_mm': 20, 'tw_hh': 7678, 'tw_mm': 20},
    '3C-OE': {'zelle_hh': 7334, 'zelle_mm': 50, 'tw_hh': 7334, 'tw_mm': 50},
    '3C-OH': {'zelle_hh': 7891, 'zelle_mm': 10, 'tw_hh': 7891, 'tw_mm': 10},
    '3C-OI': {'zelle_hh': 7156, 'zelle_mm': 35, 'tw_hh': 7156, 'tw_mm': 35},
    '3C-OJ': {'zelle_hh': 7423, 'zelle_mm': 25, 'tw_hh': 7423, 'tw_mm': 25},
    '3C-OK': {'zelle_hh': 7767, 'zelle_mm': 40, 'tw_hh': 7767, 'tw_mm': 40},
    '3C-OL': {'zelle_hh': 7201, 'zelle_mm': 55, 'tw_hh': 7201, 'tw_mm': 55},
    'RES1': {'zelle_hh': 7045, 'zelle_mm': 5, 'tw_hh': 7045, 'tw_mm': 5},
    'RES2': {'zelle_hh': 7598, 'zelle_mm': 48, 'tw_hh': 7598, 'tw_mm': 48},
}

# Demo-Bemerkungen
DEMO_REMARKS = [
    'Routineflug',
    'Übungsflug',
    'VFR Navigation',
    'Platzrunden',
    'Checkflug',
    'Schulungsflug',
    'SAR-Einsatz',
    'Patrouillenflug',
    'Nachtflug',
    'IFR Training',
    '',
    '',
    '',
]


def generate_demo_flight_data(day_index, aircraft_idx):
    """Generiert Demo-Flugdaten für einen Tag"""
    # Nicht jeden Tag fliegen (ca. 60% der Tage)
    if random.random() > 0.6:
        return None

    # Realistische Flugzeiten
    flight_hours = random.randint(1, 4)
    flight_minutes = random.choice([0, 15, 30, 45])

    # Landungen basierend auf Flugzeit
    landings = random.randint(2, min(6, flight_hours + 2))

    # Cycles entsprechen ungefähr Landungen
    cycles = landings + random.randint(-1, 1)

    # Kraftstoff (ca. 150-250 Liter pro Stunde)
    fuel_per_hour = random.randint(150, 250)
    total_fuel = int(fuel_per_hour * (flight_hours + flight_minutes/60))

    # 80% Inland, 20% Ausland
    if random.random() < 0.8:
        fuel_inl = total_fuel
        fuel_ausl = 0
    else:
        fuel_inl = 0
        fuel_ausl = total_fuel

    # Bemerkung (manchmal)
    remark = random.choice(DEMO_REMARKS) if random.random() < 0.3 else ''

    return {
        'hh': flight_hours,
        'mm': flight_minutes,
        'ldg': landings,
        'cyc': cycles,
        'fuel_inl': fuel_inl,
        'fuel_ausl': fuel_ausl,
        'remark': remark
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


def create_logbook_sheet(aircraft_id, aircraft_idx):
    """Erstellt ein Logbuch-Blatt für ein Flugzeug mit Military Design und Demo-Daten"""

    vortrag = DEMO_VORTRAG[aircraft_id]

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

    # Zeile 3: Übertrag mit Demo-Werten
    sheet_xml += f'''        <table:table-row>
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
          <table:table-cell table:style-name="number" office:value-type="float" office:value="{vortrag['zelle_hh']}">
            <text:p>{vortrag['zelle_hh']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="{vortrag['zelle_mm']}">
            <text:p>{vortrag['zelle_mm']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="{vortrag['tw_hh']}">
            <text:p>{vortrag['tw_hh']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="{vortrag['tw_mm']}">
            <text:p>{vortrag['tw_mm']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
        </table:table-row>
'''

    # Zeile 4: SUMME mit Formeln
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

    # Datumszeilen mit Demo-Daten für die ersten 2 Monate
    row_num = 5
    day_counter = 0

    for month_idx, (month_name, days) in enumerate(MONTHS):
        for day in range(1, days + 1):
            # Demo-Daten nur für erste 2 Monate generieren
            flight_data = None
            if month_idx < 2:  # Januar und Februar
                flight_data = generate_demo_flight_data(day_counter, aircraft_idx)

            if flight_data:
                sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="date" office:value-type="string">
            <text:p>{month_name}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="date" office:value-type="float" office:value="{day}">
            <text:p>{day}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="{flight_data['hh']}">
            <text:p>{flight_data['hh']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="{flight_data['mm']}">
            <text:p>{flight_data['mm']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="{flight_data['ldg']}">
            <text:p>{flight_data['ldg']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="{flight_data['cyc']}">
            <text:p>{flight_data['cyc']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="{flight_data['fuel_inl']}">
            <text:p>{flight_data['fuel_inl']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="{flight_data['fuel_ausl']}">
            <text:p>{flight_data['fuel_ausl']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="remarks" office:value-type="string">
            <text:p>{flight_data['remark']}</text:p>
          </table:table-cell>
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
            else:
                # Leere Zeile
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
            day_counter += 1

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

    standorte = ['WELS', 'LINZ', 'SALZBURG', 'INNSBRUCK', 'WELS', 'LINZ',
                 'SALZBURG', 'WELS', 'INNSBRUCK', 'WELS', 'WELS', 'WELS']
    flugklarheit = ['VB', 'VB', 'VB', 'BEB', 'VB', 'VB', 'VB', 'VUB', 'VB', 'VB', 'VB', 'VB']

    row_num = 3
    for idx, aircraft in enumerate(FLEET):
        sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="aircraft_id" office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="string">
            <text:p>{flugklarheit[idx]}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="warning" table:formula="of:=IF(TODAY()-DATE(2024;1;1)&gt;14;&quot;BDL&quot;;&quot;&quot;)" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="string">
            <text:p>STD</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="string">
            <text:p>{standorte[idx]}</text:p>
          </table:table-cell>
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

    for aircraft in FLEET:
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

        sheet_xml += '''        <table:table-row>
          <table:table-cell/>
        </table:table-row>
'''

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

    for month_name, _ in MONTHS:
        sheet_xml += f'''          <table:table-cell table:style-name="month_header" office:value-type="string">
            <text:p>{month_name[:3].upper()} Soll</text:p>
          </table:table-cell>
'''
    sheet_xml += '''        </table:table-row>
'''

    for aircraft in FLEET:
        vortrag = DEMO_VORTRAG[aircraft]
        sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="aircraft_id" office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="{vortrag['zelle_hh']}">
            <text:p>{vortrag['zelle_hh']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="{vortrag['zelle_mm']}">
            <text:p>{vortrag['zelle_mm']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="{vortrag['tw_hh']}">
            <text:p>{vortrag['tw_hh']}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="float" office:value="{vortrag['tw_mm']}">
            <text:p>{vortrag['tw_mm']}</text:p>
          </table:table-cell>
'''
        # Monatssoll-Werte (50h pro Monat als Demo)
        for _ in range(12):
            sheet_xml += '''          <table:table-cell table:style-name="input" office:value-type="float" office:value="50">
            <text:p>50</text:p>
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

    for aircraft in FLEET[:6]:
        sheet_xml += f'''          <table:table-cell table:style-name="aircraft_id" office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
'''
    sheet_xml += '''        </table:table-row>
'''

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

    # Einige Demo-Wartungen eintragen
    demo_wartungen = [
        (12, '3C-OA', '100WE', '7500', 'Planmäßige Wartung'),
        (15, '3C-OD', '50WE', '7700', ''),
        (18, '3C-OH', '100WE', '7900', 'Nach Inspektion'),
        (24, '3C-OB', '75WE', '7600', ''),
    ]

    for kw in range(1, 54):
        wartung = next((w for w in demo_wartungen if w[0] == kw), None)

        if wartung:
            sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="float" office:value="{kw}">
            <text:p>KW {kw:02d}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="string">
            <text:p>{wartung[1]}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="string">
            <text:p>{wartung[2]}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="number" office:value-type="string">
            <text:p>{wartung[3]}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="remarks" office:value-type="string">
            <text:p>{wartung[4]}</text:p>
          </table:table-cell>
        </table:table-row>
'''
        else:
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
    """Hauptfunktion: Erstellt die KIOWA ODS-Datei mit Military Modern Design und Demo-Daten"""

    print("🚁 Erstelle KIOWA Flottensteuerung V47 - MILITARY MODERN EDITION mit Demo-Daten...")

    # Seed für reproduzierbare Demo-Daten
    random.seed(42)

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
    <dc:description>Flottenüberwachung für 12 Luftfahrzeuge - Military Modern Design mit Demo-Daten</dc:description>
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

    print("\n  ✓ Erstelle OVERVIEW (Kommandozentrale)...")
    content += create_overview_sheet()

    print("  ✓ Erstelle Einzelblätter mit Demo-Daten...")
    for idx, aircraft in enumerate(FLEET):
        content += create_logbook_sheet(aircraft, idx)
        print(f"    - {aircraft} (LSN: {DEMO_VORTRAG[aircraft]['zelle_hh']}:{DEMO_VORTRAG[aircraft]['zelle_mm']:02d})")

    print("  ✓ Erstelle STATISTIK...")
    content += create_statistik_sheet()

    print("  ✓ Erstelle STEUERUNG...")
    content += create_steuerung_sheet()

    print("  ✓ Erstelle WARTUNGEN...")
    content += create_wartungen_sheet()

    print("  ✓ Erstelle WE KW...")
    content += create_we_kw_sheet()

    content += '''    </office:spreadsheet>
  </office:body>
</office:document-content>'''

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
    print(f"\n📊 DEMO-DATEN:")
    print(f"   - Alle Hubschrauber: LSN ab 7000h")
    print(f"   - Flugdaten für Januar & Februar eingetragen")
    print(f"   - Realistische Flugzeiten, Landungen, Kraftstoff")
    print(f"   - Standorte: WELS, LINZ, SALZBURG, INNSBRUCK")
    print(f"   - Wartungsplanung mit 4 Einträgen")
    print(f"   - Monatssoll: 50h pro Maschine")

    return filename


if __name__ == "__main__":
    create_kiowa_ods()
