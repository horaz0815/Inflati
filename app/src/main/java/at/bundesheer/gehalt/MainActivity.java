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

    // Inner class to store salary calculation results
    private static class SalaryResult {
        double grundgehalt;
        double funktionszulage;
        double nebengebuehren;
        double gesamtgehalt;

        SalaryResult(double grund, double funktion, double neben) {
            this.grundgehalt = grund;
            this.funktionszulage = funktion;
            this.nebengebuehren = neben;
            this.gesamtgehalt = grund + funktion + neben;
        }
    }

    // Inner class to store Luftfahrttechniker allowance components
    private static class LuftfahrtAllowance {
        double aeZivil;      // AE Zivil (Fixbetrag)
        double ezFaktor;     // EZ vH RB (Faktor)
        double mlzFaktor;    // MLZ vH RB (Faktor)
        double vergMilitar;  // Vergütung Militär (Fixbetrag)

        LuftfahrtAllowance(double ae, double ez, double mlz, double verg) {
            this.aeZivil = ae;
            this.ezFaktor = ez;
            this.mlzFaktor = mlz;
            this.vergMilitar = verg;
        }

        double calculate() {
            final double SOCKELBETRAG = 34.0983;
            return aeZivil + (ezFaktor * SOCKELBETRAG) + (mlzFaktor * SOCKELBETRAG) + vergMilitar;
        }
    }

    private Spinner spinnerVerwendungsgruppe;
    private Spinner spinnerGehaltsstufe;
    private Spinner spinnerFunktionsubergruppe;
    private Spinner spinnerFunktionsgruppe;
    private Spinner spinnerFunktionsstufe;
    private Spinner spinnerLuftfahrttechniker;
    private Spinner spinnerLuftfahrtDetail;
    private TextView tvLuftfahrtDetail;
    private Button btnBerechnen;
    private Button btnVergleichHinzufuegen;
    private Button btnVergleichZuruecksetzen;
    private CardView cardResults;
    private CardView cardComparison;
    private TextView tvGrundgehalt;
    private TextView tvFunktionszulage;
    private TextView tvNebengebuehren;
    private TextView tvGesamtgehalt;

    // Comparison TextViews
    private TextView tvGrundgehaltA;
    private TextView tvFunktionszulageA;
    private TextView tvNebengebuehrenA;
    private TextView tvGesamtgehaltA;
    private TextView tvGrundgehaltB;
    private TextView tvFunktionszulageB;
    private TextView tvNebengebuehrenB;
    private TextView tvGesamtgehaltB;
    private TextView tvDifferenz;

    private DecimalFormat euroFormat = new DecimalFormat("€ #,##0.00");

    // Comparison data
    private SalaryResult salaryA = null;
    private SalaryResult currentSalary = null;  // Store current calculation

    // Salary data structure: Verwendungsgruppe -> Gehaltsstufe -> Amount
    private Map<String, Map<Integer, Double>> salaryData;

    // Function allowance data: Übergruppe -> Funktionsgruppe -> Funktionsstufe -> Amount
    private Map<String, Map<Integer, Map<Integer, Double>>> functionAllowanceData;

    // Luftfahrttechniker allowance data: Category -> Detail -> LuftfahrtAllowance
    private Map<Integer, Map<Integer, LuftfahrtAllowance>> luftfahrtAllowanceData;

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

        // LUFTFAHRTTECHNIKER-NEBENGEBÜHREN (Stand 01.01.2025)
        // Berechnung: AE Zivil + (EZ * 34,0983) + (MLZ * 34,0983) + Vergütung Militär
        luftfahrtAllowanceData = new HashMap<>();

        // 0: Keine
        Map<Integer, LuftfahrtAllowance> keine = new HashMap<>();
        keine.put(0, new LuftfahrtAllowance(0, 0, 0, 0));
        luftfahrtAllowanceData.put(0, keine);

        // 1: Assistenzdienst
        Map<Integer, LuftfahrtAllowance> assistenz = new HashMap<>();
        assistenz.put(1, new LuftfahrtAllowance(11.00, 2.00, 0, 15.30));      // ohne Beruf
        assistenz.put(2, new LuftfahrtAllowance(11.00, 2.00, 3.17, 29.40));   // mit Beruf
        luftfahrtAllowanceData.put(1, assistenz);

        // 2: Wart (MLuFWart)
        Map<Integer, LuftfahrtAllowance> wart = new HashMap<>();
        wart.put(1, new LuftfahrtAllowance(14.60, 2.67, 4.00, 102.20));       // Basis
        wart.put(2, new LuftfahrtAllowance(14.60, 3.60, 4.00, 102.20));       // 1 Typ
        wart.put(3, new LuftfahrtAllowance(14.60, 4.53, 4.00, 102.20));       // 2 Typ
        wart.put(4, new LuftfahrtAllowance(14.60, 3.34, 4.00, 102.20));       // 1 FEW
        wart.put(5, new LuftfahrtAllowance(14.60, 4.01, 4.00, 102.20));       // 2 FEW
        wart.put(6, new LuftfahrtAllowance(14.60, 4.27, 4.00, 102.20));       // 1 FEW + 1 Typ
        wart.put(7, new LuftfahrtAllowance(14.60, 5.20, 4.00, 102.20));       // 1 FEW + 2 Typ
        wart.put(8, new LuftfahrtAllowance(14.60, 4.94, 4.00, 102.20));       // 2 FEW + 1 Typ
        wart.put(9, new LuftfahrtAllowance(14.60, 5.87, 4.00, 102.20));       // 2 FEW + 2 Typ
        luftfahrtAllowanceData.put(2, wart);

        // 3: Wart I (MLuFWart I. Kl)
        Map<Integer, LuftfahrtAllowance> wartI = new HashMap<>();
        wartI.put(1, new LuftfahrtAllowance(14.60, 2.67, 6.01, 276.90));      // Basis
        wartI.put(2, new LuftfahrtAllowance(14.60, 3.60, 6.01, 276.90));      // 1 Typ
        wartI.put(3, new LuftfahrtAllowance(14.60, 4.53, 6.01, 276.90));      // 2 Typ
        wartI.put(4, new LuftfahrtAllowance(14.60, 4.54, 6.01, 276.90));      // 1 FEW
        wartI.put(5, new LuftfahrtAllowance(14.60, 6.41, 6.01, 276.90));      // 2 FEW
        wartI.put(6, new LuftfahrtAllowance(14.60, 5.47, 6.01, 276.90));      // 1 FEW + 1 Typ
        wartI.put(7, new LuftfahrtAllowance(14.60, 6.40, 6.01, 276.90));      // 1 FEW + 2 Typ
        wartI.put(8, new LuftfahrtAllowance(14.60, 7.34, 6.01, 276.90));      // 2 FEW + 1 Typ
        wartI.put(9, new LuftfahrtAllowance(14.60, 8.27, 6.01, 276.90));      // 2 FEW + 2 Typ
        luftfahrtAllowanceData.put(3, wartI);

        // 4: Luftfahrtmeister (MLuFMst)
        Map<Integer, LuftfahrtAllowance> meister = new HashMap<>();
        meister.put(1, new LuftfahrtAllowance(14.60, 2.67, 8.68, 437.80));    // Basis
        meister.put(2, new LuftfahrtAllowance(14.60, 3.60, 8.68, 437.80));    // 1 Typ
        meister.put(3, new LuftfahrtAllowance(14.60, 4.53, 8.68, 437.80));    // 2 Typ
        meister.put(4, new LuftfahrtAllowance(14.60, 4.00, 8.68, 437.80));    // 1 FEW
        meister.put(5, new LuftfahrtAllowance(14.60, 5.33, 8.68, 437.80));    // 2 FEW
        meister.put(6, new LuftfahrtAllowance(14.60, 4.93, 8.68, 437.80));    // 1 FEW + 1 Typ
        meister.put(7, new LuftfahrtAllowance(14.60, 5.86, 8.68, 437.80));    // 1 FEW + 2 Typ
        meister.put(8, new LuftfahrtAllowance(14.60, 6.26, 8.68, 437.80));    // 2 FEW + 1 Typ
        meister.put(9, new LuftfahrtAllowance(14.60, 7.19, 8.68, 437.80));    // 2 FEW + 2 Typ
        luftfahrtAllowanceData.put(4, meister);

        // 5: Ltd Dienst B wertig
        Map<Integer, LuftfahrtAllowance> ltdB = new HashMap<>();
        ltdB.put(1, new LuftfahrtAllowance(7.30, 21.90, 4.00, 335.80));       // Standard
        ltdB.put(2, new LuftfahrtAllowance(7.30, 21.90, 5.33, 335.80));       // nach einem Jahr
        luftfahrtAllowanceData.put(5, ltdB);

        // 6: Ltd Dienst A wertig
        Map<Integer, LuftfahrtAllowance> ltdA = new HashMap<>();
        ltdA.put(1, new LuftfahrtAllowance(7.30, 21.90, 4.00, 248.90));       // Standard
        ltdA.put(2, new LuftfahrtAllowance(7.30, 21.90, 5.33, 248.90));       // nach einem Jahr
        luftfahrtAllowanceData.put(6, ltdA);
    }

    private void initializeViews() {
        spinnerVerwendungsgruppe = findViewById(R.id.spinnerVerwendungsgruppe);
        spinnerGehaltsstufe = findViewById(R.id.spinnerGehaltsstufe);
        spinnerFunktionsubergruppe = findViewById(R.id.spinnerFunktionsubergruppe);
        spinnerFunktionsgruppe = findViewById(R.id.spinnerFunktionsgruppe);
        spinnerFunktionsstufe = findViewById(R.id.spinnerFunktionsstufe);
        spinnerLuftfahrttechniker = findViewById(R.id.spinnerLuftfahrttechniker);
        spinnerLuftfahrtDetail = findViewById(R.id.spinnerLuftfahrtDetail);
        tvLuftfahrtDetail = findViewById(R.id.tvLuftfahrtDetail);
        btnBerechnen = findViewById(R.id.btnBerechnen);
        btnVergleichHinzufuegen = findViewById(R.id.btnVergleichHinzufuegen);
        btnVergleichZuruecksetzen = findViewById(R.id.btnVergleichZuruecksetzen);
        cardResults = findViewById(R.id.cardResults);
        cardComparison = findViewById(R.id.cardComparison);
        tvGrundgehalt = findViewById(R.id.tvGrundgehalt);
        tvFunktionszulage = findViewById(R.id.tvFunktionszulage);
        tvNebengebuehren = findViewById(R.id.tvNebengebuehren);
        tvGesamtgehalt = findViewById(R.id.tvGesamtgehalt);

        // Comparison TextViews
        tvGrundgehaltA = findViewById(R.id.tvGrundgehaltA);
        tvFunktionszulageA = findViewById(R.id.tvFunktionszulageA);
        tvNebengebuehrenA = findViewById(R.id.tvNebengebuehrenA);
        tvGesamtgehaltA = findViewById(R.id.tvGesamtgehaltA);
        tvGrundgehaltB = findViewById(R.id.tvGrundgehaltB);
        tvFunktionszulageB = findViewById(R.id.tvFunktionszulageB);
        tvNebengebuehrenB = findViewById(R.id.tvNebengebuehrenB);
        tvGesamtgehaltB = findViewById(R.id.tvGesamtgehaltB);
        tvDifferenz = findViewById(R.id.tvDifferenz);
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

        // Update Luftfahrt-Detail based on Luftfahrttechniker selection
        spinnerLuftfahrttechniker.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                updateLuftfahrtDetailSpinner(position);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });

        // Comparison button listeners
        btnVergleichHinzufuegen.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                addToComparison();
            }
        });

        btnVergleichZuruecksetzen.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetComparison();
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

    private void updateLuftfahrtDetailSpinner(int luftfahrtPosition) {
        ArrayAdapter<CharSequence> adapter;

        switch (luftfahrtPosition) {
            case 1: // Assistenzdienst
                adapter = ArrayAdapter.createFromResource(this,
                        R.array.luft_assistenz, android.R.layout.simple_spinner_item);
                tvLuftfahrtDetail.setVisibility(View.VISIBLE);
                spinnerLuftfahrtDetail.setVisibility(View.VISIBLE);
                break;
            case 2: // Wart (MLuFWart)
            case 3: // Wart I (MLuFWart I. Kl)
            case 4: // Luftfahrtmeister (MLuFMst)
                adapter = ArrayAdapter.createFromResource(this,
                        R.array.luft_wart, android.R.layout.simple_spinner_item);
                tvLuftfahrtDetail.setVisibility(View.VISIBLE);
                spinnerLuftfahrtDetail.setVisibility(View.VISIBLE);
                break;
            case 5: // Ltd Dienst B wertig
            case 6: // Ltd Dienst A wertig
                adapter = ArrayAdapter.createFromResource(this,
                        R.array.luft_ltd, android.R.layout.simple_spinner_item);
                tvLuftfahrtDetail.setVisibility(View.VISIBLE);
                spinnerLuftfahrtDetail.setVisibility(View.VISIBLE);
                break;
            default: // Keine
                adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item);
                adapter.add("Keine");
                tvLuftfahrtDetail.setVisibility(View.GONE);
                spinnerLuftfahrtDetail.setVisibility(View.GONE);
                break;
        }

        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerLuftfahrtDetail.setAdapter(adapter);
        spinnerLuftfahrtDetail.setSelection(0);
    }

    private void calculateSalary() {
        // Get selections
        int verwendungPosition = spinnerVerwendungsgruppe.getSelectedItemPosition();
        int gehaltPosition = spinnerGehaltsstufe.getSelectedItemPosition();
        int ubergruppePosition = spinnerFunktionsubergruppe.getSelectedItemPosition();
        int funktionsgruppePosition = spinnerFunktionsgruppe.getSelectedItemPosition();
        int funktionsstufePosition = spinnerFunktionsstufe.getSelectedItemPosition();
        int luftfahrtPosition = spinnerLuftfahrttechniker.getSelectedItemPosition();
        int luftfahrtDetailPosition = spinnerLuftfahrtDetail.getSelectedItemPosition();

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
        if (luftfahrtPosition > 0 && luftfahrtDetailPosition > 0) {
            if (luftfahrtAllowanceData.containsKey(luftfahrtPosition)) {
                Map<Integer, LuftfahrtAllowance> details = luftfahrtAllowanceData.get(luftfahrtPosition);
                if (details.containsKey(luftfahrtDetailPosition)) {
                    LuftfahrtAllowance allowance = details.get(luftfahrtDetailPosition);
                    nebengebuehren = allowance.calculate();
                }
            }
        }

        // Calculate total and store result
        currentSalary = new SalaryResult(grundgehalt, funktionszulage, nebengebuehren);

        // Display results
        tvGrundgehalt.setText(euroFormat.format(currentSalary.grundgehalt));
        tvFunktionszulage.setText(euroFormat.format(currentSalary.funktionszulage));
        tvNebengebuehren.setText(euroFormat.format(currentSalary.nebengebuehren));
        tvGesamtgehalt.setText(euroFormat.format(currentSalary.gesamtgehalt));
        cardResults.setVisibility(View.VISIBLE);

        // Check if we should show comparison
        if (salaryA != null) {
            // This is Salary B - show comparison
            showComparison(currentSalary);
        } else {
            // First calculation - show comparison button
            btnVergleichHinzufuegen.setVisibility(View.VISIBLE);
        }
    }

    private void addToComparison() {
        // Save current calculation as Salary A
        if (currentSalary != null) {
            salaryA = currentSalary;

            // Hide comparison button
            btnVergleichHinzufuegen.setVisibility(View.GONE);

            // Reset form for second calculation
            // The user can now enter different values and calculate again
            // When they click "Berechnen", it will trigger the comparison
        }
    }

    private void resetComparison() {
        salaryA = null;
        cardComparison.setVisibility(View.GONE);
        btnVergleichHinzufuegen.setVisibility(View.VISIBLE);
    }

    private void showComparison(SalaryResult salaryB) {
        if (salaryA == null || salaryB == null) {
            return;
        }

        // Display Salary A
        tvGrundgehaltA.setText(euroFormat.format(salaryA.grundgehalt));
        tvFunktionszulageA.setText(euroFormat.format(salaryA.funktionszulage));
        tvNebengebuehrenA.setText(euroFormat.format(salaryA.nebengebuehren));
        tvGesamtgehaltA.setText(euroFormat.format(salaryA.gesamtgehalt));

        // Display Salary B
        tvGrundgehaltB.setText(euroFormat.format(salaryB.grundgehalt));
        tvFunktionszulageB.setText(euroFormat.format(salaryB.funktionszulage));
        tvNebengebuehrenB.setText(euroFormat.format(salaryB.nebengebuehren));
        tvGesamtgehaltB.setText(euroFormat.format(salaryB.gesamtgehalt));

        // Force refresh the TextViews
        tvNebengebuehrenB.invalidate();
        tvNebengebuehrenB.requestLayout();

        // Calculate and display difference (B - A)
        double differenz = salaryB.gesamtgehalt - salaryA.gesamtgehalt;
        String differenzText = (differenz >= 0 ? "+ " : "- ") +
                              euroFormat.format(Math.abs(differenz)).replace("€", "€ ");
        tvDifferenz.setText(differenzText);

        // Show comparison card
        cardComparison.setVisibility(View.VISIBLE);
    }

    private double parseEuro(String euroString) {
        try {
            // Remove "€" and whitespace, replace comma with dot
            String cleaned = euroString.replace("€", "").replace(" ", "").replace(".", "").replace(",", ".");
            return Double.parseDouble(cleaned);
        } catch (Exception e) {
            return 0.0;
        }
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
