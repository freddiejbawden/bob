package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.view.MenuItem
import android.widget.Toast
import kotlinx.android.synthetic.main.dialog_login.*
import org.jetbrains.anko.toast

class LoginDialog(context: Context, private val onResult: ((loggedIn: Boolean) -> Unit)? = null) : Dialog(context) {

    private var shouldTriggerOnResult = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_login)

        setOnDismissListener {
            if (shouldTriggerOnResult)
                onResult?.invoke(ServerConnection().isLoggedIn(context))
        }

        login_button.setOnClickListener {
            ServerConnection().login(
                context,
                username.text.toString()
            ) { err, user ->
                if (err != null) {
                    Toast.makeText(context, err.message, Toast.LENGTH_LONG).show()
                } else {
                    dismiss()
                }
            }
        }

        register_button.setOnClickListener {
            RegisterDialog(context, onResult).show()
            shouldTriggerOnResult = false
            dismiss()
        }
    }
}
