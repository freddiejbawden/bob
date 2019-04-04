<template>
    <section class="section curved-section">
        <svg viewBox="0 0 1330 425">
            <defs>
                <path id="clip_path_curve" d="M5.01303218,3.50068867e-13 L1326,-7.01660952e-13 C1328.76142,-7.02168217e-13 1331,2.23857625 1331,5 L1331,384.165033 C1057.94603,404.721678 836.261132,415 665.945312,415 C495.629492,415 273.981055,404.721678 1,384.165033 L0.0130491189,5.0130152 C0.00586102485,2.2516008 2.23860259,0.00720503363 5.00001698,1.69395608e-05 C5.00435537,5.64652527e-06 5.00869378,3.34844061e-13 5.01303218,3.34843264e-13 Z"></path>
            </defs>
            <clipPath id="clip_curve">
                <use xlink:href="#clip_path_curve"  style="overflow:visible;"/>
            </clipPath>
            <g style="clip-path:url(#clip_curve);">
                <!-- <rect x="0" y="0" width="100%" height="100%" fill="none"
                    :style="{'background-image': 'url(' + section_bckg + ')'}"></rect> -->
                <image 
                    width="100%" 
                    height="225%"
                    x="0"
                    y="-60%"
                    xlink:href="~/assets/images/team.jpg"></image>
                <rect x="0" y="0" width="100%" height="100%" fill="#000000" fill-opacity="0.6"></rect>
            </g>
        </svg>

        <div class="curved-content">
            <h2>{{ section_title }}</h2>
            <p>
                {{ section_text }}
            </p>
            <nuxt-link :to="section_button.url" class="button is-primary">
                <span>{{ section_button.name }}</span>
            </nuxt-link>
        </div>

        <div class="img-bckg" :style="{'background-image': 'url(' + section_bckg + ')'}">
            <!-- <img :src="section_bckg" alt=""> -->
        </div>
    </section>
</template>

<script>

export default {
    props: ['section_title', 'section_bckg', 'section_text', 'section_button'],

    data: function () {
        return {
            
        }
    },
    methods: {
        
    },
    computed: {
        
    },
    mounted: function () {
        
    }
}
</script>
