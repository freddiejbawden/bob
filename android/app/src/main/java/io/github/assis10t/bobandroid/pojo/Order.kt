package io.github.assis10t.bobandroid.pojo

import io.github.assis10t.bobandroid.getCurrentTimeString
import io.github.assis10t.bobandroid.parseISODate
import java.text.SimpleDateFormat
import java.util.*

class Order(
    val _id: String? = null,
    val userId: String? = null,
    val warehouseId: String? = null,
    val timestamp: String? = null,
    val items: List<Item> = listOf(),
    val status: Status = Status.PENDING,
    val warehouse: Warehouse? = null
) {
    enum class Status {
        PENDING, IN_TRANSIT, READY_TO_COLLECT, COMPLETE, CANCELED
    }

    class Factory {
        private var _id: String? = null
        private var warehouseId: String? = null
        private var items: List<Item> = listOf()
        private var status: Status = Status.PENDING

        fun id(id: String?): Factory {
            this._id = id
            return this
        }
        fun warehouseId(id: String?): Factory {
            this.warehouseId = id
            return this
        }
        fun items(items: List<Item>): Factory {
            this.items = items
            return this
        }
        fun status(status: Order.Status): Factory {
            this.status = status
            return this
        }
        fun build() = Order (
            _id,
            null,
            warehouseId,
            if (_id == null) getCurrentTimeString() else null,
            items,
            status
        )
    }

    fun getTimeString(): String {
        val date = parseISODate(timestamp!!)
        val sdf = SimpleDateFormat("d MMMM yyyy HH:mm", Locale.UK)
        return sdf.format(date)
    }
}
