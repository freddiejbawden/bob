<template>
    <section class="section is-relative element-loader loading">
        <div class="container is-relative z10">
            <h2 class="has-text-centered mb25" v-if="section_title">{{ section_title }}</h2>
            <div class="columns flex-wrap">
                <div class="column is-4-desktop is-4-tablet is-12-mobile pb30 pb10t" v-for="(story, i) in stories">
                    <a :href="story.url" class="box story m0t">
                        <figure class="img-holder is-Ax240 is-Ax120-t has-rounded-corners" v-if="story.img">
                            <img :src="story.img" :alt="story.title">
                        </figure>
                        <div v-else><br></div>
                        <h4 v-line-clamp="{ 
                            lines: 4,
                            text: story.title
                        }">
                        </h4>
                        <div class="is-flex">
                            <p class="date">
                                {{ story.date }}
                            </p>
                            <p v-line-clamp="{ 
                                lines: 6,
                                text: story.desc
                            }">
                            </p>
                        </div>
                    </a>
                </div>
            </div>
            <div class="has-text-centered mt30" v-if="section_button">
                <a :href="section_button.url" class="button is-primary">
                    <span>{{ section_button.name }}</span>
                </a>
            </div>
        </div>

        <div class="illus green-egg"></div>
        <div class="illus purple-circle"></div>
    </section>
</template>

<script>

var lineClamp = require('vue-line-clamp-extended').lineClamp
Vue.directive('line-clamp', lineClamp)

export default {
    props: ['section_title', 'section_button', 'stories'],

    data: function () {
        return {
            
        }
    },
    methods: {
        
    },
    computed: {
        
    }
}
</script>
