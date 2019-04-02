package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.TextView
import com.bumptech.glide.Glide
import com.bumptech.glide.load.resource.drawable.DrawableTransitionOptions
import io.github.assis10t.bobandroid.pojo.Item
import kotlinx.android.synthetic.main.dialog_add_to_cart.*
import timber.log.Timber

class AddToCartDialog(val activity: WarehouseActivity, val item: Item): Dialog(activity) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_add_to_cart)

        title.text = item.name
        price.text = item.getPriceText()
        total.text = "£${"%.2f".format(item.price)}"

        if (item.image == null) {
            image.visibility = View.GONE
        } else {
            image.visibility = View.VISIBLE
            Glide.with(context)
                .load(base64ToByteArray(item.image))
                .into(image)
        }

        quantity.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(s: Editable?) {}
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                val amountSelected = s.toString().toIntOrNull()
                if (amountSelected != null) {
                    total.text = "£${"%.2f".format(amountSelected * item.price)}"
                    add_to_cart.isEnabled = (item.quantity == null || amountSelected <= item.quantity) && amountSelected > 0
                } else {
                    total.text = ""
                    add_to_cart.isEnabled = false
                }
            }
        })

        add_to_cart.setOnClickListener {
            val cartItem = Item(
                item._id,
                item.warehouseId,
                item.name,
                item.image,
                item.position,
                Integer.parseInt(quantity.text.toString()).toDouble(),
                item.unit,
                item.price,
                item.size
            )
            addToCart(context, cartItem)
            activity.refreshItems()
            Timber.d("Cart: ${getCart(context)}")
            val dialog = AddedToCartDialog(context)
            dialog.show()
            Handler().postDelayed({
                dialog.dismiss()
                dismiss()
            }, 1000)
        }
    }
}