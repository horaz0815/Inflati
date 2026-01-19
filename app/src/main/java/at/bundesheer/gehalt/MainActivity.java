package at.bundesheer.gehalt;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import java.text.DecimalFormat;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private Spinner spinnerVerwendungsgruppe;
    private Spinner spinnerGehaltsstufe;
    private Spinner spinnerFunktionsubergruppe;
    private Spinner spinnerFunktionsgruppe;
    private Spinner spinnerFunktionsstufe;
    private Spinner spinnerLuftfahrttechniker;
    private Button btnBerechnen;
    private CardView cardResults;
    private TextView tvGrundgehalt;
    private TextView tvFunktionszulage;
    private TextView tvNebengebuehren;
    private TextView tvGesamtgehalt;

    private DecimalFormat euroFormat = new DecimalFormat("€ #,##0.00");

    // Salary data structure: Verwendungsgruppe -> Gehaltsstufe -> Amount
    private Map<String, Map<Integer, Double>> salaryData;

    // Function allowance data: Übergruppe -> Funktionsgruppe -> Funktionsstufe -> Amount
    private Map<String, Map<Integer, Map<Integer, Double>>> functionAllowanceData;

    // Luftfahrttechniker allowance data: Position -> Amount
    private Map<Integer, Double> luftfahrtAllowanceData;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initializeSalaryData();
        initializeViews();
        setupSpinners();
        setupListeners();
    }

    private void initializeSalaryData() {
        salaryData = new HashMap<>();

        // OFFIZIELLE DATEN 2025 von GÖD Gehaltstabellen
        // Quelle: § 85 und § 89 GehG, gültig ab 01.01.2025
        // https://www.goed.at/themen/gehaltstabellen-2025/militaerischer-dienst

        // M1 - Berufsoffiziere M BO 1
        Map<Integer, Double> m1Salaries = new HashMap<>();
        m1Salaries.put(1, 3296.8);
        m1Salaries.put(2, 3414.9);
        m1Salaries.put(3, 3592.6);
        m1Salaries.put(4, 3846.4);
        m1Salaries.put(5, 4101.6);
        m1Salaries.put(6, 4358.3);
        m1Salaries.put(7, 4613.7);
        m1Salaries.put(8, 4870.4);
        m1Salaries.put(9, 5128.5);
        m1Salaries.put(10, 5386.8);
        m1Salaries.put(11, 5643.4);
        m1Salaries.put(12, 5900.2);
        m1Salaries.put(13, 6158.4);
        m1Salaries.put(14, 6415.1);
        m1Salaries.put(15, 6699.6);
        m1Salaries.put(16, 6966.0);
        m1Salaries.put(17, 0.0); // Nicht in Tabelle
        m1Salaries.put(18, 0.0); // Nicht in Tabelle
        m1Salaries.put(19, 0.0); // Nicht in Tabelle
        m1Salaries.put(20, 135.8); // daz (kleine Dienstalterzulage)
        m1Salaries.put(21, 541.2); // DAZ (große Dienstalterzulage)
        salaryData.put("M1", m1Salaries);

        // M2 - Berufsunteroffiziere M BUO
        Map<Integer, Double> m2Salaries = new HashMap<>();
        m2Salaries.put(1, 2532.0);
        m2Salaries.put(2, 2552.2);
        m2Salaries.put(3, 2572.6);
        m2Salaries.put(4, 2592.6);
        m2Salaries.put(5, 2634.7);
        m2Salaries.put(6, 2676.5);
        m2Salaries.put(7, 2729.6);
        m2Salaries.put(8, 2794.0);
        m2Salaries.put(9, 2858.8);
        m2Salaries.put(10, 2929.1);
        m2Salaries.put(11, 2999.9);
        m2Salaries.put(12, 3077.7);
        m2Salaries.put(13, 3162.2);
        m2Salaries.put(14, 3255.3);
        m2Salaries.put(15, 3359.3);
        m2Salaries.put(16, 3466.2);
        m2Salaries.put(17, 3572.9);
        m2Salaries.put(18, 3681.3);
        m2Salaries.put(19, 3790.8);
        m2Salaries.put(20, 137.0); // daz (kleine Dienstalterzulage)
        m2Salaries.put(21, 218.2); // DAZ (große Dienstalterzulage)
        salaryData.put("M2", m2Salaries);

        // M3 - Chargen M ZCh
        Map<Integer, Double> m3Salaries = new HashMap<>();
        m3Salaries.put(1, 2378.3);
        m3Salaries.put(2, 2378.3);
        m3Salaries.put(3, 2378.3);
        m3Salaries.put(4, 2378.3);
        m3Salaries.put(5, 2378.3);
        m3Salaries.put(6, 2381.9);
        m3Salaries.put(7, 2401.6);
        m3Salaries.put(8, 2423.8);
        m3Salaries.put(9, 2443.4);
        m3Salaries.put(10, 2463.8);
        m3Salaries.put(11, 2485.2);
        m3Salaries.put(12, 2496.6);
        m3Salaries.put(13, 0.0); // Nicht in Tabelle
        m3Salaries.put(14, 0.0); // Nicht in Tabelle
        m3Salaries.put(15, 0.0); // Nicht in Tabelle
        m3Salaries.put(16, 0.0); // Nicht in Tabelle
        m3Salaries.put(17, 0.0); // Nicht in Tabelle
        m3Salaries.put(18, 0.0); // Nicht in Tabelle
        m3Salaries.put(19, 0.0); // Nicht in Tabelle
        m3Salaries.put(20, 0.0); // daz nicht in Tabelle
        m3Salaries.put(21, 0.0); // DAZ nicht in Tabelle
        salaryData.put("M3", m3Salaries);

        // FUNKTIONSZULAGEN § 91 GehG - OFFIZIELLE DATEN 2025
        functionAllowanceData = new HashMap<>();

        // MBO 1 - Offiziere M BO 1 / M ZO 1 (6 Funktionsgruppen, je 4 Stufen)
        Map<Integer, Map<Integer, Double>> mbo1 = new HashMap<>();

        Map<Integer, Double> mbo1_fg1 = new HashMap<>();
        mbo1_fg1.put(1, 76.8);
        mbo1_fg1.put(2, 227.9);
        mbo1_fg1.put(3, 425.2);
        mbo1_fg1.put(4, 485.4);
        mbo1.put(1, mbo1_fg1);

        Map<Integer, Double> mbo1_fg2 = new HashMap<>();
        mbo1_fg2.put(1, 379.0);
        mbo1_fg2.put(2, 606.9);
        mbo1_fg2.put(3, 1363.5);
        mbo1_fg2.put(4, 2271.2);
        mbo1.put(2, mbo1_fg2);

        Map<Integer, Double> mbo1_fg3 = new HashMap<>();
        mbo1_fg3.put(1, 409.8);
        mbo1_fg3.put(2, 749.7);
        mbo1_fg3.put(3, 1641.8);
        mbo1_fg3.put(4, 2717.4);
        mbo1.put(3, mbo1_fg3);

        Map<Integer, Double> mbo1_fg4 = new HashMap<>();
        mbo1_fg4.put(1, 436.3);
        mbo1_fg4.put(2, 955.2);
        mbo1_fg4.put(3, 1787.2);
        mbo1_fg4.put(4, 2865.5);
        mbo1.put(4, mbo1_fg4);

        Map<Integer, Double> mbo1_fg5 = new HashMap<>();
        mbo1_fg5.put(1, 1002.6);
        mbo1_fg5.put(2, 1760.7);
        mbo1_fg5.put(3, 3143.6);
        mbo1_fg5.put(4, 4283.3);
        mbo1.put(5, mbo1_fg5);

        Map<Integer, Double> mbo1_fg6 = new HashMap<>();
        mbo1_fg6.put(1, 1208.2);
        mbo1_fg6.put(2, 2036.1);
        mbo1_fg6.put(3, 3445.7);
        mbo1_fg6.put(4, 4556.3);
        mbo1.put(6, mbo1_fg6);

        functionAllowanceData.put("MBO1", mbo1);

        // MBO 2 - Offiziere M BO 2 / M ZO 2 / M ZO 3 (9 Funktionsgruppen, je 4 Stufen)
        Map<Integer, Map<Integer, Double>> mbo2 = new HashMap<>();

        Map<Integer, Double> mbo2_fg1 = new HashMap<>();
        mbo2_fg1.put(1, 91.0);
        mbo2_fg1.put(2, 106.3);
        mbo2_fg1.put(3, 121.5);
        mbo2_fg1.put(4, 137.0);
        mbo2.put(1, mbo2_fg1);

        Map<Integer, Double> mbo2_fg2 = new HashMap<>();
        mbo2_fg2.put(1, 106.3);
        mbo2_fg2.put(2, 137.0);
        mbo2_fg2.put(3, 166.3);
        mbo2_fg2.put(4, 227.9);
        mbo2.put(2, mbo2_fg2);

        Map<Integer, Double> mbo2_fg3 = new HashMap<>();
        mbo2_fg3.put(1, 258.8);
        mbo2_fg3.put(2, 365.0);
        mbo2_fg3.put(3, 530.0);
        mbo2_fg3.put(4, 1060.2);
        mbo2.put(3, mbo2_fg3);

        Map<Integer, Double> mbo2_fg4 = new HashMap<>();
        mbo2_fg4.put(1, 334.1);
        mbo2_fg4.put(2, 454.5);
        mbo2_fg4.put(3, 727.2);
        mbo2_fg4.put(4, 1439.2);
        mbo2.put(4, mbo2_fg4);

        Map<Integer, Double> mbo2_fg5 = new HashMap<>();
        mbo2_fg5.put(1, 365.0);
        mbo2_fg5.put(2, 485.4);
        mbo2_fg5.put(3, 787.3);
        mbo2_fg5.put(4, 1545.4);
        mbo2.put(5, mbo2_fg5);

        Map<Integer, Double> mbo2_fg6 = new HashMap<>();
        mbo2_fg6.put(1, 454.5);
        mbo2_fg6.put(2, 606.9);
        mbo2_fg6.put(3, 1060.2);
        mbo2_fg6.put(4, 1787.2);
        mbo2.put(6, mbo2_fg6);

        Map<Integer, Double> mbo2_fg7 = new HashMap<>();
        mbo2_fg7.put(1, 530.0);
        mbo2_fg7.put(2, 682.4);
        mbo2_fg7.put(3, 1135.7);
        mbo2_fg7.put(4, 1969.0);
        mbo2.put(7, mbo2_fg7);

        Map<Integer, Double> mbo2_fg8 = new HashMap<>();
        mbo2_fg8.put(1, 1068.4);
        mbo2_fg8.put(2, 1424.9);
        mbo2_fg8.put(3, 2136.9);
        mbo2_fg8.put(4, 2991.4);
        mbo2.put(8, mbo2_fg8);

        Map<Integer, Double> mbo2_fg9 = new HashMap<>();
        mbo2_fg9.put(1, 1139.6);
        mbo2_fg9.put(2, 1567.8);
        mbo2_fg9.put(3, 2350.8);
        mbo2_fg9.put(4, 3560.6);
        mbo2.put(9, mbo2_fg9);

        functionAllowanceData.put("MBO2", mbo2);

        // MUO 1 - Unteroffiziere M BUO / M ZUO (7 Funktionsgruppen, je 4 Stufen)
        Map<Integer, Map<Integer, Double>> muo1 = new HashMap<>();

        Map<Integer, Double> muo1_fg1 = new HashMap<>();
        muo1_fg1.put(1, 91.0);
        muo1_fg1.put(2, 106.3);
        muo1_fg1.put(3, 121.5);
        muo1_fg1.put(4, 137.0);
        muo1.put(1, muo1_fg1);

        Map<Integer, Double> muo1_fg2 = new HashMap<>();
        muo1_fg2.put(1, 106.3);
        muo1_fg2.put(2, 137.0);
        muo1_fg2.put(3, 166.3);
        muo1_fg2.put(4, 197.3);
        muo1.put(2, muo1_fg2);

        Map<Integer, Double> muo1_fg3 = new HashMap<>();
        muo1_fg3.put(1, 152.4);
        muo1_fg3.put(2, 227.9);
        muo1_fg3.put(3, 303.6);
        muo1_fg3.put(4, 530.0);
        muo1.put(3, muo1_fg3);

        Map<Integer, Double> muo1_fg4 = new HashMap<>();
        muo1_fg4.put(1, 227.9);
        muo1_fg4.put(2, 303.6);
        muo1_fg4.put(3, 379.0);
        muo1_fg4.put(4, 606.9);
        muo1.put(4, muo1_fg4);

        Map<Integer, Double> muo1_fg5 = new HashMap<>();
        muo1_fg5.put(1, 303.6);
        muo1_fg5.put(2, 379.0);
        muo1_fg5.put(3, 606.9);
        muo1_fg5.put(4, 924.5);
        muo1.put(5, muo1_fg5);

        Map<Integer, Double> muo1_fg6 = new HashMap<>();
        muo1_fg6.put(1, 379.0);
        muo1_fg6.put(2, 454.5);
        muo1_fg6.put(3, 758.0);
        muo1_fg6.put(4, 984.8);
        muo1.put(6, muo1_fg6);

        Map<Integer, Double> muo1_fg7 = new HashMap<>();
        muo1_fg7.put(1, 454.5);
        muo1_fg7.put(2, 606.9);
        muo1_fg7.put(3, 908.9);
        muo1_fg7.put(4, 1212.4);
        muo1.put(7, muo1_fg7);

        functionAllowanceData.put("MUO1", muo1);

        // LUFTFAHRTTECHNIKER-NEBENGEBÜHREN
        // TODO: Konkrete Beträge vom Benutzer erhalten
        luftfahrtAllowanceData = new HashMap<>();
        luftfahrtAllowanceData.put(0, 0.0);    // Keine
        luftfahrtAllowanceData.put(1, 0.0);    // Assistenzdienst
        luftfahrtAllowanceData.put(2, 0.0);    // Wart (MLuFWart)
        luftfahrtAllowanceData.put(3, 0.0);    // Wart I (MLuFWart I. Kl)
        luftfahrtAllowanceData.put(4, 0.0);    // Luftfahrtmeister (MLuFMst)
        luftfahrtAllowanceData.put(5, 0.0);    // Leitender Dienst (Ltd Dienst)
    }

    private void initializeViews() {
        spinnerVerwendungsgruppe = findViewById(R.id.spinnerVerwendungsgruppe);
        spinnerGehaltsstufe = findViewById(R.id.spinnerGehaltsstufe);
        spinnerFunktionsubergruppe = findViewById(R.id.spinnerFunktionsubergruppe);
        spinnerFunktionsgruppe = findViewById(R.id.spinnerFunktionsgruppe);
        spinnerFunktionsstufe = findViewById(R.id.spinnerFunktionsstufe);
        spinnerLuftfahrttechniker = findViewById(R.id.spinnerLuftfahrttechniker);
        btnBerechnen = findViewById(R.id.btnBerechnen);
        cardResults = findViewById(R.id.cardResults);
        tvGrundgehalt = findViewById(R.id.tvGrundgehalt);
        tvFunktionszulage = findViewById(R.id.tvFunktionszulage);
        tvNebengebuehren = findViewById(R.id.tvNebengebuehren);
        tvGesamtgehalt = findViewById(R.id.tvGesamtgehalt);
    }

    private void setupSpinners() {
        // Verwendungsgruppe Spinner
        ArrayAdapter<CharSequence> verwendungAdapter = ArrayAdapter.createFromResource(this,
                R.array.verwendungsgruppen, android.R.layout.simple_spinner_item);
        verwendungAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerVerwendungsgruppe.setAdapter(verwendungAdapter);

        // Gehaltsstufe Spinner
        ArrayAdapter<CharSequence> gehaltAdapter = ArrayAdapter.createFromResource(this,
                R.array.gehaltsstufen, android.R.layout.simple_spinner_item);
        gehaltAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerGehaltsstufe.setAdapter(gehaltAdapter);

        // Funktionsübergruppe Spinner
        ArrayAdapter<CharSequence> ubergruppeAdapter = ArrayAdapter.createFromResource(this,
                R.array.funktionsubergruppen, android.R.layout.simple_spinner_item);
        ubergruppeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerFunktionsubergruppe.setAdapter(ubergruppeAdapter);

        // Funktionsstufe Spinner
        ArrayAdapter<CharSequence> funktionsstufeAdapter = ArrayAdapter.createFromResource(this,
                R.array.funktionsstufen, android.R.layout.simple_spinner_item);
        funktionsstufeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerFunktionsstufe.setAdapter(funktionsstufeAdapter);

        // Luftfahrttechniker Spinner
        ArrayAdapter<CharSequence> luftfahrtAdapter = ArrayAdapter.createFromResource(this,
                R.array.luftfahrttechniker, android.R.layout.simple_spinner_item);
        luftfahrtAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerLuftfahrttechniker.setAdapter(luftfahrtAdapter);
    }

    private void setupListeners() {
        btnBerechnen.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                calculateSalary();
            }
        });

        // Update Funktionsgruppe based on Übergruppe selection
        spinnerFunktionsubergruppe.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                updateFunktionsgruppeSpinner(position);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });

        // Enable/disable Funktionsstufe based on Funktionsgruppe selection
        spinnerFunktionsgruppe.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                spinnerFunktionsstufe.setEnabled(position > 0);
                if (position == 0) {
                    spinnerFunktionsstufe.setSelection(0);
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });
    }

    private void updateFunktionsgruppeSpinner(int ubergruppePosition) {
        ArrayAdapter<CharSequence> adapter;

        switch (ubergruppePosition) {
            case 1: // MBO 1 - 6 Funktionsgruppen
                adapter = ArrayAdapter.createFromResource(this,
                        R.array.funktionsgruppen_mbo1, android.R.layout.simple_spinner_item);
                break;
            case 2: // MBO 2 - 9 Funktionsgruppen
                adapter = ArrayAdapter.createFromResource(this,
                        R.array.funktionsgruppen_mbo2, android.R.layout.simple_spinner_item);
                break;
            case 3: // MUO 1 - 7 Funktionsgruppen
                adapter = ArrayAdapter.createFromResource(this,
                        R.array.funktionsgruppen_muo1, android.R.layout.simple_spinner_item);
                break;
            default: // Keine
                adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item);
                adapter.add("Keine");
                break;
        }

        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerFunktionsgruppe.setAdapter(adapter);
        spinnerFunktionsgruppe.setEnabled(ubergruppePosition > 0);
        spinnerFunktionsstufe.setEnabled(false);
        spinnerFunktionsstufe.setSelection(0);
    }

    private void calculateSalary() {
        // Get selections
        int verwendungPosition = spinnerVerwendungsgruppe.getSelectedItemPosition();
        int gehaltPosition = spinnerGehaltsstufe.getSelectedItemPosition();
        int ubergruppePosition = spinnerFunktionsubergruppe.getSelectedItemPosition();
        int funktionsgruppePosition = spinnerFunktionsgruppe.getSelectedItemPosition();
        int funktionsstufePosition = spinnerFunktionsstufe.getSelectedItemPosition();
        int luftfahrtPosition = spinnerLuftfahrttechniker.getSelectedItemPosition();

        // Validate selections
        if (verwendungPosition == 0 || gehaltPosition == 0) {
            cardResults.setVisibility(View.GONE);
            return;
        }

        // Extract usage group code (M1, M2, M3)
        String verwendungsKey = extractVerwendungsCode(spinnerVerwendungsgruppe.getSelectedItem().toString());
        int gehaltsstufe = gehaltPosition;

        // Get basic salary
        double grundgehalt = 0.0;
        if (salaryData.containsKey(verwendungsKey)) {
            Map<Integer, Double> stufen = salaryData.get(verwendungsKey);
            if (stufen.containsKey(gehaltsstufe)) {
                grundgehalt = stufen.get(gehaltsstufe);
            }
        }

        // Get function allowance
        double funktionszulage = 0.0;
        if (ubergruppePosition > 0 && funktionsgruppePosition > 0 && funktionsstufePosition > 0) {
            String ubergruppeKey = extractUbergruppeCode(ubergruppePosition);

            if (functionAllowanceData.containsKey(ubergruppeKey)) {
                Map<Integer, Map<Integer, Double>> gruppen = functionAllowanceData.get(ubergruppeKey);
                if (gruppen.containsKey(funktionsgruppePosition)) {
                    Map<Integer, Double> stufen = gruppen.get(funktionsgruppePosition);
                    if (stufen.containsKey(funktionsstufePosition)) {
                        funktionszulage = stufen.get(funktionsstufePosition);
                    }
                }
            }
        }

        // Get Luftfahrttechniker allowance
        double nebengebuehren = 0.0;
        if (luftfahrtAllowanceData.containsKey(luftfahrtPosition)) {
            nebengebuehren = luftfahrtAllowanceData.get(luftfahrtPosition);
        }

        // Calculate total
        double gesamtgehalt = grundgehalt + funktionszulage + nebengebuehren;

        // Display results
        tvGrundgehalt.setText(euroFormat.format(grundgehalt));
        tvFunktionszulage.setText(euroFormat.format(funktionszulage));
        tvNebengebuehren.setText(euroFormat.format(nebengebuehren));
        tvGesamtgehalt.setText(euroFormat.format(gesamtgehalt));
        cardResults.setVisibility(View.VISIBLE);
    }

    private String extractVerwendungsCode(String text) {
        if (text.contains("M1")) return "M1";
        if (text.contains("M2")) return "M2";
        if (text.contains("M3")) return "M3";
        return "";
    }

    private String extractUbergruppeCode(int position) {
        switch (position) {
            case 1: return "MBO1";
            case 2: return "MBO2";
            case 3: return "MUO1";
            default: return "";
        }
    }
}
