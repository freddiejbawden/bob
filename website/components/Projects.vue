<template>
    <section class="section is-relative element-loader loading">
        <div class="container is-relative z10">
            <h2 class="has-text-centered mb25" v-if="section_title">{{ section_title }}</h2>
            
            <div v-if="extended">
                <div class="box p0 mb40" v-for="(project, i) in projects">
                    <div class="columns m0">
                        <div class="column is-5 p0">
                            <a :href="project.path" class="is-block is-full-width is-full-height has-scaled-hover has-rounded-corners mb10">
                                <figure class="img-holder is-full-width is-full-height has-rounded-corners has-bckg-grey is-Ax200-t">
                                    <img :src="project.img" :alt="project.title">
                                </figure>
                            </a>
                        </div>

                        <div class="column is-7 pt30 pb30 pl50 p15t">
                            <p v-if="project.type_id" class="has-text-primary mb5 mt0">{{ project.type.name }}</p>
                            <h3 class="mt0 mb20">{{ project.title }}</h3>
                            
                            <div v-if="project.info.length" class="columns is-mobile flex-wrap">
                                <div class="column is-4-tablet is-6-mobile" v-for="info in project.info">
                                    <p class="mt0 mb5">{{ info.title }}</p>
                                    <h6 :class="{'has-info-tooltip': info.additional, 'lh1-1': true}">
                                        {{ info.desc }}

                                        <div class="info-tooltip" v-if="info.additional">
                                            <div class="box">
                                                <h6 class="has-text-centered mb30">{{ info.additional.title }}</h6>

                                                <div class="columns flex-wrap mb10">
                                                    <div class="column is-6 p0" v-for="text in info.additional.texts">
                                                        <p class="mt0 mb5">
                                                            {{ text.text }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </h6>
                                </div>
                            </div>
                            <div v-else class="columns flex-wrap">
                                <p>{{ project.short_description }}</p>
                            </div>

                            <div class="has-text-centered-mobile">
                                <a :href="project.path" class="button is-primary is-outlined mt20">
                                    <span>See more</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="columns" v-else>
                <div class="column is-4 mb20t" v-for="(project, i) in projects">
                    <div :class="{
                        'has-svg-corner': i == 0 || i == projects.length - 1,
                        'corner-green': i == 0,    
                        'corner-purple': i == projects.length - 1,    
                    }">
                        <a :href="project.path" class="is-block has-scaled-hover has-rounded-corners mb10">
                            <figure class="img-holder is-Ax240 is-Ax120-t has-rounded-corners has-bckg-grey">
                                <img :src="project.img" :alt="project.title">
                            </figure>
                        </a>
                    </div>
                    <!-- <div class="date-place-stamp">
                        {{ project.dates }} <span class="divider">|</span> {{ project.place }}
                    </div> -->
                    <h4>
                        <a :href="project.path">{{ project.title }}</a>
                    </h4>
                </div>
            </div>
            <div class="has-text-centered mt30" v-if="section_button">
                <a :href="section_button.url" class="button is-primary">
                    <span>{{ section_button.name }}</span>
                </a>
            </div>
        </div>

        <div class="illus green-blob"></div>
    </section>
</template>

<script>

export default {
    props: ['section_title', 'section_button', 'projects', 'extended'],

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
