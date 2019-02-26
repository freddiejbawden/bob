<template>
    <section class="section element-loader loading is-relative">
        <div class="container is-relative z10">
            <h2 class="mb25 has-text-centered" v-if="project_title">{{ project_title }}</h2>

            <div class="is-relative">
                <div 
                    :class="[
                        'columns', 'flex-wrap', 'align-center', 'is-relative', 'z10',
                        {'element-loader': loading, 'loading': loading, }
                    ]">
                    <div class="column is-3-tablet is-6-mobile p15" 
                        v-if="i > (start_from - 1)"
                        v-for="(post, i) in posts">
                        <a :href="post.link" class="event-holder" target="_blank">
                            <img :src="post.images.standard_resolution.url" :alt="post.caption.text">
                        </a>
                    </div>
                </div>

                <div class="illus purple-dots smaller flipped-x z20" v-if="has_illus"></div>
            </div>

            <div class="is-flex justify-space-between flex-wrap mt30 justify-center-mobile" v-if="pagination">
                <a href="javascript:;" class="button is-primary is-outlined mb10t" @click="prevFeed()">
                    <span>Prev</span>
                </a>
                <a href="javascript:;" class="button is-primary" @click="nextFeed()">
                    <span>Next</span>
                </a>
            </div>
        </div>

        <div class="illus green-donut" v-if="has_illus"></div>
    </section>
</template>

<script>

import jsonp from 'browser-jsonp'

export default {
    props: ['project_title', 'count', 'from', 'pagination', 'has_illus'],  

    data: function () {
        return {
            start_from: 0,
            token: '3540941447.1677ed0.9a3438e47d2b4c2585d67633c766c497',
            url: 'https://api.instagram.com/v1/users/self/media/recent',
            next_url: '',
            prev_url: [],
            posts: [],
            loading: false
        }
    },
    methods: {
        prevFeed: function () {
            this.getUserFeed(this.prev_url[this.prev_url.length - 2])
            this.prev_url.pop()
            this.prev_url.pop()
        },
        nextFeed: function () {
            if (this.start_from) this.start_from = 0
            this.getUserFeed(this.next_url)
        },
        getUserFeed (url) {
            this.loading = true
            jsonp({
                url: (url ? url : this.url),
                data: { access_token: this.token, count: this.start_from ? (this.count + this.start_from) : this.count},
                error: error => { throw error },
                complete: response => {
                    this.posts = response.data
                    this.prev_url.push(url ? url : this.url)
                    this.next_url = response.pagination.next_url

                    this.loading = false
                }
            })
        }
    },
    computed: {
        
    },
    mounted: function () {
        if (this.from) this.start_from = this.from
        
        this.getUserFeed()
    }
}
</script>
