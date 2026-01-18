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
    private Spinner spinnerFunktionsgruppe;
    private Spinner spinnerFunktionsstufe;
    private Button btnBerechnen;
    private CardView cardResults;
    private TextView tvGrundgehalt;
    private TextView tvFunktionszulage;
    private TextView tvGesamtgehalt;

    private DecimalFormat euroFormat = new DecimalFormat("€ #,##0.00");

    // Salary data structure: Verwendungsgruppe -> Gehaltsstufe -> Amount
    private Map<String, Map<Integer, Double>> salaryData;

    // Function allowance data: Funktionsgruppe -> Funktionsstufe -> Amount
    private Map<String, Map<Integer, Double>> functionAllowanceData;

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

        // HINWEIS: Dies sind BEISPIELDATEN!
        // Bitte ersetzen Sie diese mit den aktuellen offiziellen Werten von:
        // https://www.goed.at/themen/gehaltstabellen-2025/militaerischer-dienst

        // M1 - Berufsoffiziere (Professional Officers)
        Map<Integer, Double> m1Salaries = new HashMap<>();
        m1Salaries.put(1, 2850.50);
        m1Salaries.put(2, 3125.80);
        m1Salaries.put(3, 3425.30);
        m1Salaries.put(4, 3750.90);
        m1Salaries.put(5, 4105.20);
        m1Salaries.put(6, 4485.70);
        m1Salaries.put(7, 4895.40);
        m1Salaries.put(8, 5335.80);
        m1Salaries.put(9, 5550.00);
        m1Salaries.put(10, 5775.00);
        m1Salaries.put(11, 6010.00);
        m1Salaries.put(12, 6255.00);
        m1Salaries.put(13, 6510.00);
        m1Salaries.put(14, 6775.00);
        m1Salaries.put(15, 7050.00);
        m1Salaries.put(16, 7335.00);
        m1Salaries.put(17, 7630.00);
        m1Salaries.put(18, 7935.00);
        m1Salaries.put(19, 8250.00);
        m1Salaries.put(20, 8500.00); // daz
        m1Salaries.put(21, 8800.00); // DAZ
        salaryData.put("M1", m1Salaries);

        // M2 - Berufsunteroffiziere (Professional NCOs)
        Map<Integer, Double> m2Salaries = new HashMap<>();
        m2Salaries.put(1, 2350.60);
        m2Salaries.put(2, 2585.40);
        m2Salaries.put(3, 2845.70);
        m2Salaries.put(4, 3125.30);
        m2Salaries.put(5, 3425.90);
        m2Salaries.put(6, 3750.50);
        m2Salaries.put(7, 4095.80);
        m2Salaries.put(8, 4465.20);
        m2Salaries.put(9, 4655.00);
        m2Salaries.put(10, 4855.00);
        m2Salaries.put(11, 5065.00);
        m2Salaries.put(12, 5285.00);
        m2Salaries.put(13, 5515.00);
        m2Salaries.put(14, 5755.00);
        m2Salaries.put(15, 6005.00);
        m2Salaries.put(16, 6265.00);
        m2Salaries.put(17, 6535.00);
        m2Salaries.put(18, 6815.00);
        m2Salaries.put(19, 7105.00);
        m2Salaries.put(20, 7350.00); // daz
        m2Salaries.put(21, 7650.00); // DAZ
        salaryData.put("M2", m2Salaries);

        // M3 - Chargen (Enlisted ranks)
        Map<Integer, Double> m3Salaries = new HashMap<>();
        m3Salaries.put(1, 1985.40);
        m3Salaries.put(2, 2185.70);
        m3Salaries.put(3, 2405.80);
        m3Salaries.put(4, 2645.50);
        m3Salaries.put(5, 2905.90);
        m3Salaries.put(6, 3185.40);
        m3Salaries.put(7, 3485.70);
        m3Salaries.put(8, 3805.30);
        m3Salaries.put(9, 3975.00);
        m3Salaries.put(10, 4155.00);
        m3Salaries.put(11, 4345.00);
        m3Salaries.put(12, 4545.00);
        m3Salaries.put(13, 4755.00);
        m3Salaries.put(14, 4975.00);
        m3Salaries.put(15, 5205.00);
        m3Salaries.put(16, 5445.00);
        m3Salaries.put(17, 5695.00);
        m3Salaries.put(18, 5955.00);
        m3Salaries.put(19, 6225.00);
        m3Salaries.put(20, 6450.00); // daz
        m3Salaries.put(21, 6725.00); // DAZ
        salaryData.put("M3", m3Salaries);

        // Function allowances
        functionAllowanceData = new HashMap<>();

        // F1 - Gruppenkommandant (Squad Leader)
        Map<Integer, Double> f1Allowances = new HashMap<>();
        f1Allowances.put(1, 185.50);
        f1Allowances.put(2, 225.80);
        f1Allowances.put(3, 275.40);
        functionAllowanceData.put("F1", f1Allowances);

        // F2 - Zugführer (Platoon Leader)
        Map<Integer, Double> f2Allowances = new HashMap<>();
        f2Allowances.put(1, 285.70);
        f2Allowances.put(2, 345.90);
        f2Allowances.put(3, 415.60);
        functionAllowanceData.put("F2", f2Allowances);

        // F3 - Kompaniechef (Company Commander)
        Map<Integer, Double> f3Allowances = new HashMap<>();
        f3Allowances.put(1, 425.80);
        f3Allowances.put(2, 515.40);
        f3Allowances.put(3, 625.90);
        functionAllowanceData.put("F3", f3Allowances);

        // F4 - Bataillonskommandant (Battalion Commander)
        Map<Integer, Double> f4Allowances = new HashMap<>();
        f4Allowances.put(1, 685.50);
        f4Allowances.put(2, 825.70);
        f4Allowances.put(3, 995.30);
        functionAllowanceData.put("F4", f4Allowances);

        // F5 - Regimentskommandant (Regiment Commander)
        Map<Integer, Double> f5Allowances = new HashMap<>();
        f5Allowances.put(1, 985.60);
        f5Allowances.put(2, 1185.90);
        f5Allowances.put(3, 1425.40);
        functionAllowanceData.put("F5", f5Allowances);

        // No function (Keine)
        Map<Integer, Double> noFunction = new HashMap<>();
        noFunction.put(0, 0.0);
        functionAllowanceData.put("Keine", noFunction);
    }

    private void initializeViews() {
        spinnerVerwendungsgruppe = findViewById(R.id.spinnerVerwendungsgruppe);
        spinnerGehaltsstufe = findViewById(R.id.spinnerGehaltsstufe);
        spinnerFunktionsgruppe = findViewById(R.id.spinnerFunktionsgruppe);
        spinnerFunktionsstufe = findViewById(R.id.spinnerFunktionsstufe);
        btnBerechnen = findViewById(R.id.btnBerechnen);
        cardResults = findViewById(R.id.cardResults);
        tvGrundgehalt = findViewById(R.id.tvGrundgehalt);
        tvFunktionszulage = findViewById(R.id.tvFunktionszulage);
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

        // Funktionsgruppe Spinner
        ArrayAdapter<CharSequence> funktionsAdapter = ArrayAdapter.createFromResource(this,
                R.array.funktionsgruppen, android.R.layout.simple_spinner_item);
        funktionsAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerFunktionsgruppe.setAdapter(funktionsAdapter);

        // Funktionsstufe Spinner
        ArrayAdapter<CharSequence> funktionsstufeAdapter = ArrayAdapter.createFromResource(this,
                R.array.funktionsstufen, android.R.layout.simple_spinner_item);
        funktionsstufeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerFunktionsstufe.setAdapter(funktionsstufeAdapter);
    }

    private void setupListeners() {
        btnBerechnen.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                calculateSalary();
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

    private void calculateSalary() {
        // Get selections
        int verwendungPosition = spinnerVerwendungsgruppe.getSelectedItemPosition();
        int gehaltPosition = spinnerGehaltsstufe.getSelectedItemPosition();
        int funktionsPosition = spinnerFunktionsgruppe.getSelectedItemPosition();
        int funktionsstufePosition = spinnerFunktionsstufe.getSelectedItemPosition();

        // Validate selections
        if (verwendungPosition == 0 || gehaltPosition == 0) {
            // Show error or return
            cardResults.setVisibility(View.GONE);
            return;
        }

        // Extract usage group code (M1, M2, M3)
        String verwendungsKey = extractCode(spinnerVerwendungsgruppe.getSelectedItem().toString());
        int gehaltsstufe = gehaltPosition; // Position 1-19 = Stufe 1-19, Position 20 = daz, Position 21 = DAZ

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
        if (funktionsPosition > 0) {
            String funktionsKey = extractCode(spinnerFunktionsgruppe.getSelectedItem().toString());
            int funktionsstufe = funktionsstufePosition; // 0 for Keine, 1-3 for others

            if (funktionsstufe > 0 && functionAllowanceData.containsKey(funktionsKey)) {
                Map<Integer, Double> stufen = functionAllowanceData.get(funktionsKey);
                if (stufen.containsKey(funktionsstufe)) {
                    funktionszulage = stufen.get(funktionsstufe);
                }
            }
        }

        // Calculate total
        double gesamtgehalt = grundgehalt + funktionszulage;

        // Display results
        tvGrundgehalt.setText(euroFormat.format(grundgehalt));
        tvFunktionszulage.setText(euroFormat.format(funktionszulage));
        tvGesamtgehalt.setText(euroFormat.format(gesamtgehalt));
        cardResults.setVisibility(View.VISIBLE);
    }

    private String extractCode(String text) {
        // Extract M1, M2, M3, F1, F2, etc. from spinner text
        if (text.contains("M1")) return "M1";
        if (text.contains("M2")) return "M2";
        if (text.contains("M3")) return "M3";
        if (text.contains("F1")) return "F1";
        if (text.contains("F2")) return "F2";
        if (text.contains("F3")) return "F3";
        if (text.contains("F4")) return "F4";
        if (text.contains("F5")) return "F5";
        if (text.contains("Keine")) return "Keine";
        return "";
    }
}
