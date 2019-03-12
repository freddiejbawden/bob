package io.github.assis10t.bobandroid

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.LocationManager
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.support.design.widget.BottomSheetBehavior
import android.support.v4.app.ActivityCompat
import android.support.v7.app.AlertDialog
import android.support.v7.widget.CardView
import android.support.v7.widget.LinearLayoutManager
import android.support.v7.widget.RecyclerView
import android.view.*
import android.widget.TextView
import android.widget.Toast

import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.MarkerOptions
import io.github.assis10t.bobandroid.pojo.Warehouse
import kotlinx.android.synthetic.main.activity_warehouse_list.*

// Location permission logic from https://github.com/oktay-sen/Coinz
class WarehouseListActivity : ActivityWithLoginMenu(), OnMapReadyCallback {

    private lateinit var mMap: GoogleMap

    private val PERMISSION_REQUEST = 3749
    private val LOCATION_PERMISSIONS = arrayOf(
        Manifest.permission.ACCESS_COARSE_LOCATION,
        Manifest.permission.ACCESS_FINE_LOCATION
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_warehouse_list)

        supportActionBar?.title = "Shops near you"

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)

        if (!hasLocationPermissions())
            requestLocationPermissions()

        val behavior = BottomSheetBehavior.from(warehouse_list_container)
        behavior.isHideable = false
        behavior.state = BottomSheetBehavior.STATE_COLLAPSED
        behavior.peekHeight = dp(this, 128f).toInt()
        behavior.skipCollapsed = false

        warehouse_list.layoutManager = LinearLayoutManager(this, LinearLayoutManager.VERTICAL, false)
//        warehouse_list.adapter = WarehouseAdapter(listOf(
//            Warehouse("some_id","My Warehouse") //TODO: Remove this.
//        ))
        warehouse_list.adapter = WarehouseAdapter(listOf())
        loading.visibility = View.GONE
    }

    override fun onResume() {
        super.onResume()
        refreshWarehouseList()
    }

    fun refreshWarehouseList() {
        loading.visibility = View.VISIBLE
        warehouse_list.visibility = View.INVISIBLE
        ServerConnection().getWarehouses {err, warehouses ->
            loading.visibility = View.GONE
            warehouse_list.visibility = View.VISIBLE
            if (err != null) {
                Toast.makeText(this, err.message, Toast.LENGTH_SHORT).show()
                return@getWarehouses
            }
            val adapter = warehouse_list.adapter as WarehouseAdapter
            adapter.setItems(warehouses!!)

            mMap.clear()
            warehouses.forEach { warehouse ->
                mMap.addMarker(
                    MarkerOptions()
                        .position(warehouse.location!!.asLatLng())
                        .title(warehouse.name)
                )
            }
        }
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap

        if (hasLocationPermissions()) {
            enableCurrentLocation()
        }

        // Add a marker in Sydney and move the camera
//        val sydney = LatLng(-34.0, 151.0)
//        mMap.addMarker(MarkerOptions().position(sydney).title("Marker in Sydney"))
//        mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney))
    }

    @SuppressLint("MissingPermission")
    fun enableCurrentLocation() {
        mMap.isMyLocationEnabled = true
        val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        val location = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
        val latLng = LatLng(location.latitude, location.longitude)
        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(latLng, 16f))
    }

    private fun hasLocationPermissions():Boolean =
        LOCATION_PERMISSIONS.fold(true) { acc, perm ->
            acc && checkSelfPermission(perm) == PackageManager.PERMISSION_GRANTED }

    private fun requestLocationPermissions() {
        if (LOCATION_PERMISSIONS.fold(false) { acc, perm ->
                acc || ActivityCompat.shouldShowRequestPermissionRationale(this, perm) }) {
            AlertDialog.Builder(this)
                .setTitle("Location Permissions")
                .setMessage("To find stores around you, please accept the location permissions")
                .setPositiveButton("OK") { _, _ ->
                    requestPermissions(LOCATION_PERMISSIONS, PERMISSION_REQUEST)
                }
                .create()
                .show()
        } else {
            requestPermissions(LOCATION_PERMISSIONS, PERMISSION_REQUEST)
        }
    }

    @SuppressLint("MissingPermission")
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        if (requestCode == PERMISSION_REQUEST) {
            if (hasLocationPermissions()) {
                enableCurrentLocation()
            } else {
                Toast.makeText(this, "You can later grant location permissions in the settings.", Toast.LENGTH_SHORT).show()
            }
        } else {
            super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        }
    }

    class WarehouseAdapter(private var warehouseList: List<Warehouse> = listOf()) : RecyclerView.Adapter<WarehouseAdapter.ViewHolder>() {

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val inflater = LayoutInflater.from(parent.context)
            return ViewHolder(inflater.inflate(R.layout.fragment_warehouse_list_item, parent, false))
        }

        override fun getItemCount() = warehouseList.size

        override fun onBindViewHolder(vh: ViewHolder, pos: Int) {
            vh.title.text = warehouseList[pos].name
            vh.description.text = "Supermarket"
            vh.container.setOnClickListener {v ->
                val intent = Intent(v.context, WarehouseActivity::class.java)
                intent.putExtra("warehouseId", warehouseList[pos]._id)
                intent.putExtra("warehouseName", warehouseList[pos].name)
                v.context.startActivity(intent)
            }
        }

        fun setItems(warehouseList: List<Warehouse>) {
            this.warehouseList = warehouseList
            notifyDataSetChanged()
        }

        fun getItems() = warehouseList

        class ViewHolder(v: View): RecyclerView.ViewHolder(v) {
            val container: CardView = v.findViewById(R.id.container)
            val title: TextView = v.findViewById(R.id.title)
            val description: TextView = v.findViewById(R.id.description)
        }
    }
}
