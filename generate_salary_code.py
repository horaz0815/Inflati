#!/usr/bin/env python3
"""
Generiert Java-Code für MainActivity.java aus gehaltsdaten_template.txt

Usage:
    python generate_salary_code.py gehaltsdaten_template.txt > salary_data_output.java
"""

import sys
import re

def parse_template(filename):
    """Parse the template file and extract salary data"""
    data = {
        'M1': {}, 'M2': {}, 'M3': {},
        'MBO1': {}, 'MBO2': {}, 'MUO1': {}
    }

    current_section = None

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue

            # Check for section headers
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                if 'M1' in section:
                    current_section = 'M1'
                elif 'M2' in section:
                    current_section = 'M2'
                elif 'M3' in section:
                    current_section = 'M3'
                elif 'MBO1' in section:
                    current_section = 'MBO1'
                elif 'MBO2' in section:
                    current_section = 'MBO2'
                elif 'MUO1' in section:
                    current_section = 'MUO1'
                continue

            # Parse data line
            if '=' in line and current_section:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                if not value:  # Skip empty values
                    continue

                try:
                    value_float = float(value)

                    if current_section in ['M1', 'M2', 'M3']:
                        # Basic salary
                        if key == 'daz':
                            data[current_section][20] = value_float
                        elif key == 'DAZ':
                            data[current_section][21] = value_float
                        else:
                            data[current_section][int(key)] = value_float
                    else:
                        # Function allowances (format: FG.Stufe)
                        if '.' in key:
                            fg, stufe = key.split('.')
                            fg_int = int(fg)
                            stufe_int = int(stufe)

                            if fg_int not in data[current_section]:
                                data[current_section][fg_int] = {}
                            data[current_section][fg_int][stufe_int] = value_float
                except ValueError:
                    print(f"Warning: Could not parse line: {line}", file=sys.stderr)

    return data

def generate_salary_code(data):
    """Generate Java code for salary data"""
    code = []

    code.append("// ===== GRUNDGEHÄLTER (Generated from template) =====")
    code.append("")

    # Generate M1
    if data['M1']:
        code.append("// M1 - Berufsoffiziere")
        code.append("Map<Integer, Double> m1Salaries = new HashMap<>();")
        for stufe in sorted(data['M1'].keys()):
            value = data['M1'][stufe]
            comment = ""
            if stufe == 20:
                comment = " // daz"
            elif stufe == 21:
                comment = " // DAZ"
            code.append(f"m1Salaries.put({stufe}, {value:.2f});{comment}")
        code.append("salaryData.put(\"M1\", m1Salaries);")
        code.append("")

    # Generate M2
    if data['M2']:
        code.append("// M2 - Berufsunteroffiziere")
        code.append("Map<Integer, Double> m2Salaries = new HashMap<>();")
        for stufe in sorted(data['M2'].keys()):
            value = data['M2'][stufe]
            comment = ""
            if stufe == 20:
                comment = " // daz"
            elif stufe == 21:
                comment = " // DAZ"
            code.append(f"m2Salaries.put({stufe}, {value:.2f});{comment}")
        code.append("salaryData.put(\"M2\", m2Salaries);")
        code.append("")

    # Generate M3
    if data['M3']:
        code.append("// M3 - Chargen")
        code.append("Map<Integer, Double> m3Salaries = new HashMap<>();")
        for stufe in sorted(data['M3'].keys()):
            value = data['M3'][stufe]
            comment = ""
            if stufe == 20:
                comment = " // daz"
            elif stufe == 21:
                comment = " // DAZ"
            code.append(f"m3Salaries.put({stufe}, {value:.2f});{comment}")
        code.append("salaryData.put(\"M3\", m3Salaries);")
        code.append("")

    code.append("// ===== FUNKTIONSZULAGEN (Generated from template) =====")
    code.append("")

    # Generate MBO1
    if data['MBO1']:
        code.append("// MBO 1 - Offiziere (6 Funktionsgruppen, je 4 Stufen)")
        code.append("Map<Integer, Map<Integer, Double>> mbo1 = new HashMap<>();")
        for fg in sorted(data['MBO1'].keys()):
            code.append(f"Map<Integer, Double> mbo1_fg{fg} = new HashMap<>();")
            for stufe in sorted(data['MBO1'][fg].keys()):
                value = data['MBO1'][fg][stufe]
                code.append(f"mbo1_fg{fg}.put({stufe}, {value:.2f});")
            code.append(f"mbo1.put({fg}, mbo1_fg{fg});")
        code.append("functionAllowanceData.put(\"MBO1\", mbo1);")
        code.append("")

    # Generate MBO2
    if data['MBO2']:
        code.append("// MBO 2 - Offiziere (9 Funktionsgruppen, je 4 Stufen)")
        code.append("Map<Integer, Map<Integer, Double>> mbo2 = new HashMap<>();")
        for fg in sorted(data['MBO2'].keys()):
            code.append(f"Map<Integer, Double> mbo2_fg{fg} = new HashMap<>();")
            for stufe in sorted(data['MBO2'][fg].keys()):
                value = data['MBO2'][fg][stufe]
                code.append(f"mbo2_fg{fg}.put({stufe}, {value:.2f});")
            code.append(f"mbo2.put({fg}, mbo2_fg{fg});")
        code.append("functionAllowanceData.put(\"MBO2\", mbo2);")
        code.append("")

    # Generate MUO1
    if data['MUO1']:
        code.append("// MUO 1 - Unteroffiziere (7 Funktionsgruppen, je 4 Stufen)")
        code.append("Map<Integer, Map<Integer, Double>> muo1 = new HashMap<>();")
        for fg in sorted(data['MUO1'].keys()):
            code.append(f"Map<Integer, Double> muo1_fg{fg} = new HashMap<>();")
            for stufe in sorted(data['MUO1'][fg].keys()):
                value = data['MUO1'][fg][stufe]
                code.append(f"muo1_fg{fg}.put({stufe}, {value:.2f});")
            code.append(f"muo1.put({fg}, muo1_fg{fg});")
        code.append("functionAllowanceData.put(\"MUO1\", muo1);")
        code.append("")

    return '\n'.join(code)

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_salary_code.py gehaltsdaten_template.txt")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        data = parse_template(filename)
        code = generate_salary_code(data)
        print(code)

        # Print statistics
        print("\n// ===== STATISTIK =====", file=sys.stderr)
        print(f"// M1 Einträge: {len(data['M1'])}", file=sys.stderr)
        print(f"// M2 Einträge: {len(data['M2'])}", file=sys.stderr)
        print(f"// M3 Einträge: {len(data['M3'])}", file=sys.stderr)
        print(f"// MBO1 Funktionsgruppen: {len(data['MBO1'])}", file=sys.stderr)
        print(f"// MBO2 Funktionsgruppen: {len(data['MBO2'])}", file=sys.stderr)
        print(f"// MUO1 Funktionsgruppen: {len(data['MUO1'])}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
