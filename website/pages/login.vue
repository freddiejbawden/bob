<template>
    <div>
        <page-title
            title="Login to your account"
        ></page-title>

        <section class="section">
            <div class="container is-flex justify-center">
                <div class="box third-width p30 pl50 pr50">
                    <form action="">
                        <div class="field">
                            <label class="label">Username:</label>
                            <div class="control">
                                <input 
                                    :class="[
                                        'input', 'is-' + message.status
                                    ]" 
                                    type="text" 
                                    placeholder="Enter your full name" 
                                    v-model="username">
                            </div>
                            <p :class="[
                                'help', 'is-' + message.status
                            ]">
                                {{ message.text }}
                            </p>
                        </div>
                        <div class="field">
                            <label class="label">Password:</label>
                            <div class="control">
                                <input class="input" type="password" v-model="password" placeholder="Enter your password">
                            </div>
                        </div>
                        <!-- <div class="field">
                            <label class="label">Confirm password:</label>
                            <div class="control">
                                <input class="input" type="password" v-model="password" placeholder="Confirm your password">
                            </div>
                        </div> -->
                        <div class="field">
                            <div class="control pt30">
                                <a 
                                    href="javascript:;"
                                    class="button is-link" 
                                    :disabled="!username || !password"
                                    @click.stop.prevent="login()">
                                    <span>Login</span>
                                </a>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import PageTitle from '~/components/PageTitle'
import axios from 'axios'

export default {
    components: {
        PageTitle
    },
    data: function () {
        return {
            email: null,
            username: null,
            password: null,
            type: 'merchant',
            message: {
                status: null,
                text: null
            }
        }
    },
    methods: {
        login () {
            if (this.username && this.password) {
                axios.
                    post('http://localhost:9000/api/login/', {
                        username: this.username,
                        password: this.password,
                        // type: this.type,
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                        }
                    })
                    .then((res) => {
                        this.$store.commit('setUser', res.data.user)
                        this.$cookies.set('user', res.data.user)
                        console.log("Server response: ", res);
    
                        if (res.status == 200) {
                            this.$router.push('/merchant/orders').go(1)
                        } else {
                            this.message.status = 'danger'
                            this.message.text = 'There is no such username in our database.'
                        }
                    })
                    .catch((error) => {
                        this.message.status = 'danger'
                        this.message.text = 'There is no such username in our database.'

                        console.error("Error adding document: ", error);
                    });
            }
        }
    }
};
</script>

<style lang="sass" scoped>


</style>
