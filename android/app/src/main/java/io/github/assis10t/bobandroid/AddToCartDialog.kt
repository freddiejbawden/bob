package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.graphics.Color
import android.os.Bundle
import android.os.Handler
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.widget.TextView
import android.widget.Toast
import com.bumptech.glide.Glide
import com.bumptech.glide.load.resource.drawable.DrawableTransitionOptions
import com.cesarferreira.pluralize.pluralize
import com.cesarferreira.pluralize.singularize
import com.cesarferreira.pluralize.utils.Plurality
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

        val unitText =
            if (item.quantity!!.toInt() == 1)
                (item.unit?:"item").singularize()
            else
                (item.unit?:"item").pluralize()

        unit.text = "${item.quantity.toInt()} $unitText"

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
                    if (amountSelected <= item.quantity && amountSelected > 0) {
                        add_to_cart.isEnabled = true
                        unit.setTextColor(Color.parseColor("#89000000"))
                    } else {
                        add_to_cart.isEnabled = false
                        unit.setTextColor(Color.parseColor("#89FF0000"))
                    }
                } else {
                    total.text = ""
                    add_to_cart.isEnabled = false
                    unit.setTextColor(Color.parseColor("#89000000"))
                }
            }
        })

        add_to_cart.setOnClickListener {
            val cartItem = Item(
                item._id,
                item.warehouseId,
                item.name,
                null,
                item.position,
                Integer.parseInt(quantity.text.toString()).toDouble(),
                item.unit,
                item.price,
                item.size
            )
            val success = addToCart(context, cartItem)
            if (!success) {
                Toast.makeText(context, "Couldn't add item to cart.", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
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