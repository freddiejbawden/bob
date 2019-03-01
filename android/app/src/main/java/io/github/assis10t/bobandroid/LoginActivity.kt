package io.github.assis10t.bobandroid

import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.view.MenuItem
import io.github.assis10t.bobandroid.pojo.User
import kotlinx.android.synthetic.main.activity_login.*
import org.jetbrains.anko.toast

class LoginActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        supportActionBar?.setDisplayShowHomeEnabled(true)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setHomeButtonEnabled(true)

        login_button.setOnClickListener {
            ServerConnection().login(
                this,
                username.text.toString()
            ) { err, user ->
                if (err != null) {
                    toast("An error occured while logging in.")
                } else {
//                    val intent = Intent(this, WarehouseActivity::class.java)
//                    intent.putExtra("loggedIn", true)
//                    startActivity(intent)
//                    onBackPressed() //TODO: Replace with startActivityForResult logic.
                    finish()
                }
            }
        }

        register_button.setOnClickListener {
            ServerConnection().register(
                this,
                username.text.toString()
            ) { err, user ->
                if (err != null) {
                    toast("An error occured while registering.")
                } else {
//                    val intent = Intent(this, WarehouseActivity::class.java)
//                    intent.putExtra("loggedIn", true)
//                    startActivity(intent)
//                    onBackPressed() //TODO: Replace with startActivityForResult logic.
                    finish()
                }
            }
        }
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        if (item?.itemId == android.R.id.home) {
            finish()
            return true
        } else {
            return super.onOptionsItemSelected(item)
        }
    }
}
