package io.github.assis10t.bobandroid

import android.app.Dialog
import android.content.Context
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.MenuItem
import android.widget.Toast
import kotlinx.android.synthetic.main.dialog_register.*
import org.jetbrains.anko.toast

class RegisterDialog(context: Context, val onResult: ((loggedIn: Boolean) -> Unit)? = null) : Dialog(context) {

    private var shouldTriggerOnResult = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.dialog_register)

        setOnDismissListener {
            if (shouldTriggerOnResult)
                onResult?.invoke(ServerConnection().isLoggedIn(context))
        }

        username.addTextChangedListener(object: TextWatcher {
            override fun afterTextChanged(s: Editable?) {
                username.error = null
            }
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
        })

        password.addTextChangedListener(object: TextWatcher {
            override fun afterTextChanged(s: Editable?) {
                username.error = null
            }
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
        })

        register_button.setOnClickListener {
            if (!runInputValidation()) {
                return@setOnClickListener
            }

            ServerConnection().register(
                context,
                username.text.toString().trim()
            ) { err, user ->
                if (err != null) {
                    Toast.makeText(context, err.message, Toast.LENGTH_LONG).show()
                } else {
                    dismiss()
                }
            }
        }

        login_button.setOnClickListener {
            LoginDialog(context, onResult).show()
            shouldTriggerOnResult = false
            dismiss()
        }
    }

    private fun runInputValidation(): Boolean {
        var inputValid = true

        if (!username.text.trim().matches(Regex("[a-zA-z0-9_-]+"))) {
            username.error = "Username can only contain alphanumeric characters"
            inputValid = false
        }

        if (username.text.trim().length < 3) {
            username.error = "Username should be at least 3 characters"
            inputValid = false
        }

        if (username.text.trim().length >= 50) {
            username.error = "Username should be shorter than 50 characters"
            inputValid = false
        }

        if (password.text.length < 8) {
            password.error = "Password should be at least 8 characters"
            inputValid = false
        }

        if (password.text.length >= 50) {
            password.error = "Password should be shorter than 50 characters"
            inputValid = false
        }

        return inputValid
    }
}
