<template>
    <section class="section pt60 pt30t pb10 pb30t element-loader loading">
        <div class="container">
            <h2 class="mb25 has-text-centered">{{ title }}</h2>
            
            <div class="box position" v-for="(pos, i) in positions">
                <a href="javascript:;" class="is-flex align-center has-text-dark" @click="expand(i)">
                    <div class="icon-holder is-relative">
                        <i :class="
                            ['mdi', 'mdi-plus', 'is-size-1', 'has-text-primary', 'm0-20', 'ml0t', 'mr10t',
                            {'is-not-visible': expands[i]}]
                        "></i>
                        <i :class="
                            ['mdi', 'mdi-minus', 'is-size-1', 'has-text-primary', 'm0-20', 'ml0t', 'mr10t', 'is-absolute', 't0',
                            {'is-not-visible': !expands[i]}]
                        "></i>
                    </div>
                    <h4>
                        {{ pos.info.title }}
                    </h4>
                </a>
                <div v-if="expands[i]" class="pl80 pl0t mt20">
                    <div v-html="pos.info.desc"></div>
                    <a :href="pos.info.link" class="button is-primary m30-0" target="_blank">
                        <span>Apply now</span>
                    </a>
                </div>
            </div>
        </div>
    </section>
</template>

<script>

export default {
    props: ['title', 'positions'],

    data: function () {
        return {
            expands: [],
            opa: 'opaa'
        }
    },
    methods: {
        expand: function (i) {
            Vue.set(this.expands, i, !this.expands[i])
        },
        toggleOpa: function (ops) {
            this.opa = ops
        }
    },
    computed: {
        
    },
    mounted: function () {
        for (let i = 0; i < this.positions.length; i++) {
            this.expands.push(false)
        }
    }
}
</script>
