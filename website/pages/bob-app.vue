<template>
    <div>

        <page-title
            title="Download the Bob App"
            desc="The Bob App helps you shop easier. It gives customers the ability to browse items and place orders."
        ></page-title>

        <section class="section">
            <div class="container">
                <div class="box">
                    <div class="columns">
                        <div class="column is-6 is-flex align-center justify-center">
                            <img src="~/assets/images/bob-app-icon.png">
                        </div>
                        <div class="column is-6 is-flex direction-column align-center p40-0">
                            <p class="has-text-centered mb20">
                                You can download the beta version (v2.2) of the app using the link below. It currently works only for Android OS.
                            </p>
                            <a href="https://github.com/Assis10t/assis10t/releases/download/v2.2/app-debug.apk" class="button is-primary" target="_blank">
                                <span>Download .apk</span>
                            </a>
                        </div>
                    </div>
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
            
        }
    },
    methods: {

    }
};
</script>

<style lang="sass" scoped>

</style>
