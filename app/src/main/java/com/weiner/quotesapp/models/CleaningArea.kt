package com.weiner.quotesapp.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class CleaningArea(
    val id: String = java.util.UUID.randomUUID().toString(),
    var name: String = "",
    var sizeInSqm: Double = 0.0,
    var areaType: String = "",
    var frequency: String = "",
    var pricePerSqm: Double = 0.0
) : Parcelable {

    /**
     * Berechnet den monatlichen Preis für diesen Bereich
     */
    fun calculateMonthlyPrice(): Double {
        val frequencyMultiplier = when (frequency) {
            "Täglich" -> 22.0  // ~22 Arbeitstage pro Monat
            "3x pro Woche" -> 13.0
            "2x pro Woche" -> 8.0
            "Wöchentlich" -> 4.0
            "14-tägig" -> 2.0
            "Monatlich" -> 1.0
            else -> 1.0
        }

        return sizeInSqm * pricePerSqm * frequencyMultiplier
    }

    fun isValid(): Boolean {
        return name.isNotBlank() &&
               sizeInSqm > 0 &&
               areaType.isNotBlank() &&
               frequency.isNotBlank() &&
               pricePerSqm > 0
    }
}
