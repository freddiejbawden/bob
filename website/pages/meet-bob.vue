<template>
    <div>

        <page-title
            title="Meet the <span>Bob</span>"
            desc="The robot is powered by a Lego Mindstorms EV3 and a Raspberry Pi. This allows the robot to listen for new instructions and perform complex tasks such as lifting, grabbing and tracking its position."
        ></page-title>


<section class="section">
    <!-- <div class="container"> -->
        <div class="columns m0t">
            <div class="column is-6 direction-column justify-center p80 p15t">
                <h2 class="mb30">
                    Bob's <span class="has-text-primary">Construction</span>
                </h2>
                <h4 class="has-text-primary mt20">
                    Omnidirectional Base
                </h4>
                <p>
                    The core part of the Bob system is Bob himself. Bob was constructed with an omnidirectional wheel base, this allows for optimal movement through a grid like warehouse.
                </p>
                <h4 class="has-text-primary mt20">
                    Scissor Lift
                </h4>
                <p>
                    In order to reach different shelves we tested a number of lift mechanisms, the one we settled for was a scissor lift due to its compact nature, as well as the resources we had available.
                </p>
                <h4 class="has-text-primary mt20">
                    Sweep Grabber
                </h4>
                <p>
                    The final key part of Bob is the grabber, the central rail can be driven to collect items, and then a sweep on the end pulls items in too his storage.
                </p>
            </div>
            <div class="column is-6">
                <div class="is-full-width is-full-height">
                    <img class="box p0" src="~/assets/images/bob-photo1.jpg" alt="Bob the robot">
                </div>
            </div>
        </div>
    <!-- </div> -->
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
