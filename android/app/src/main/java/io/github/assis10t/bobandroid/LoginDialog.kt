package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.view.MenuItem
import android.widget.Toast
import kotlinx.android.synthetic.main.dialog_login.*
import org.jetbrains.anko.toast

class LoginDialog(context: Context, val onResult: ((loggedIn: Boolean) -> Unit)? = null) : Dialog(context) {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_login)

        setOnDismissListener {
            onResult?.invoke(ServerConnection().isLoggedIn(context))
        }

        login_button.setOnClickListener {
            ServerConnection().login(
                context,
                username.text.toString()
            ) { err, user ->
                if (err != null) {
                    Toast.makeText(context, "An error occured while logging in.", Toast.LENGTH_LONG).show()
                } else {
                    dismiss()
                }
            }
        }

        register_button.setOnClickListener {
            ServerConnection().register(
                context,
                username.text.toString()
            ) { err, user ->
                if (err != null) {
                    Toast.makeText(context, "An error occured while registering.", Toast.LENGTH_LONG).show()
                } else {
                    dismiss()
                }
            }
        }
    }
}
