<template>
  <section class="section p0">
    <div class="container">
      <div class="box p0 oh m10">

        <GmapMap
            :center="{ lat: 42.017322, lng: 23.095913}"
            :zoom="16"
        >
            <GmapMarker
                :position="{ lat: 42.017322, lng: 23.095913}"
            />
        </GmapMap>

        <!-- <mapbox
          access-token="pk.eyJ1IjoiaHlhcHJha292IiwiYSI6ImNqcThjeGVoYzJ6emQ0OHIxdzFoN2c4N3MifQ.pm2dqcPXQmlvgMFmaUQAyQ"
          :map-options="{
                        style: 'mapbox://styles/mapbox/light-v9',
                        center: [23.095913, 42.017322],
                        zoom: 16
                    }"
          :geolocate-control="{
                        show: true,
                        position: 'top-left'
                    }"
          :scale-control="{
                        show: true,
                        position: 'top-left'
                    }"
          :fullscreen-control="{
                        show: true,
                        position: 'top-left'
                    }"
            @map-load="mapLoaded"
        ></mapbox>-->
      </div>
    </div>
  </section>
</template>

<script>

import * as VueGoogleMaps from 'vue2-google-maps'

Vue.use(VueGoogleMaps, {
    load: {
        key: 'AIzaSyCeUVNN4kP1WMKXswKrPUSdqDNrN7CY-6Y',
    }
})

export default {
    props: ["title", "desc"],
    // components: {
    //     MglMap
    // },

    data: function() {
        return {
            
        };
    },
    methods: {
        
    },
    computed: {

    }
};
</script>
