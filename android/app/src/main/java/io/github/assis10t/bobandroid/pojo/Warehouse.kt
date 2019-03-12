package io.github.assis10t.bobandroid.pojo

import com.google.gson.Gson

class Warehouse (
    val _id: String? = null,
    val name: String = "Unnamed Warehouse",
    val merchantId: String? = null,
    val location: Location? = null,
    val items: List<Item>? = null
) {
    companion object {
        class Location(
            val latitude: Double = 0.0,
            val longitude: Double = 0.0
        )

        fun fromString(str: String) = Gson().fromJson(str, Warehouse::class.java)
    }

    override fun toString() = Gson().toJson(this)
}