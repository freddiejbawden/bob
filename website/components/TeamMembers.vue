<template>
    <section class="section element-loader loading">
        <div class="container">
            <div class="columns flex-wrap">
                <div class="column mb30 is-12" v-for="(member, i) in team_members" v-if="extended">
                    <div class="box">
                        <div class="columns">
                            <div class="column is-3 is-flex justify-center p30">
                                <figure class="image is-220x220 is-rounded">
                                    <img :src="member.imagesFolder+member.info.img" :alt="member.info.name">
                                </figure>
                            </div>
                            <div class="column is-9 is-flex direction-column justify-center p30">
                                <div class="is-flex align-center is-block-tablet">
                                    <h4>
                                        {{ member.info.name }}
                                    </h4>
                                    <div class="purple-hyphen"></div>
                                    <h5>"{{ member.info.motto }}"</h5>
                                </div>
                                <p v-line-clamp="{ 
                                    lines: 5,
                                    text: member.info.desc,
                                    expanded: member.expand
                                    }"></p>
                                <a href="javascript:;" @click="toggleMore(i)">
                                <!-- <a href="javascript:;" @click="toggleMore(i)" v-if="member.overflows"> -->
                                    See 
                                    <span v-if="member.expand">less</span> 
                                    <span v-else>more</span>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column p0-15 is-6 pb30t" v-for="(member, i) in team_members" v-if="!extended">
                    <div class="box" v-if="!minimized">
                        <div class="columns">
                            <div class="column is-5 is-flex align-center justify-center p30">
                                <figure class="image is-160x160 is-rounded">
                                    <img :src="member.imagesFolder+member.info.img" :alt="member.info.name">
                                </figure>
                            </div>
                            <div class="column is-7 is-flex direction-column justify-center">
                                <h3>
                                    {{ member.name }}
                                </h3>
                                <h5 class="has-text-grey mb20">{{ member.info.position }}</h5>
                                <a :href="'tel:' + member.info.tel" class="is-flex align-center has-text-dark">
                                    <i class="mdi mdi-phone is-size-4 has-text-primary mr10"></i>
                                    {{ member.info.tel }}
                                </a>
                                <a :href="'mailto:' + member.info.mail" class="is-flex align-center has-text-dark">
                                    <i class="mdi mdi-email is-size-4 has-text-primary mr10"></i>
                                    {{ member.info.mail }}
                                </a>
                            </div>
                        </div>
                    </div>
                    <div class="box p25" v-if="minimized">
                        <div class="columns flex-wrap">
                            <div class="column">
                                <h6>{{ member.name }}</h6>
                                <p class="mb0">
                                    {{ member.position }}
                                </p>
                            </div>
                            <div class="column has-text-right">
                                <p>
                                   <a :href="'tel:' + member.tel">{{ member.tel }}</a>
                                </p>
                                <p class="mb0">
                                    <a :href="'mailto:' + member.mail">{{ member.mail }}</a>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>

var lineClamp = require('vue-line-clamp-extended').lineClamp
Vue.directive('line-clamp', lineClamp)

export default {
    props: ['members', 'extended', 'minimized'],

    data: function () {
        return {
            lines: [],
            init_line: 6,
            team_members: []
        }
    },
    methods: {
        toggleMore: function (i) {
            let newVal = {}
            if (this.team_members[i].expand == undefined) {
            //     this.team_members[0].expand = true
            //     return
                newVal = Object.assign({}, this.team_members[i], {expand: true})
            } else {
                newVal = Object.assign({}, this.team_members[i], {expand: !this.team_members[i].expand})
            }
            // this.team_members[0].expand = !this.team_members[0].expand
            // console.log(this.members[0].expand)
            Vue.set(this.team_members, i, newVal)
        }
    },
    mounted: function () {
        this.team_members = this.members
        // for (let i = 0; i < this.members.length; i++) {
        //     this.members[i].expand = false
        // }
        let j = 0
        // this.$on('is-expandable', bool => {
        //     this.team_members[j].overflows = bool
        //     j++
        // })
    }
}
</script>
