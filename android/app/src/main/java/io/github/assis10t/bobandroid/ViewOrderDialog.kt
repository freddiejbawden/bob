package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.support.v7.widget.LinearLayoutManager
import android.support.v7.widget.RecyclerView
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import io.github.assis10t.bobandroid.pojo.Item
import io.github.assis10t.bobandroid.pojo.Order
import kotlinx.android.synthetic.main.dialog_view_order.*
import org.w3c.dom.Text
import timber.log.Timber

class ViewOrderDialog(context: Context, val order: Order): Dialog(context) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_view_order)

        cart.layoutManager = LinearLayoutManager(context, LinearLayoutManager.VERTICAL, false)
        cart.adapter = ViewCartDialog.CartAdapter(order.items)

        warehouse_title.text = order.warehouse!!.name
        status.text = when(order.status) {
            Order.Status.PENDING -> "Pending"
            Order.Status.IN_TRANSIT -> "In transit"
            Order.Status.READY_TO_COLLECT -> "Ready"
            Order.Status.COMPLETE -> "Collected"
            Order.Status.CANCELED -> "Canceled"
        }
        status.setTextColor(when(order.status) {
            Order.Status.PENDING -> R.color.statusPending
            Order.Status.IN_TRANSIT -> R.color.statusInTransit
            Order.Status.READY_TO_COLLECT -> R.color.statusReady
            Order.Status.COMPLETE -> R.color.statusComplete
            Order.Status.CANCELED -> R.color.statusCanceled
        })

        view_qr.visibility =
                if (order.status == Order.Status.COMPLETE)
                    View.VISIBLE
                else
                    View.VISIBLE //TODO: Change to View.GONE

        val totalAmount =
            if (order.items.isEmpty())
                0.0
            else
                order.items
                    .map{ it.quantity!! * it.price }
                    .reduce { a, b -> a + b}

        total.text = "£${"%.2f".format(totalAmount)}"


        view_qr.setOnClickListener {
            ViewQRDialog(context, order).show()
        }

        get_directions.setOnClickListener {
            val location = order.warehouse!!.location!!
            val intent = Intent(
                Intent.ACTION_VIEW,
                Uri.parse("https://www.google.com/maps/dir/?api=1&destination=${location.latitude},${location.longitude}")
            )
            context.startActivity(intent)
        }
    }
}