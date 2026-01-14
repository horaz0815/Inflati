package com.weiner.quotesapp.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class CleaningArea(
    val id: String = java.util.UUID.randomUUID().toString(),
    var name: String = "",
    var numberOfWorkers: Int = 0,
    var hoursPerSession: Double = 0.0,
    var areaType: String = "",
    var frequency: String = "",
    var pricePerHour: Double = 0.0
) : Parcelable {

    /**
     * Berechnet den monatlichen Preis für diesen Bereich
     * Formel: Anzahl Arbeiter × Stunden × Preis/Stunde × Häufigkeitsfaktor
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

        return numberOfWorkers * hoursPerSession * pricePerHour * frequencyMultiplier
    }

    fun isValid(): Boolean {
        return name.isNotBlank() &&
               numberOfWorkers > 0 &&
               hoursPerSession > 0 &&
               areaType.isNotBlank() &&
               frequency.isNotBlank() &&
               pricePerHour > 0
    }
}
