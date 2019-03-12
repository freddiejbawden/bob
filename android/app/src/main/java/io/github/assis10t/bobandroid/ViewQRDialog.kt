package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.os.Bundle
import com.bumptech.glide.Glide
import io.github.assis10t.bobandroid.pojo.Order
import kotlinx.android.synthetic.main.dialog_view_qr.*

class ViewQRDialog(context: Context, val order: Order): Dialog(context) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_view_qr)

        message.text = "Show this code to the cashier at ${order.warehouse!!.name}."

        Glide.with(context)
            .load(generateQRCode(order._id!!))
            .into(qr)
    }
}