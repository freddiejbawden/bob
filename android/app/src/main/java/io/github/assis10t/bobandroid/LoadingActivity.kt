package io.github.assis10t.bobandroid

import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.support.v7.app.AlertDialog
import android.text.InputType
import android.view.Menu
import android.view.MenuItem
import android.widget.EditText

class LoadingActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_loading)

        supportActionBar?.elevation = 0f

        ServerConnection().connect {
            val intent = Intent(this, WarehouseListActivity::class.java)
            startActivity(intent)
            finish()
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_loading, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle item selection
        return when (item.itemId) {
            R.id.zeroconf_bypass -> {
                val builder = AlertDialog.Builder(this)
                builder.setTitle("What's the address of the server?")
                val input = EditText(this)
                input.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_URI or InputType.TYPE_TEXT_FLAG_AUTO_COMPLETE
                input.text.insert(0, "192.168.")
                builder.setView(input)
                builder.setPositiveButton("Set") { dialog, which ->
                    ServerConnection.zeroconfBypass("http://${input.text}:9000")
                }
                builder.setNegativeButton("Cancel") { dialog, which ->
                    dialog.cancel()
                }
                builder.show()
                true
            }
            R.id.cloud -> {
                //TODO: Implement build-time config instead.
                ServerConnection.zeroconfBypass("https://sdp-10-beta.herokuapp.com")
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}
