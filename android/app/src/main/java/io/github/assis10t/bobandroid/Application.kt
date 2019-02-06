package io.github.assis10t.bobandroid

import android.app.Application
<<<<<<< HEAD
=======
import timber.log.Timber
>>>>>>> 1339882e609619cd14b45720a5a2a734b8a407d6

class Application: Application() {

    override fun onCreate() {
        super.onCreate()
        ServerConnection.initialize()
<<<<<<< HEAD
=======

        //From: https://github.com/oktay-sen/Coinz
        Timber.plant(object : Timber.DebugTree() {
            override fun createStackElementTag(element: StackTraceElement): String? {
                return super.createStackElementTag(element) + ':' + element.lineNumber
            }
        })
>>>>>>> 1339882e609619cd14b45720a5a2a734b8a407d6
    }
}