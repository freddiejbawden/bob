<template>
    <section class="section partners-carousel element-loader loading">
        <div class="container">
            <h2 class="has-text-centered mb30">{{ section_title }}</h2>

            <carousel
                :per-page="per_page"
                :scroll-per-page="false"
                :navigation-enabled="false"
                :pagination-enabled="false"
                :autoplay="true"
                :loop="true"
                :min-swipe-distance="300">
                
                <slide v-for="(partner, i) in partners" :key="'slide' + i" v-if="partners.length > 0">
                    <a :href="partner.info.link" :title="partner.name" class="partner-slide" target="_blank">
                        <img :src="partner.imagesFolder+partner.info.logo" :alt="partner.name">
                    </a>
                </slide>
            </carousel>
        </div>
    </section>
</template>

<script>

import VueCarousel from 'vue-carousel'

Vue.use(VueCarousel)

export default {
    props: ['section_title', 'slides'],

    data: function () {
        return {
            partners: [],
            per_page: 4
        }
    },
    methods: {
        
    },
    computed: {
        
    },
    mounted: function () {
        this.partners = this.slides ? this.slides : []
        
        if (window.matchMedia("(max-width: 480px)").matches) {
            this.per_page = 2
        }
    }
}
</script>
