package io.github.assis10t.bobandroid.pojo

import com.google.android.gms.maps.model.LatLng
import com.google.gson.Gson

class Warehouse (
    val _id: String? = null,
    val name: String = "Unnamed Warehouse",
    val merchantId: String? = null,
    val location: Location? = null,
    var items: List<Item> = listOf()
) {
    companion object {
        class Location(
            val latitude: Double = 0.0,
            val longitude: Double = 0.0
        ) {
            fun asLatLng(): LatLng = LatLng(latitude, longitude)
        }

        fun fromString(str: String) = Gson().fromJson(str, Warehouse::class.java)
    }

    override fun toString() = Gson().toJson(this)
}