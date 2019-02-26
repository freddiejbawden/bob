<template>
    <section class="section is-relative p0">
        <div class="columns m0t">
            <div :class="[
                'column', 'oh', 'p0t', 'is-relative',
                {'is-6': is_carousel},
                {'is-7': !is_carousel},
            ]">
                
                <!-- <div class="img-bckg is-browser-ie" 
                    :style="{'background-image': 'url(' + slide.img + ')'}"
                    v-for="(slide, i) in slides" 
                    :key="'img' + i"></div> -->
                
                <!-- <div class="is-hidden-desktop" 
                v-for="(slide, i) in slides" 
                :key="'img' + i">
                    <img :src="slide.img" alt="slide.title">
                </div>
                <div class="img-bckg static is-Ax200-t" 
                    :style="{'background-image': 'url(' + slide.img + ')'}"
                    v-for="(slide, i) in slides" 
                    :key="'img' + i"></div> -->
                
                <svg class="hero-svg is-not-browser-ie is-hidden-touch" viewBox="0 0 772 606" preserveAspectRatio="xMaxYMax meet">
                    <defs>
                        <path id="clip_path" d="M0,0 L740,0 C757.746303,100 766.619454,200 766.619454,300 C766.619454,400 757.746303,500 740,600 L0,600 L0,0 Z"></path>
                    </defs>
                    <clipPath id="clip">
                        <use xlink:href="#clip_path"  style="overflow:visible;"/>
                    </clipPath>
                    <g style="clip-path:url(#clip);">
                        <image  
                            width="120%" 
                            height="100%"
                            x="-10%"
                            xlink:href="~/assets/images/hero.png" 
                            v-for="(slide, i) in slides" 
                            :key="'img' + i"></image>
                        <rect x="0" y="0" width="100%" height="100%" fill="#646464" fill-opacity="0.15"></rect>
                    </g>
                </svg>

            </div>
            <div :class="[
                    'column', 'is-4', 'pl50', 'is-flex', 'direction-column', 'hero-slide', 
                    {'justify-space-between': is_carousel},
                    {'justify-center': slides.length == 1},
                    {'pt100': is_carousel}, 'p30t', 'pb20'
                ]">
                <div>
                    <br>
                </div>

                <div 
                    v-for="(slide, i) in slides"
                    :key="'slide' + i">
                    
                    <!-- <div class="date-place-stamp">
                        {{ slide.dates }} <span class="divider">|</span> {{ slide.place }}
                    </div> -->
                    <!-- <h1 v-if="slide.title" class="mt0" v-line-clamp="{ 
                        lines: 5,
                        text: slide.title
                    }"></h1> -->
                    <h1 class="mt0">
                        {{ slide.title }}
                    </h1>
                    <p>
                        {{ slide.short_description }}
                    </p>
                    <a :href="slide.path" class="button is-primary mt30">
                        <span>Learn more</span>
                    </a>
                    <!-- <p v-if="!is_carousel" class="has-text-grey is-size-6 mt30">
                        Or scroll down to learn more <i class="mdi mdi-chevron-down"></i>
                    </p> -->
                </div>
            </div>
        </div>
        <div class="illus purple-mesh" v-if="has_icon"></div>
    </section>
</template>

<script>
// import { headroom } from 'vue-headroom'


export default {
    props: ['slides', 'has_icon', 'is_carousel'],
    // components: {
    //     headroom
    // },

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
        }
    },
    computed: {
        slides_length: function () {
            return this.slides.length
        },
        next_disabled: function () {
            return this.current_slide == this.slides_length - 1
        },
        prev_disabled: function () {
            return this.current_slide == 0
        }
    },
    mounted: function () {
        if (this.slides) {
            this.$emit('send-project', {
                title: this.slides[0].title,
                url: this.slides[0].url
            })
        }
    }
}
</script>
