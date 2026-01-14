package com.weiner.quotesapp

import android.app.Dialog
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.AutoCompleteTextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import androidx.core.widget.addTextChangedListener
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import com.weiner.quotesapp.adapters.CleaningAreaAdapter
import com.weiner.quotesapp.databinding.ActivityMainBinding
import com.weiner.quotesapp.models.CleaningArea
import com.weiner.quotesapp.models.Customer
import com.weiner.quotesapp.models.Quote
import com.weiner.quotesapp.utils.PdfGenerator
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File
import java.text.NumberFormat
import java.util.*

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var areaAdapter: CleaningAreaAdapter
    private val currencyFormat = NumberFormat.getCurrencyInstance(Locale.GERMANY)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupRecyclerView()
        setupListeners()
        updateTotals()
    }

    private fun setupRecyclerView() {
        areaAdapter = CleaningAreaAdapter(mutableListOf()) { area ->
            showDeleteConfirmation(area)
        }

        binding.recyclerAreas.apply {
            layoutManager = LinearLayoutManager(this@MainActivity)
            adapter = areaAdapter
        }
    }

    private fun setupListeners() {
        binding.btnAddArea.setOnClickListener {
            showAddAreaDialog()
        }

        binding.btnGeneratePdf.setOnClickListener {
            generateQuote()
        }

        binding.btnSendEmail.setOnClickListener {
            sendQuoteByEmail()
        }

        // Update totals when customer data changes
        val textWatcher = {
            updateTotals()
        }

        binding.editCustomerName.addTextChangedListener { textWatcher() }
        binding.editCustomerAddress.addTextChangedListener { textWatcher() }
        binding.editCustomerCity.addTextChangedListener { textWatcher() }
        binding.editCustomerEmail.addTextChangedListener { textWatcher() }
        binding.editCustomerPhone.addTextChangedListener { textWatcher() }
    }

    private fun showAddAreaDialog() {
        val dialog = Dialog(this)
        dialog.setContentView(R.layout.dialog_add_area)
        dialog.window?.setLayout(
            (resources.displayMetrics.widthPixels * 0.9).toInt(),
            android.view.ViewGroup.LayoutParams.WRAP_CONTENT
        )

        val editAreaName = dialog.findViewById<TextInputEditText>(R.id.editAreaName)
        val editAreaSize = dialog.findViewById<TextInputEditText>(R.id.editAreaSize)
        val spinnerAreaType = dialog.findViewById<AutoCompleteTextView>(R.id.spinnerAreaType)
        val spinnerFrequency = dialog.findViewById<AutoCompleteTextView>(R.id.spinnerFrequency)
        val editPricePerSqm = dialog.findViewById<TextInputEditText>(R.id.editPricePerSqm)
        val btnSave = dialog.findViewById<MaterialButton>(R.id.btnSave)
        val btnCancel = dialog.findViewById<MaterialButton>(R.id.btnCancel)

        // Setup spinners
        val areaTypes = resources.getStringArray(R.array.area_types)
        val frequencies = resources.getStringArray(R.array.frequencies)

        spinnerAreaType.setAdapter(
            ArrayAdapter(this, R.layout.dropdown_item, areaTypes)
        )
        spinnerFrequency.setAdapter(
            ArrayAdapter(this, R.layout.dropdown_item, frequencies)
        )

        btnSave.setOnClickListener {
            val name = editAreaName.text?.toString() ?: ""
            val size = editAreaSize.text?.toString()?.toDoubleOrNull() ?: 0.0
            val type = spinnerAreaType.text?.toString() ?: ""
            val frequency = spinnerFrequency.text?.toString() ?: ""
            val price = editPricePerSqm.text?.toString()?.toDoubleOrNull() ?: 0.0

            if (name.isBlank() || size <= 0 || type.isBlank() || frequency.isBlank() || price <= 0) {
                Toast.makeText(this, R.string.fill_all_fields, Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val area = CleaningArea(
                name = name,
                sizeInSqm = size,
                areaType = type,
                frequency = frequency,
                pricePerSqm = price
            )

            areaAdapter.addArea(area)
            updateTotals()
            Toast.makeText(this, R.string.area_added, Toast.LENGTH_SHORT).show()
            dialog.dismiss()
        }

        btnCancel.setOnClickListener {
            dialog.dismiss()
        }

        dialog.show()
    }

    private fun showDeleteConfirmation(area: CleaningArea) {
        AlertDialog.Builder(this)
            .setTitle(R.string.delete)
            .setMessage("${area.name} löschen?")
            .setPositiveButton(R.string.delete) { _, _ ->
                areaAdapter.removeArea(area)
                updateTotals()
                Toast.makeText(this, R.string.area_deleted, Toast.LENGTH_SHORT).show()
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }

    private fun updateTotals() {
        val areas = areaAdapter.getAreas()
        val monthlyTotal = areas.sumOf { it.calculateMonthlyPrice() }
        val yearlyTotal = monthlyTotal * 12

        binding.txtMonthlyTotal.text = currencyFormat.format(monthlyTotal)
        binding.txtYearlyTotal.text = currencyFormat.format(yearlyTotal)
    }

    private fun getCustomer(): Customer {
        return Customer(
            name = binding.editCustomerName.text?.toString() ?: "",
            address = binding.editCustomerAddress.text?.toString() ?: "",
            city = binding.editCustomerCity.text?.toString() ?: "",
            email = binding.editCustomerEmail.text?.toString() ?: "",
            phone = binding.editCustomerPhone.text?.toString() ?: ""
        )
    }

    private fun generateQuote() {
        val customer = getCustomer()
        val areas = areaAdapter.getAreas()

        if (!customer.isValid()) {
            Toast.makeText(this, "Bitte alle Kundendaten ausfüllen", Toast.LENGTH_SHORT).show()
            return
        }

        if (areas.isEmpty()) {
            Toast.makeText(this, "Bitte mindestens einen Bereich hinzufügen", Toast.LENGTH_SHORT).show()
            return
        }

        val quote = Quote(customer = customer, areas = areas)

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val pdfFile = PdfGenerator.generateQuotePdf(this@MainActivity, quote)

                withContext(Dispatchers.Main) {
                    Toast.makeText(
                        this@MainActivity,
                        "${getString(R.string.pdf_generated)}\n${pdfFile.name}",
                        Toast.LENGTH_LONG
                    ).show()

                    // Open PDF
                    openPdf(pdfFile)
                }
            } catch (e: Exception) {
                e.printStackTrace()
                withContext(Dispatchers.Main) {
                    Toast.makeText(
                        this@MainActivity,
                        "${getString(R.string.error)}: ${e.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }
    }

    private fun openPdf(file: File) {
        val uri = FileProvider.getUriForFile(
            this,
            "${applicationContext.packageName}.fileprovider",
            file
        )

        val intent = Intent(Intent.ACTION_VIEW).apply {
            setDataAndType(uri, "application/pdf")
            flags = Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_ACTIVITY_NO_HISTORY
        }

        if (intent.resolveActivity(packageManager) != null) {
            startActivity(intent)
        } else {
            Toast.makeText(this, "Keine PDF-App gefunden", Toast.LENGTH_SHORT).show()
        }
    }

    private fun sendQuoteByEmail() {
        val customer = getCustomer()
        val areas = areaAdapter.getAreas()

        if (!customer.isValid()) {
            Toast.makeText(this, "Bitte alle Kundendaten ausfüllen", Toast.LENGTH_SHORT).show()
            return
        }

        if (areas.isEmpty()) {
            Toast.makeText(this, "Bitte mindestens einen Bereich hinzufügen", Toast.LENGTH_SHORT).show()
            return
        }

        val quote = Quote(customer = customer, areas = areas)

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val pdfFile = PdfGenerator.generateQuotePdf(this@MainActivity, quote)
                val uri = FileProvider.getUriForFile(
                    this@MainActivity,
                    "${applicationContext.packageName}.fileprovider",
                    pdfFile
                )

                withContext(Dispatchers.Main) {
                    val emailIntent = Intent(Intent.ACTION_SEND).apply {
                        type = "application/pdf"
                        putExtra(Intent.EXTRA_EMAIL, arrayOf(customer.email))
                        putExtra(Intent.EXTRA_SUBJECT, "Angebot ${quote.getQuoteNumber()} - Weiner Gebäudeservice GmbH")
                        putExtra(
                            Intent.EXTRA_TEXT,
                            """
                            Sehr geehrte Damen und Herren,

                            anbei erhalten Sie unser Angebot für die Reinigungsleistungen.

                            Bei Fragen stehen wir Ihnen gerne zur Verfügung.

                            Mit freundlichen Grüßen
                            Weiner Gebäudeservice GmbH
                            """.trimIndent()
                        )
                        putExtra(Intent.EXTRA_STREAM, uri)
                        flags = Intent.FLAG_GRANT_READ_URI_PERMISSION
                    }

                    if (emailIntent.resolveActivity(packageManager) != null) {
                        startActivity(Intent.createChooser(emailIntent, "E-Mail senden"))
                    } else {
                        Toast.makeText(this@MainActivity, "Keine E-Mail-App gefunden", Toast.LENGTH_SHORT).show()
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
                withContext(Dispatchers.Main) {
                    Toast.makeText(
                        this@MainActivity,
                        "${getString(R.string.error)}: ${e.message}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }
    }
}
