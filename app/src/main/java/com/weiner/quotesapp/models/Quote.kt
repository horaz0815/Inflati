package com.weiner.quotesapp.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize
import java.text.SimpleDateFormat
import java.util.*

@Parcelize
data class Quote(
    val id: String = java.util.UUID.randomUUID().toString(),
    val customer: Customer,
    val areas: List<CleaningArea>,
    val createdDate: Date = Date(),
    val validUntilDate: Date = calculateValidUntilDate()
) : Parcelable {

    companion object {
        private fun calculateValidUntilDate(): Date {
            val calendar = Calendar.getInstance()
            calendar.add(Calendar.DAY_OF_YEAR, 30) // Angebot gilt 30 Tage
            return calendar.time
        }
    }

    /**
     * Berechnet den monatlichen Gesamtpreis
     */
    fun calculateMonthlyTotal(): Double {
        return areas.sumOf { it.calculateMonthlyPrice() }
    }

    /**
     * Berechnet den jährlichen Gesamtpreis
     */
    fun calculateYearlyTotal(): Double {
        return calculateMonthlyTotal() * 12
    }

    /**
     * Formatiert das Datum
     */
    fun getFormattedDate(): String {
        val dateFormat = SimpleDateFormat("dd.MM.yyyy", Locale.GERMAN)
        return dateFormat.format(createdDate)
    }

    fun getFormattedValidUntilDate(): String {
        val dateFormat = SimpleDateFormat("dd.MM.yyyy", Locale.GERMAN)
        return dateFormat.format(validUntilDate)
    }

    /**
     * Generiert eine Angebotsnummer
     */
    fun getQuoteNumber(): String {
        val dateFormat = SimpleDateFormat("yyyyMMdd", Locale.GERMAN)
        return "ANG-${dateFormat.format(createdDate)}-${id.substring(0, 6).uppercase()}"
    }
}
