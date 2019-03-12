package io.github.assis10t.bobandroid

import android.content.Context
import android.content.SharedPreferences
import android.graphics.Bitmap
import android.util.TypedValue
import android.provider.SyncStateContract.Helpers.update
import android.util.Base64
import com.google.zxing.BarcodeFormat
import com.google.zxing.MultiFormatWriter
import com.journeyapps.barcodescanner.BarcodeEncoder
import io.github.assis10t.bobandroid.pojo.Item
import timber.log.Timber
import java.security.NoSuchAlgorithmException
import java.text.SimpleDateFormat
import java.time.LocalDateTime
import java.util.*


fun dp(context: Context, dp: Float) =
    TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dp, context.resources.displayMetrics)

//From: http://www.kospol.gr/204/create-md5-hashes-in-android/
fun md5(s: String): String {
    try {
        // Create MD5 Hash
        val digest = java.security.MessageDigest
            .getInstance("MD5")
        digest.update(s.toByteArray())
        val messageDigest = digest.digest()

        // Create Hex String
        val hexString = StringBuffer()
        for (i in messageDigest.indices) {
            var h = Integer.toHexString(0xFF and messageDigest[i].toInt())
            while (h.length < 2)
                h = "0$h"
            hexString.append(h)
        }
        return hexString.toString()

    } catch (e: NoSuchAlgorithmException) {
        e.printStackTrace()
    }

    return ""
}

fun getCurrentTimeString(): String {
    val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.UK)
    return sdf.format(Date())
}

fun parseISODate(str: String): Date {
    val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSXXX", Locale.UK)
    return sdf.parse(str)
}

fun addToCart(context: Context, i: Item) {
    val preferences = context.getSharedPreferences("bob", Context.MODE_PRIVATE)
    val cart = context.getSharedPreferences("bob", Context.MODE_PRIVATE).getStringSet("cart", setOf()).toMutableSet()
    cart.add(i.toString())
    preferences.edit()
        .putStringSet("cart", cart)
        .commit()
}

fun getCart(context: Context) = context
    .getSharedPreferences("bob", Context.MODE_PRIVATE)
    .getStringSet("cart", setOf())
    .toList()
    .map { Item.fromString(it) }

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