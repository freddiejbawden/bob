package io.github.assis10t.bobandroid.pojo

import com.google.gson.Gson

class Item (
    val _id: String? = null,
    val warehouseId: String? = null,
    val name: String? = null,
    val image: String? = null,
    val position: Position? = null,
    val quantity: Double? = null,
    val unit: String? = null,
    val price: Double = 0.0,
    val size: String? = null
) {
    companion object {
        fun fromString(str: String) = Gson().fromJson(str, Item::class.java)
    }

    fun getPriceText() = "£${"%.2f".format(price)}/${unit?:"item"}"

    override fun toString() = Gson().toJson(this)
}
