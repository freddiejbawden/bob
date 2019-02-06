package io.github.assis10t.bobandroid

import android.content.Context
import android.util.TypedValue
import android.provider.SyncStateContract.Helpers.update
import java.security.NoSuchAlgorithmException


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