package io.github.assis10t.bobandroid

import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.view.MenuItem
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
                username.text.toString(),
                md5(password.text.toString())
            ) { success, loggedIn ->
                if (!success) {
                    toast("An error occured while logging in.")
                } else if (!loggedIn) {
                    toast("Wrong username or password.")
                } else {
                    val intent = Intent(this, MainActivity::class.java)
                    intent.putExtra("loggedIn", true)
                    startActivity(intent)
                }
            }
        }

        register_button.setOnClickListener {
            ServerConnection().register(
                username.text.toString(),
                md5(password.text.toString())
            ) { success ->
                if (!success) {
                    toast("An error occured while registering.")
                } else {
                    val intent = Intent(this, MainActivity::class.java)
                    intent.putExtra("loggedIn", true)
                    startActivity(intent)
                }
            }
        }
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        if (item?.itemId == android.R.id.home) {
            onBackPressed()
            return true
        } else {
            return super.onOptionsItemSelected(item)
        }
    }
}
