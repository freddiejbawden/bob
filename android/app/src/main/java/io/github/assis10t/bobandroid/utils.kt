package io.github.assis10t.bobandroid

import android.app.Activity
import android.content.Context
import android.content.SharedPreferences
import android.graphics.Bitmap
import android.util.TypedValue
import android.provider.SyncStateContract.Helpers.update
import android.util.Base64
import android.view.View
import com.google.gson.Gson
import com.google.zxing.BarcodeFormat
import com.google.zxing.MultiFormatWriter
import com.journeyapps.barcodescanner.BarcodeEncoder
import io.github.assis10t.bobandroid.pojo.Cart
import io.github.assis10t.bobandroid.pojo.Item
import kotlinx.android.synthetic.main.dialog_add_to_cart.*
import timber.log.Timber
import java.security.NoSuchAlgorithmException
import java.text.SimpleDateFormat
import java.time.LocalDateTime
import java.util.*


fun dp(context: Context, dp: Float) =
    TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dp, context.resources.displayMetrics)

fun getCurrentTimeString(): String {
    val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.UK)
    return sdf.format(Date())
}

fun parseISODate(str: String): Date {
    val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSXXX", Locale.UK)
    return sdf.parse(str)
}

fun addToCart(context: Context, item: Item): Boolean {
    if (item._id == null || item.quantity == null) {
        return false
    }
    val preferences = context.getSharedPreferences("bob", Context.MODE_PRIVATE)
    val cart = getCart(context)

    val cartItem = cart.items[item._id]
    val newCartItem = Item(
        item._id,
        item.warehouseId,
        item.name,
        null,
        item.position,
        (cartItem?.quantity ?: 0.0) + item.quantity,
        item.unit,
        item.price,
        item.size
    )
    cart.items[item._id] = newCartItem

    preferences.edit()
        .putString("cart", Gson().toJson(cart))
        .commit()
    return true
}

fun getCart(context: Context): Cart =
    Gson().fromJson(
        context
            .getSharedPreferences("bob", Context.MODE_PRIVATE)
            .getString("cart", Gson().toJson(Cart())),
        Cart::class.java
    )


fun clearCart(context: Context) {
    val preferences = context.getSharedPreferences("bob", Context.MODE_PRIVATE)
    preferences.edit().remove("cart").commit()
}

fun base64ToByteArray(str: String): ByteArray? {
    //Removing data:image/jpg;base64, from the beginning.
    val pureStr = str.substring(str.indexOf(",")+1)
    val bytes = Base64.decode(pureStr, Base64.DEFAULT)
    return bytes
}

fun generateQRCode(str: String): Bitmap {
    val bitMatrix = MultiFormatWriter().encode(str, BarcodeFormat.QR_CODE, 300, 300)
    return BarcodeEncoder().createBitmap(bitMatrix)
}

fun snackbarView(activity: Activity): View
        = activity.findViewById(R.id.view_cart)
        ?: activity.findViewById(android.R.id.content)