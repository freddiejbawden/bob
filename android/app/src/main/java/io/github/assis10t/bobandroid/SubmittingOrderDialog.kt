package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.os.Bundle
import android.view.View
import com.bumptech.glide.Glide
import io.github.assis10t.bobandroid.pojo.Order
import kotlinx.android.synthetic.main.dialog_submitting_order.*

class SubmittingOrderDialog(context: Context): Dialog(context) {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_submitting_order)

        setCancelable(false)
        setCanceledOnTouchOutside(false)
    }

    fun completed() {
        loading.visibility = View.GONE
        check.check()
    }
}