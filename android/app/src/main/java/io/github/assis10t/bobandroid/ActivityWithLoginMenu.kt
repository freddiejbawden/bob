package io.github.assis10t.bobandroid

import android.annotation.SuppressLint
import android.content.DialogInterface
import android.content.Intent
import android.os.Bundle
import android.os.PersistableBundle
import android.support.v7.app.AlertDialog
import android.support.v7.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import org.jetbrains.anko.toast
import timber.log.Timber

@SuppressLint("Registered")
open class ActivityWithLoginMenu: AppCompatActivity() {

    private val authListener = { isLoggedIn: Boolean ->
        Timber.d("Is logged in? $isLoggedIn")
        invalidateOptionsMenu()
    }

    override fun onStart() {
        super.onStart()
        ServerConnection().addAuthListener(authListener)
    }

    override fun onStop() {
        super.onStop()
        ServerConnection().removeAuthListener(authListener)
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        if (ServerConnection().isLoggedIn(this)) {
            menuInflater.inflate(R.menu.menu_logged_in, menu)
        } else {
            menuInflater.inflate(R.menu.menu_logged_out, menu)
        }
        return true
    }

    override fun onResume() {
        super.onResume()
        invalidateOptionsMenu()
    }

    override fun onPrepareOptionsMenu(menu: Menu?): Boolean {
        val welcome = menu?.findItem(R.id.welcome_text)
        if (welcome != null) {
            val username = ServerConnection().getCurrentUsername(this)
            welcome.title = "Welcome, $username!"
        }
        val orders = menu?.findItem(R.id.orders)
        if (orders != null) {
            orders.isEnabled = this !is OrdersActivity
        }
        return super.onPrepareOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        // Handle item selection
        return when (item?.itemId) {
            R.id.login -> {
                LoginDialog(this) { invalidateOptionsMenu() }.show()
                true
            }
            R.id.logout -> {
                ServerConnection().logout(this) {err ->
                    invalidateOptionsMenu()
                    if (err != null) {
                        Toast.makeText(this, err.message, Toast.LENGTH_SHORT).show()
                        return@logout
                    }
                    Toast.makeText(this, "Logged out successfully.", Toast.LENGTH_SHORT).show()
                }
                true
            }
            R.id.orders -> {
                startActivity(Intent(this, OrdersActivity::class.java))
                true
            }
            R.id.deleteMyData -> {
                AlertDialog.Builder(this)
                    .setTitle("Confirm Data Deletion")
                    .setMessage("Are you sure you want to delete ALL of your data? This action cannot be undone.")
                    .setPositiveButton("Delete") { dialogInterface, whichButton ->
                        ServerConnection().deleteMyData(this) { error ->
                            Timber.d(error, "DeleteMyData result")
                            if (error != null) {
                                toast("A problem occured while deleting your data.")
                                return@deleteMyData
                            }
                            toast("Your data has been deleted. Thank you for using Bob!")
                            if (this !is WarehouseListActivity) {
                                startActivity(Intent(this, WarehouseListActivity::class.java))
                                finish()
                            }
                        }
                    }
                    .setNegativeButton("Cancel", null)
                    .show()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}