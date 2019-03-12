package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.support.v7.widget.LinearLayoutManager
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import io.github.assis10t.bobandroid.pojo.Item
import io.github.assis10t.bobandroid.pojo.Order
import kotlinx.android.synthetic.main.dialog_view_cart.*

class ViewCartDialog(val activity: WarehouseActivity, val warehouseId: String): Dialog(activity) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val data = getCart(context)
        if (data.isEmpty()) {
            setContentView(R.layout.dialog_view_cart_empty)
            return
        } else {
            setContentView(R.layout.dialog_view_cart)
        }

        cart.layoutManager = LinearLayoutManager(context, LinearLayoutManager.VERTICAL, false)
        cart.adapter = CartAdapter(data)

        val totalAmount =
            if (data.isEmpty())
                0.0
            else
                data
                    .map{ it.quantity!! * it.price }
                    .reduce { a, b -> a + b}

        total.text = "£${"%.2f".format(totalAmount)}"

        clear.setOnClickListener {
            clearCart(context)
            if (context is WarehouseActivity)
                (context as WarehouseActivity).refreshItems()
            dismiss()
        }

        complete_order.setOnClickListener {
            val order = Order.Factory()
                .items(data)
                .warehouseId(warehouseId)
                .build()

            val submitDialog = SubmittingOrderDialog(context)
            submitDialog.show()

            Handler().postDelayed({
                ServerConnection()
                    .makeOrder(context, order) { err ->
                        if (err != null) {
                            Toast.makeText(context, err.message, Toast.LENGTH_LONG).show()
                            submitDialog.dismiss()
                            return@makeOrder
                        }
                        clearCart(context)
                        activity.refreshItems()
                        submitDialog.completed()
                        Handler().postDelayed({
                            submitDialog.dismiss()
                            dismiss()
                        }, 2000)
                    }
            }, 2000)
        }
    }

    class CartAdapter(val items: List<Item>): RecyclerView.Adapter<CartAdapter.ViewHolder>() {
        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.fragment_cart_item, parent, false)
            return ViewHolder(view)
        }

        override fun getItemCount(): Int = items.size

        override fun onBindViewHolder(vh: ViewHolder, pos: Int) {
            val item = items[pos]
            vh.name.text = item.name
            vh.quantity.text = "${item.quantity}"
            vh.price.text =
                if (item.unit == null)
                    "£${"%.2f".format(item.price)}"
                else
                    "£${"%.2f".format(item.price)}/${item.unit}"
        }

        class ViewHolder(v: View): RecyclerView.ViewHolder(v) {
            val name: TextView = v.findViewById(R.id.name)
            val quantity: TextView = v.findViewById(R.id.quantity)
            val price: TextView = v.findViewById(R.id.price)
        }
    }
}