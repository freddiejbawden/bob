package io.github.assis10t.bobandroid

import android.content.Context
import android.util.TypedValue

fun dp(context: Context, dp: Float) =
    TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dp, context.resources.displayMetrics)