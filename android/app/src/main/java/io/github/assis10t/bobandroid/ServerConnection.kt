package io.github.assis10t.bobandroid

import android.os.AsyncTask
import android.util.Log
import java.net.Inet4Address
import javax.jmdns.JmDNS
import javax.jmdns.ServiceEvent
import javax.jmdns.ServiceListener

class ServerConnection {

    companion object {
        private val TAG = "ServerConnection"
        val SERVER_NAME = "assis10t"
        var serverIp: String? = null

        val onConnectedListeners: MutableList<(String) -> Unit> = mutableListOf()

        class ConnectTask: AsyncTask<Unit, JmDNS, Unit>() {
            override fun doInBackground(vararg params: Unit?) {
                Log.d(TAG, "Discovery started")
                val mJmDNS = JmDNS.create()
                mJmDNS.addServiceListener("_http._tcp.local.", object : ServiceListener {
                    override fun serviceResolved(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Log.d(TAG, "Service resolved: $info")
                        if (info.name.contains(SERVER_NAME)) {
                            serverIp = "${info.inet4Addresses[0]!!.hostAddress}:${info.port}"
                            onConnectedListeners.forEach { it(serverIp!!) }
                            onConnectedListeners.clear()
                        }
                    }

                    override fun serviceRemoved(event: ServiceEvent?) {
                        Log.d(TAG, "Service removed")
                    }

                    override fun serviceAdded(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Log.d(TAG, "Service added: $info")
                    }
                })
            }
        }

        fun initialize() {
            ConnectTask().execute()
            ServerConnection().connect { ip ->
                Log.d(TAG, "Server found at $ip")
            }
        }
    }

    fun connect(onConnected: (String) -> Unit) {
        if (serverIp != null)
            onConnected(serverIp!!)
        else
            onConnectedListeners.add(onConnected)
    }
}