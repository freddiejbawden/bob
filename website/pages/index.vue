<template>
    <div>

        <hero 
            :slides="[
                {
                    title: 'Meet the <span>Bob</span>',
                    img: '~/assets/images/bob-hero.jpg',
                    short_description: 'Introducing Bob, the automated shopping robot that will revolutionise the grocery shopping experience.',
                    path: '/meet-bob'
                }
            ]"
            :is_carousel="false"
            :has_icon="true"
        ></hero> 

        <section class="section p0">
            <!-- <div class="container"> -->
                <div class="columns m0t">
                    <div class="column is-6 direction-column justify-center p80 p15t">
                        <h6>
                            At Bob, our mission is
                        </h6>
                        <h1 class="has-text-primary mt5 mb30">
                            "To make shopping as convenient as possible for everyone"
                        </h1>
                        <h6 class="mb10">
                            What Bob can do for you:
                        </h6>
                        <h6 class="p5-0">
                            <b>-</b> receive orders for goods from your customers,
                        </h6>
                        <h6 class="p5-0">
                            <b>-</b> automatically collect them within the shop,
                        </h6>
                        <h6 class="p5-0">
                            <b>-</b> get them ready for collection by the customer.
                        </h6>
                        <h6 class="mt10">
                            All of this while also giving you full control of how you run your retail business.
                        </h6>
                    </div>
                    <div class="column is-6">
                        <div class="is-full-width is-full-height">
                            <img src="~/assets/images/bob-photo2.jpg" alt="Bob">
                        </div>
                    </div>
                </div>
            <!-- </div> -->
        </section>

        <page-title
            title="The way Bob works is surprisingly simple"
            desc="Everything from the robot itself to your customers’ orders are handled by our cloud-hosted server. Changes made to your shop will be automatically updated across the website, app and robot."
        ></page-title>

        <section class="section pb80">
            <div class="container">
                <div class="columns">
                    <div class="column is-4 has-text-centered pr50 pl50">
                        <h4>
                            The <span class="has-text-primary">Robot</span>
                        </h4>
                        <p>
                            The robot listens for instructions and perform complex tasks such as lifting, grabbing and tracking its position.
                        </p>
                    </div>
                    <div class="column is-4 has-text-centered pr50 pl50">
                        <h4>
                            The <span class="has-text-primary">App</span>
                        </h4>
                        <p>
                            Using the app, customers can browse the shop’s inventory, order items and get updates about their orders.
                        </p>
                    </div>
                    <div class="column is-4 has-text-centered pr50 pl50">
                        <h4>
                            The <span class="has-text-primary">Website</span>
                        </h4>
                        <p>
                            Through the website, you can manage your shop - add stock, change the layout, monitor your robot’s status, view and complete orders.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <curved-section
            section_title="About us"
            section_bckg="~/assets/images/team.jpg"
            section_text="We are young professionals with a wide variety of skills in different fields. Our dedication is what brought Bob to life and the fuel to keep him going."
            :section_button="{
                name: 'Meet the Team',
                url: '/about'
            }"
        ></curved-section>

        <section class="section">
            <div class="container">
                <div class="box">
                    <div class="columns">
                        <div class="column is-6 is-flex align-center justify-center">
                            <img src="~/assets/images/bob-app-icon.png">
                        </div>
                        <div class="column is-6 is-flex direction-column align-center p40-0">
                            <h4>Download the <span class="has-text-primary mb20">Bob App</span></h4>
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
import Hero from '~/components/Hero'
import PageTitle from '~/components/PageTitle'
import CurvedSection from '~/components/CurvedSection'

export default {
    components: {
        Hero,
        PageTitle,
        CurvedSection,
    },
    data: function () {
        return {

        }
    },
    computed: {
        user: function () {
            return this.$store.state.user
        }
    },
    mounted: function () {
        console.log('TEST is', process.env.baseUrl)
    }
};
</script>

<style lang="sass">
</style>
