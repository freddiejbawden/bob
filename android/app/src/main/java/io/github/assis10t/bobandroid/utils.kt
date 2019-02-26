package io.github.assis10t.bobandroid

import android.content.Context
import android.content.SharedPreferences
import android.util.TypedValue
import android.provider.SyncStateContract.Helpers.update
import io.github.assis10t.bobandroid.pojo.Item
import timber.log.Timber
import java.security.NoSuchAlgorithmException
import java.text.SimpleDateFormat
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
    val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssZ", Locale.UK)
    return sdf.format(Date())
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