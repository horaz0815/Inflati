package com.weiner.quotesapp.models

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Customer(
    var name: String = "",
    var address: String = "",
    var city: String = "",
    var email: String = "",
    var phone: String = ""
) : Parcelable {

    fun isValid(): Boolean {
        return name.isNotBlank() &&
               address.isNotBlank() &&
               city.isNotBlank() &&
               email.isNotBlank()
    }
}
