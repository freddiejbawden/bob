<template>
    <section class="section curved-section pt70 pt20t element-loader loading">
        <h2 class="has-text-centered mb30" v-if="section_title">
            {{ section_title }}
        </h2>
        <div class="container is-relative">
            <svg viewBox="0 0 1032 315">
                <defs>
                    <path d="
                        M 57, 64 L 1069, 64 C 1072, 64 1074, 66 1074,69 L 1074, 338 C 903, 350 733, 369 563, 369 C 393, 369 222, 359 52, 338 L 52, 69 C 52, 66 54, 64 57,64 Z" id="ref_curve"></path>
                    <filter x="-0.8%" y="-2.3%" width="101.6%" height="105.2%" filterUnits="objectBoundingBox" id="shadow">
                        <feMorphology radius="0.5" operator="dilate" in="SourceAlpha" result="shadowSpreadOuter1"></feMorphology>
                        <feOffset dx="0" dy="1" in="shadowSpreadOuter1" result="shadowOffsetOuter1"></feOffset>
                        <feGaussianBlur stdDeviation="3" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>
                        <feColorMatrix 
                            values="
                                0 0 0 0 0.3   
                                0 0 0 0 0.3   
                                0 0 0 0 0.3  
                                0 0 0 0.3 0" 
                            type="matrix" in="shadowBlurOuter1"></feColorMatrix>
                    </filter>
                </defs>
                <clipPath id="clip_ref_curve">
                    <use xlink:href="#ref_curve"  style="overflow:visible;"/>
                </clipPath>
                <g transform="translate(-149.000000, -2619.000000)">
                    <g transform="translate(102.000000, 2559.000000)">
                        <use fill="black" fill-opacity="1" filter="url(#shadow)" xlink:href="#ref_curve"></use>
                        <use fill="#FFFFFF" xlink:href="#ref_curve"></use>
                    </g>
                </g>
            </svg>
            <div class="curved-content has-text-dark has-nostyle align-center b50">
                <div class="columns flex-wrap is-full-width ml30 mr30" v-if="list">
                    <div class="column is-3" v-for="info in list">
                        <p class="mt0 mb5">{{ info.title }}</p>
                        <h6 :class="{'has-info-tooltip': info.additional, 'lh1-1': true}">
                            {{ info.desc }}

                            <div class="info-tooltip" v-if="info.additional">
                                <div class="box">
                                    <h6 class="has-text-centered mb30">{{ info.additional.title }}</h6>

                                    <div class="columns flex-wrap mb10">
                                        <div class="column is-6 p0" v-for="entry in info.additional.texts">
                                            <p class="mt0 mb5">
                                                {{ entry.text }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </h6>
                    </div>
                </div>
                <div>
                    <h2 class="has-text-centered mb30" v-if="box_title">
                        {{ box_title }}
                    </h2>
                    <p v-if="desc" class="p0-50 has-text-centered">
                        {{ desc }}
                    </p>
                </div>
            </div>

            <div class="illus purple-curves" v-if="has_illus"></div>
            <div class="illus green-dashes" v-if="has_illus"></div>
        </div>
    </section>
</template>

<script>

export default {
    props: ['section_title', 'list', 'box_title', 'desc', 'has_illus'],

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
