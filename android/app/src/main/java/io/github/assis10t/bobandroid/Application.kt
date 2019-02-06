package io.github.assis10t.bobandroid

import android.app.Application
import timber.log.Timber

class Application: Application() {

    override fun onCreate() {
        super.onCreate()
        ServerConnection.initialize()

        //From: https://github.com/oktay-sen/Coinz
        Timber.plant(object : Timber.DebugTree() {
            override fun createStackElementTag(element: StackTraceElement): String? {
                return super.createStackElementTag(element) + ':' + element.lineNumber
            }
        })
    }
}