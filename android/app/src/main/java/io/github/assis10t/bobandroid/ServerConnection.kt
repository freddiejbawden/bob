package io.github.assis10t.bobandroid

import android.annotation.SuppressLint
import android.content.Context
import com.google.gson.Gson
import io.github.assis10t.bobandroid.pojo.*
import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.uiThread
import timber.log.Timber
import java.io.IOException
import javax.jmdns.JmDNS
import javax.jmdns.ServiceEvent
import javax.jmdns.ServiceListener

// Using API level v3

class ServerConnection {
    companion object {
        val SERVER_NAME = "assis10t"
        var serverAddress: String? = null
        val httpClient: OkHttpClient = OkHttpClient()

        val onConnectedListeners: MutableList<(serverAddress: String) -> Unit> = mutableListOf()

        fun initialize() {
            doAsync {
                Timber.d("Discovery started")
                val mJmDNS = JmDNS.create()
                mJmDNS.addServiceListener("_http._tcp.local.", object : ServiceListener {

                    override fun serviceResolved(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Timber.d("Service resolved: $info")
                        if (info.name.contains(SERVER_NAME)) {
                            uiThread {
                                serverAddress = "http://${info.inet4Addresses[0]!!.hostAddress}:${info.port}"
                                onConnectedListeners.forEach { it(serverAddress!!) }
                                onConnectedListeners.clear()
                            }
                        }
                    }

                    override fun serviceRemoved(event: ServiceEvent?) {
                        Timber.d("Service removed")
                    }

                    override fun serviceAdded(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Timber.d("Service added: $info")
                    }
                })
            }
            ServerConnection().connect { ip ->
                Timber.d("Server found at $ip")
            }
        }

        fun zeroconfBypass(address: String) {
            Timber.d("Bypassed zeroconf: $address")
            serverAddress = "http://$address:9000"
            onConnectedListeners.forEach { it(serverAddress!!) }
            onConnectedListeners.clear()
        }
    }

    fun connect(onConnected: (String) -> Unit) {
        if (serverAddress != null)
            onConnected(serverAddress!!)
        else
            onConnectedListeners.add(onConnected)
    }

    val getRequestWithAuthFactory = { http: OkHttpClient, gson: Gson ->
        { url: String, username: String, onGetComplete: (error: Exception?, response: String?) -> Unit ->
            doAsync {
                Timber.d("Get request to $url")
                try {
                    val request = Request.Builder().url(url).header("username",username).build()
                    val response = http.newCall(request).execute()
                    Timber.d("Response received.")
                    val responseBody = response.body()?.string()!!
                    val failResponse = gson.fromJson(responseBody, FailResponse::class.java)
                    if (!failResponse.success) {
                        uiThread { onGetComplete(Exception(failResponse.error), responseBody) }
                    } else {
                        uiThread { onGetComplete(null, responseBody) }
                    }
                } catch (e: IOException) {
                    Timber.e(e, "Get Request failed")
                    uiThread { onGetComplete(e, null) }
                }
            }
        }
    }
    val getRequestFactory = { http: OkHttpClient, gson: Gson ->
        { url: String, onGetComplete: (error: Exception?, response: String?) -> Unit ->
            getRequestWithAuthFactory(http, gson)(url, "", onGetComplete)
        }
    }

    val postRequestWithAuthFactory = { http: OkHttpClient, gson: Gson ->
        { url: String, username: String, body: Any, onPostComplete: (error: Exception?, response: String?) -> Unit ->
            doAsync {
                Timber.d("Post request to $url")
                try {
                    val JSON = MediaType.get("application/json; charset=utf-8")
                    val requestBody = RequestBody.create(JSON, gson.toJson(body))
                    val request = Request.Builder().header("username",username).url(url).post(requestBody).build()
                    val response = http.newCall(request).execute()
                    val responseBody = response.body()?.string()!!
                    Timber.d("Response received.")
                    val failResponse = gson.fromJson(responseBody, FailResponse::class.java)
                    if (!failResponse.success) {
                        uiThread { onPostComplete(Exception(failResponse.error), responseBody) }
                    } else {
                        uiThread { onPostComplete(null, responseBody) }
                    }
                } catch (e: IOException) {
                    Timber.e(e, "Post Request failed")
                    uiThread { onPostComplete(e, null) }
                }
            }
        }
    }

    val postRequestFactory = { http: OkHttpClient, gson: Gson ->
        { url: String, body: Any, onPostComplete: (error: Exception?, response: String?) -> Unit ->
            postRequestWithAuthFactory(http, gson)(url, "", body, onPostComplete)
        }
    }

    val getWarehousesFactory = { http: OkHttpClient, gson: Gson ->
        { onGetWarehouses: (error: Exception?, warehouses: List<Warehouse>?) -> Unit ->
            connect { server ->
                getRequestFactory(http, gson)("$server/api/warehouse") { error, str ->
                    if (error != null) {
                        onGetWarehouses(error, null)
                    } else {
                        val response = gson.fromJson(str!!, GetWarehousesResponse::class.java)
                        onGetWarehouses(null, response.warehouses)
                    }
                }
            }
        }
    }
    val getWarehouses = getWarehousesFactory(httpClient, Gson())

    val getWarehouseFactory = { http: OkHttpClient, gson: Gson ->
        { warehouseId: String, onGetWarehouse: (error: Exception?, warehouse: Warehouse?) -> Unit ->
            connect { server ->
                getRequestFactory(http, gson)("$server/api/warehouse/$warehouseId") { error, str ->
                    if (error != null) {
                        onGetWarehouse(error, null)
                    } else {
                        val response = gson.fromJson(str!!, GetWarehouseResponse::class.java)
                        onGetWarehouse(null, response.warehouse)
                    }
                }
            }
        }
    }
    val getWarehouse = getWarehouseFactory(httpClient, Gson())

    //Requires login
    val getOrdersFactory = { http: OkHttpClient, gson: Gson ->
        { context: Context, onGetOrders: (error: Exception?, orders: List<Order>?) -> Unit ->
            connect {server ->
                if (!isLoggedIn(context)) {
                    onGetOrders(Exception("This operation requires authentication."), null)
                    return@connect
                }
                getRequestWithAuthFactory(http, gson)("$server/api/order", getCurrentUsername(context)!!) { error, str ->
                    if (error != null) {
                        onGetOrders(error, null)
                    } else {
                        val response = gson.fromJson(str, GetOrdersResponse::class.java)
                        onGetOrders(null, response.orders)
                    }
                }
            }
        }
    }
    val getOrders = getOrdersFactory(httpClient, Gson())

    // Requires login
    val makeOrderFactory = { http: OkHttpClient, gson: Gson ->
        { context: Context, order: Order, onOrderComplete: ((error: Exception?) -> Unit)? ->
            connect { server ->
                if (!isLoggedIn(context)) {
                    onOrderComplete?.invoke(Exception("This operation requires authentication."))
                    return@connect
                }
                postRequestWithAuthFactory(http, gson)("$server/api/order", getCurrentUsername(context)!!, order) { error, str ->
                    onOrderComplete?.invoke(error)
                }
            }
        }
    }
    val makeOrder = makeOrderFactory(httpClient, Gson())

    val isLoggedIn = { context: Context -> getCurrentUsername(context) != null }

    val getCurrentUsername = { context: Context ->
        context.getSharedPreferences("bob", Context.MODE_PRIVATE).getString("username", null)
    }

    private val setCurrentUsername = { context: Context, username: String? ->
        if (username == null) {
            context
                .getSharedPreferences("bob", Context.MODE_PRIVATE)
                .edit()
                .remove("username")
                .apply()
        } else {
            context
                .getSharedPreferences("bob", Context.MODE_PRIVATE)
                .edit()
                .putString("username", username)
                .apply()
        }
    }

    val loginFactory = { http: OkHttpClient, gson: Gson ->
        { context: Context, username: String, onLoginComplete: ((error: Exception?, user: User?) -> Unit)? ->
            connect { server ->
                postRequestFactory(http, gson)("$server/api/login", LoginRequest(username)) { error, str ->
                    if (error != null) {
                        onLoginComplete?.invoke(error, null)
                    } else {
                        val response = gson.fromJson(str!!, LoginResponse::class.java)
                        setCurrentUsername(context, response.user!!.username)
                        onLoginComplete?.invoke(null, response.user)
                    }
                }
            }
        }
    }
    val login = loginFactory(httpClient, Gson())

    val logout = { context: Context, onLogoutComplete: ((error: Exception?) -> Unit)? ->
        setCurrentUsername(context, null)
        onLogoutComplete?.invoke(null)
    }

    val registerFactory = { http: OkHttpClient, gson: Gson ->
        { context: Context, username: String, onRegisterComplete: ((error: Exception?, user: User?) -> Unit)? ->
            connect { server ->
                postRequestFactory(http, gson)("$server/api/register", RegisterRequest(username)) { error, str ->
                    if (error != null) {
                        onRegisterComplete?.invoke(error, null)
                    } else {
                        val response = gson.fromJson(str!!, LoginResponse::class.java)
                        setCurrentUsername(context, response.user!!.username)
                        onRegisterComplete?.invoke(null, response.user)
                    }
                }
            }
        }
    }
    val register = registerFactory(httpClient, Gson())
}