package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.widget.TextView
import io.github.assis10t.bobandroid.pojo.Item
import kotlinx.android.synthetic.main.dialog_add_to_cart.*
import timber.log.Timber

class AddToCartDialog(context: Context, val item: Item): Dialog(context) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_add_to_cart)

        title.text = item.name
        price.text = item.getPriceText()
        total.text = "£${"%.2f".format(item.price)}"
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
                item.price
            )
            addToCart(context, cartItem)
            Timber.d("Cart: ${getCart(context)}")
            dismiss()
        }
    }
}