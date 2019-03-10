<template>
    <section class="section element-loader loading">
        <div class="container">
            <h2 class="has-text-centered mb20">{{ section_title }}</h2>

            <div class="columns">
                <div class="column is-1 hero-nav justify-center mt0">
                    <a 
                        href="javascript:;" 
                        :class="{'is-disabled': prev_disabled}"
                        @click="prevSlide()">
                        <i class="mdi mdi-chevron-left"></i>
                    </a>
                </div>
                <div class="column">
                    <transition name="slide" mode="out-in">
                        <div class="curved-section"
                            v-for="(reference, i) in references" 
                            v-if="i == current_slide"
                            :key="'reference' + i">

                            <svg viewBox="0 0 1032 315" class="is-not-browser-ie">
                                <defs>
                                    <path d="M57,64 L1069,64 C1071.76142,64 1074,66.2385762 1074,69 L1074,338.165033 C903.612695,358.721678 733.261132,369 562.945312,369 C392.629492,369 222.314388,358.721678 52,338.165033 L52,69 C52,66.2385763 54.2385763,64 57,64 Z" id="ref_curve"></path>
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
                                        <image 
                                            height="100%"
                                            width="20%"
                                            x="50"
                                            y="60"
                                            :xlink:href="reference.imagesFolder+reference.info.img"
                                            style="clip-path:url(#clip_ref_curve);"></image>
                                    </g>
                                </g>
                            </svg>
                            <div class="curved-content has-text-dark has-nostyle">
                                <div class="columns is-full-height">
                                    <div class="column is-3 is-not-browser-ie">
                                        
                                    </div>
                                    <div class="column is-2 is-browser-ie">
                                        
                                    </div>
                                    <div class="column is-7 is-offset-1 direction-column justify-center">
                                        <p>
                                            {{ reference.info.name }}, {{ reference.info.info }}
                                        </p>
                                        <h5 v-html="reference.info.desc"></h5>

                                    </div>
                                </div>
                            </div>

                            <div class="illus purple-dots flipped-x"></div>
                        </div>
                    </transition>
                </div>
                <div class="column is-1 hero-nav justify-center mt0">
                    <a 
                        href="javascript:;" 
                        :class="{'is-disabled': next_disabled}"
                        @click="nextSlide()">
                        <i class="mdi mdi-chevron-right"></i>
                    </a>
                </div>
            </div>
        </div>
    </section>
</template>

<script>

export default {
    props: ['section_title', 'references'],

    data: function () {
        return {
            current_slide: 0,
        }
    },
    methods: {
        nextSlide: function () {
            if (this.current_slide < this.slides_length - 1) {
                this.current_slide++
            }
        },
        prevSlide: function () {
            if (this.current_slide > 0) {
                this.current_slide--
            }
        },
    },
    computed: {
        slides_length: function () {
            return this.references.length
        },
        next_disabled: function () {
            return this.current_slide == this.slides_length - 1
        },
        prev_disabled: function () {
            return this.current_slide == 0
        }
    }
}
</script>
