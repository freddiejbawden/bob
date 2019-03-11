package io.github.assis10t.bobandroid

import android.os.Bundle
import android.support.v7.widget.CardView
import android.support.v7.widget.LinearLayoutManager
import android.support.v7.widget.RecyclerView
import android.view.LayoutInflater
import android.view.MenuItem
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import io.github.assis10t.bobandroid.pojo.Order
import kotlinx.android.synthetic.main.activity_orders.*

class OrdersActivity : ActivityWithLoginMenu() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_orders)
        supportActionBar?.title = "Orders"

        supportActionBar?.setHomeButtonEnabled(true)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        orders_container.setOnRefreshListener { refresh() }
        orders.layoutManager = LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false)
        orders.adapter = OrderAdapter()
    }

    override fun onResume() {
        super.onResume()
        refresh()
    }

    fun refresh() {
        if (!ServerConnection().isLoggedIn(this)) {
            finish()
            return
        }
        orders_container.isRefreshing = true
        no_orders.visibility = View.GONE
        ServerConnection().getOrders(this) { error, ordrs ->
            orders_container.isRefreshing = false
            if (error != null) {
                Toast.makeText(this, error.message, Toast.LENGTH_LONG).show()
                return@getOrders
            }
            val adapter = orders.adapter as OrderAdapter
            adapter.updateOrders(ordrs!!)
            if (ordrs.isEmpty()) {
                no_orders.visibility = View.VISIBLE
            } else {
                no_orders.visibility = View.GONE
            }
        }
    }
    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        if (item?.itemId == android.R.id.home) {
            finish()
            return true
        } else {
            return super.onOptionsItemSelected(item)
        }
    }

    class OrderAdapter: RecyclerView.Adapter<OrderAdapter.ViewHolder>() {
        var orderList: List<Order> = listOf()

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.fragment_orders_list_item, parent, false)
            return ViewHolder(view)
        }

        override fun getItemCount(): Int = orderList.size

        override fun onBindViewHolder(vh: ViewHolder, pos: Int) {
            val order = orderList[pos]
            vh.title.text = order.warehouse!!.name
            vh.timestamp.text = order.getTimeString()
            vh.container.setOnClickListener {v ->
                Toast.makeText(vh.container.context, "TODO: Open order details dialog", Toast.LENGTH_SHORT).show()
            }
            vh.status.text = when(order.status) {
                Order.Status.PENDING -> "Pending"
                Order.Status.IN_TRANSIT -> "In transit"
                Order.Status.COMPLETE -> "Ready to collect"
                Order.Status.CANCELED -> "Canceled"
            }
            vh.summary.text = "${order.items.size} items"
        }

        fun updateOrders(orders: List<Order>) {
            this.orderList = orders
            notifyDataSetChanged()
        }

        class ViewHolder(view: View): RecyclerView.ViewHolder(view) {
            val container: CardView = view.findViewById(R.id.container)
            val title: TextView = view.findViewById(R.id.title)
            val timestamp: TextView = view.findViewById(R.id.timestamp)
            val summary: TextView = view.findViewById(R.id.summary)
            val status: TextView = view.findViewById(R.id.status)
        }
    }
}
