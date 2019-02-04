package io.github.assis10t.bobandroid

import android.app.Application

class Application: Application() {

    override fun onCreate() {
        super.onCreate()
        ServerConnection.initialize()
    }
}