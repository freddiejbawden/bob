package io.github.assis10t.bobandroid

import android.app.Activity
import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.support.v7.widget.CardView
import android.support.v7.widget.GridLayoutManager
import android.support.v7.widget.RecyclerView
import android.view.*
import android.widget.ImageView
import android.widget.TextView
import com.bumptech.glide.Glide
import com.bumptech.glide.load.resource.drawable.DrawableTransitionOptions
import io.github.assis10t.bobandroid.pojo.Item
import io.github.assis10t.bobandroid.pojo.Order
import io.github.assis10t.bobandroid.pojo.Warehouse
import kotlinx.android.synthetic.main.activity_warehouse.*
import timber.log.Timber


class WarehouseActivity : ActivityWithLoginMenu() {

    lateinit var warehouseId: String
    var warehouse: Warehouse? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_warehouse)

        warehouseId = intent.getStringExtra("warehouseId")
        val warehouseName = intent.getStringExtra("warehouseName")

        supportActionBar?.setDisplayShowHomeEnabled(true)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setHomeButtonEnabled(true)
        supportActionBar?.title = warehouseName

        container.setOnRefreshListener { refreshItems() }
        item_list.layoutManager = GridLayoutManager(this, 2)
        item_list.adapter = ItemAdapter()
//        (item_list.adapter as ItemAdapter).updateOrders(listOf(
//            Item("some_id2", "some_id", "My Item", "my_img", null, null, null, 1.25)
//        )) //TODO: Remove this.
        view_cart.setOnClickListener {
            ViewCartDialog(this, warehouseId).show()
        }
    }

    override fun onResume() {
        super.onResume()

        refreshItems()
    }

    fun refreshItems() {
        container.isRefreshing = true
        ServerConnection().getWarehouse(warehouseId) { err, warehouse ->
            container.isRefreshing = false
            if (err != null) {
                Timber.e("getWarehouse failed. $err")
                return@getWarehouse
            }
            if (warehouse == null) {
                Timber.e("Warehouse $warehouseId not found.")
                return@getWarehouse
            }
            this.warehouse = warehouse
            val items = warehouse.items!!
            Timber.d("GetWarehouse success. Items: ${items.size}")
            val adapter = item_list.adapter as ItemAdapter
            adapter.updateItems(items)
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

    class ItemAdapter: RecyclerView.Adapter<ItemAdapter.ViewHolder>() {
        var itemList: List<Item> = listOf()

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.fragment_warehouse_item, parent, false)
            return ViewHolder(view)
        }

        override fun getItemCount(): Int = itemList.size

        override fun onBindViewHolder(vh: ViewHolder, pos: Int) {
            val item = itemList[pos]
            vh.title.text = item.name
            vh.price.text = item.getPriceText()
            vh.container.setOnClickListener {v ->
                AddToCartDialog(v.context, item).show()
            }
            if (item.image == null) {
                Glide.with(vh.container)
                    .clear(vh.image)
                vh.image.setImageDrawable(null)
            } else {
                Glide.with(vh.container)
                    .load(base64ToByteArray(item.image))
                    .transition(DrawableTransitionOptions.withCrossFade())
                    .into(vh.image)
            }
        }

        fun updateItems(items: List<Item>) {
            this.itemList = items
            notifyDataSetChanged()
        }

        class ViewHolder(view: View): RecyclerView.ViewHolder(view) {
            val title: TextView = view.findViewById(R.id.title)
            val price: TextView = view.findViewById(R.id.price)
            val container: CardView = view.findViewById(R.id.container)
            val image: ImageView = view.findViewById(R.id.image)
        }
    }
}
