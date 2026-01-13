#!/usr/bin/env python3
"""
KIOWA Flottensteuerung V47
Generiert eine LibreOffice Calc Datei für die Überwachung von Flugzeug-Flotten
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


class ODSGenerator:
    """Generiert ODS-Dateien für KIOWA System"""

    def __init__(self):
        self.namespaces = {
            'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
            'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
            'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
            'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
            'number': 'urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0'
        }

    def create_cell(self, value=None, formula=None, value_type='string', style=None):
        """Erstellt eine Tabellenzelle"""
        cell_attrs = {}
        if style:
            cell_attrs['{%s}style-name' % self.namespaces['table']] = style
        if value_type:
            cell_attrs['{%s}value-type' % self.namespaces['office']] = value_type

        if formula:
            cell_attrs['{%s}formula' % self.namespaces['table']] = f'of:={formula}'
        elif value is not None and value_type == 'float':
            cell_attrs['{%s}value' % self.namespaces['office']] = str(value)

        cell = ET.Element('{%s}table-cell' % self.namespaces['table'], cell_attrs)

        if value is not None:
            p = ET.SubElement(cell, '{%s}p' % self.namespaces['text'])
            p.text = str(value)

        return cell

    def create_empty_cell(self, count=1):
        """Erstellt leere Zellen"""
        if count == 1:
            return ET.Element('{%s}table-cell' % self.namespaces['table'])
        else:
            return ET.Element('{%s}table-cell' % self.namespaces['table'],
                            {'{%s}number-columns-repeated' % self.namespaces['table']: str(count)})


def create_logbook_sheet(aircraft_id):
    """Erstellt ein Logbuch-Blatt für ein Flugzeug"""

    sheet_xml = f'''      <table:table table:name="{aircraft_id}" table:style-name="ta1">
        <!-- Kopfzeile -->
        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Monat</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Tag</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>HH</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>MM</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>LDG</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>CYC</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>Fuel-INL</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
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

    # Zeile 2: Übertrag (manuell einzutragen)
    sheet_xml += '''        <table:table-row>
          <table:table-cell table:style-name="vortrag" office:value-type="string">
            <text:p>ÜBERTRAG</text:p>
          </table:table-cell>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
        </table:table-row>
'''

    # Zeile 3: SUMME (mit Formeln)
    # Formel für Zellen-LSN HH (L3): =L2+SUM(C4:C369)+INT((M2+SUM(D4:D369))/60)
    # Formel für Zellen-LSN MM (M3): =MOD(M2+SUM(D4:D369);60)
    # Formel für TW-LSN HH (N3): =N2+SUM(C4:C369)+INT((O2+SUM(D4:D369))/60)+P2+INT((O2+Q2)/60)
    # Formel für TW-LSN MM (O3): =MOD(O2+SUM(D4:D369)+Q2;60)

    sheet_xml += f'''        <table:table-row>
          <table:table-cell table:style-name="summe" office:value-type="string">
            <text:p>SUMME</text:p>
          </table:table-cell>
          <table:table-cell/>
          <table:table-cell table:style-name="calculated" table:formula="of:=SUM({aircraft_id}.C4:{aircraft_id}.C369)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=SUM({aircraft_id}.D4:{aircraft_id}.D369)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=SUM({aircraft_id}.E4:{aircraft_id}.E369)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=SUM({aircraft_id}.F4:{aircraft_id}.F369)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=SUM({aircraft_id}.G4:{aircraft_id}.G369)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=SUM({aircraft_id}.H4:{aircraft_id}.H369)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell/>
          <table:table-cell table:style-name="calculated" table:formula="of:={aircraft_id}.L2+SUM({aircraft_id}.C4:{aircraft_id}.C369)+INT(({aircraft_id}.M2+SUM({aircraft_id}.D4:{aircraft_id}.D369))/60)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=MOD({aircraft_id}.M2+SUM({aircraft_id}.D4:{aircraft_id}.D369);60)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:={aircraft_id}.N2+SUM({aircraft_id}.C4:{aircraft_id}.C369)+INT(({aircraft_id}.O2+SUM({aircraft_id}.D4:{aircraft_id}.D369))/60)+{aircraft_id}.P2+INT(({aircraft_id}.O2+{aircraft_id}.Q2)/60)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=MOD({aircraft_id}.O2+SUM({aircraft_id}.D4:{aircraft_id}.D369)+{aircraft_id}.Q2;60)" office:value-type="float">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell/>
          <table:table-cell/>
        </table:table-row>
'''

    # Datumszeilen für alle 365 Tage
    row_num = 4
    for month_name, days in MONTHS:
        for day in range(1, days + 1):
            sheet_xml += f'''        <table:table-row>
          <table:table-cell office:value-type="string">
            <text:p>{month_name}</text:p>
          </table:table-cell>
          <table:table-cell office:value-type="float" office:value="{day}">
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
          <table:table-cell table:style-name="calculated" table:formula="of:=IF({aircraft_id}.C{row_num}=&quot;&quot;;&quot;&quot;;{aircraft_id}.L2+SUM({aircraft_id}.C$4:{aircraft_id}.C{row_num})+INT(({aircraft_id}.M2+SUM({aircraft_id}.D$4:{aircraft_id}.D{row_num}))/60))" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=IF({aircraft_id}.C{row_num}=&quot;&quot;;&quot;&quot;;MOD({aircraft_id}.M2+SUM({aircraft_id}.D$4:{aircraft_id}.D{row_num});60))" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=IF({aircraft_id}.C{row_num}=&quot;&quot;;&quot;&quot;;{aircraft_id}.N2+SUM({aircraft_id}.C$4:{aircraft_id}.C{row_num})+INT(({aircraft_id}.O2+SUM({aircraft_id}.D$4:{aircraft_id}.D{row_num}))/60)+{aircraft_id}.P2+INT(({aircraft_id}.O2+{aircraft_id}.Q2)/60))" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=IF({aircraft_id}.C{row_num}=&quot;&quot;;&quot;&quot;;MOD({aircraft_id}.O2+SUM({aircraft_id}.D$4:{aircraft_id}.D{row_num})+{aircraft_id}.Q2;60))" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
        </table:table-row>
'''
            row_num += 1

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_statistik_sheet():
    """Erstellt das STATISTIK-Blatt"""

    sheet_xml = '''      <table:table table:name="STATISTIK" table:style-name="ta1">
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
        sheet_xml += f'''          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>{month_name}</text:p>
          </table:table-cell>
'''
    sheet_xml += '''          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>JAHR</text:p>
          </table:table-cell>
        </table:table-row>
'''

    # Für jedes Flugzeug einen 8-Zeilen-Block
    for aircraft in FLEET:
        # Zeile 1: Flugzeit HH
        sheet_xml += f'''        <table:table-row>
          <table:table-cell office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
          <table:table-cell office:value-type="string">
            <text:p>Flugzeit HH</text:p>
          </table:table-cell>
'''
        # Hier würden die monatlichen Formeln kommen (vereinfacht als 0)
        for i in range(13):  # 12 Monate + Jahr
            sheet_xml += '''          <table:table-cell office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
        sheet_xml += '        </table:table-row>\n'

        # Zeile 2: Flugzeit MM
        sheet_xml += f'''        <table:table-row>
          <table:table-cell/>
          <table:table-cell office:value-type="string">
            <text:p>Flugzeit MM</text:p>
          </table:table-cell>
'''
        for i in range(13):
            sheet_xml += '''          <table:table-cell office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
        sheet_xml += '        </table:table-row>\n'

        # Zeile 3-6: Landungen, Cycles, Fuel-INL, Fuel-AUSL
        for param in ['Landungen', 'Cycles', 'Fuel-INL', 'Fuel-AUSL']:
            sheet_xml += f'''        <table:table-row>
          <table:table-cell/>
          <table:table-cell office:value-type="string">
            <text:p>{param}</text:p>
          </table:table-cell>
'''
            for i in range(13):
                sheet_xml += '''          <table:table-cell office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
            sheet_xml += '        </table:table-row>\n'

        # Zeile 7: TW-LSN (Stand Monatsende)
        sheet_xml += f'''        <table:table-row>
          <table:table-cell/>
          <table:table-cell office:value-type="string">
            <text:p>TW-LSN Monatsende</text:p>
          </table:table-cell>
'''
        for i in range(13):
            sheet_xml += '''          <table:table-cell office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
        sheet_xml += '        </table:table-row>\n'

        # Zeile 8: Leerzeile
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


def create_overview_sheet():
    """Erstellt das OVERVIEW-Blatt"""

    sheet_xml = '''      <table:table table:name="OVERVIEW" table:style-name="ta1">
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
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>LSN IST</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="header" office:value-type="string">
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

    row_num = 2
    for aircraft in FLEET:
        sheet_xml += f'''        <table:table-row>
          <table:table-cell office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input">
            <text:p>VB</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:=IF(TODAY()-DATE(2024;1;1)&gt;14;&quot;BDL&quot;;&quot;&quot;)" office:value-type="string">
            <text:p></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="calculated" table:formula="of:={aircraft}.L3&amp;&quot;:&quot;&amp;TEXT({aircraft}.M3;&quot;00&quot;)" office:value-type="string">
            <text:p>0:00</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated" table:formula="of:={aircraft}.N3&amp;&quot;:&quot;&amp;TEXT({aircraft}.O3;&quot;00&quot;)" office:value-type="string">
            <text:p>0:00</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="calculated"/>
          <table:table-cell table:style-name="calculated"/>
          <table:table-cell table:style-name="calculated"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="calculated"/>
          <table:table-cell table:style-name="calculated"/>
        </table:table-row>
'''
        row_num += 1

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_steuerung_sheet():
    """Erstellt das STEUERUNG-Blatt"""

    sheet_xml = '''      <table:table table:name="STEUERUNG" table:style-name="ta1">
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
        sheet_xml += f'''          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>{month_name} Soll</text:p>
          </table:table-cell>
'''

    sheet_xml += '''        </table:table-row>
'''

    # Zeilen für jedes Flugzeug
    for aircraft in FLEET:
        sheet_xml += f'''        <table:table-row>
          <table:table-cell office:value-type="string">
            <text:p>{aircraft}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
        # Monatssoll-Werte (beispielhaft 0)
        for _ in range(12):
            sheet_xml += '''          <table:table-cell table:style-name="input" office:value-type="float" office:value="0">
            <text:p>0</text:p>
          </table:table-cell>
'''
        sheet_xml += '        </table:table-row>\n'

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_wartungen_sheet():
    """Erstellt das WARTUNGEN-Blatt"""

    sheet_xml = '''      <table:table table:name="WARTUNGEN" table:style-name="ta1">
        <table:table-row>
          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>LSN-Stufe</text:p>
          </table:table-cell>
'''

    # Spalten für jedes Flugzeug und jeden Wartungstyp
    for aircraft in FLEET:
        for wtyp in WARTUNGSTYPEN:
            sheet_xml += f'''          <table:table-cell table:style-name="header" office:value-type="string">
            <text:p>{aircraft} {wtyp}</text:p>
          </table:table-cell>
'''

    sheet_xml += '''        </table:table-row>
'''

    # Zeilen für LSN-Stufen (25h Schritte bis 12000h)
    for lsn in range(0, 12001, 25):
        sheet_xml += f'''        <table:table-row>
          <table:table-cell office:value-type="float" office:value="{lsn}">
            <text:p>{lsn}</text:p>
          </table:table-cell>
'''
        # Platzhalter für Berechnungen
        for aircraft in FLEET:
            for _ in WARTUNGSTYPEN:
                sheet_xml += '''          <table:table-cell table:style-name="calculated"/>
'''
        sheet_xml += '        </table:table-row>\n'

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_we_kw_sheet():
    """Erstellt das WE KW-Blatt"""

    sheet_xml = '''      <table:table table:name="WE KW" table:style-name="ta1">
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
          <table:table-cell office:value-type="float" office:value="{kw}">
            <text:p>KW {kw}</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
          <table:table-cell table:style-name="input"/>
        </table:table-row>
'''

    sheet_xml += '      </table:table>\n'
    return sheet_xml


def create_kiowa_ods(filename="KIOWA_V47.ods"):
    """Hauptfunktion: Erstellt die KIOWA ODS-Datei"""

    print("🚁 Erstelle KIOWA Flottensteuerung V47...")

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
    <meta:generator>KIOWA Generator V47</meta:generator>
    <dc:title>KIOWA Flottensteuerung</dc:title>
    <dc:description>Flottenüberwachung für 12 Luftfahrzeuge</dc:description>
    <dc:date>{datetime.now().isoformat()}</dc:date>
  </office:meta>
</office:document-meta>'''

    settings = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                          xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"
                          office:version="1.2">
  <office:settings/>
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

    # Content-Header mit Stilen
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                         xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
                         xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                         xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
                         xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
                         xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
                         office:version="1.2">
  <office:automatic-styles>
    <!-- Header Style -->
    <style:style style:name="header" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#667eea"/>
      <style:text-properties fo:color="#ffffff" fo:font-weight="bold" fo:font-size="11pt"/>
    </style:style>

    <!-- Input Style -->
    <style:style style:name="input" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#f5f5f5"/>
    </style:style>

    <!-- Calculated Style -->
    <style:style style:name="calculated" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#e8eaf6"/>
    </style:style>

    <!-- Vortrag Style -->
    <style:style style:name="vortrag" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#ffeb3b"/>
      <style:text-properties fo:font-weight="bold"/>
    </style:style>

    <!-- Summe Style -->
    <style:style style:name="summe" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#4caf50"/>
      <style:text-properties fo:color="#ffffff" fo:font-weight="bold"/>
    </style:style>

    <!-- Remarks Style -->
    <style:style style:name="remarks" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#ffffff"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:spreadsheet>
'''

    # Sheets generieren
    print("  ✓ Erstelle Einzelblätter für Flotte...")
    for aircraft in FLEET:
        content += create_logbook_sheet(aircraft)
        print(f"    - {aircraft}")

    print("  ✓ Erstelle STATISTIK...")
    content += create_statistik_sheet()

    print("  ✓ Erstelle OVERVIEW...")
    content += create_overview_sheet()

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
    print(f"  ✓ Schreibe {filename}...")
    with ZipFile(filename, 'w') as ods:
        ods.writestr('mimetype', mimetype)
        ods.writestr('META-INF/manifest.xml', manifest)
        ods.writestr('meta.xml', meta)
        ods.writestr('settings.xml', settings)
        ods.writestr('styles.xml', styles)
        ods.writestr('content.xml', content)

    print(f"\n✅ {filename} wurde erfolgreich erstellt!")
    print(f"\n📊 System-Übersicht:")
    print(f"   - 12 Einzelblätter (Logbücher)")
    print(f"   - STATISTIK (Aggregation)")
    print(f"   - OVERVIEW (Kommandozentrale)")
    print(f"   - STEUERUNG (Sollwerte)")
    print(f"   - WARTUNGEN (Wartungsintervalle)")
    print(f"   - WE KW (Terminplanung)")

    return filename


if __name__ == "__main__":
    create_kiowa_ods()
