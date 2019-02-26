<template>
    <section class="section pt60 pt30t pb0">
        <div class="container has-text-centered">
            <h1 class="mb25">{{ title }}</h1>
            <p v-if="desc" class="max-width-half is-full-width-tablet m0-a m0t">
                {{ desc }}
            </p>
        </div>
    </section>
</template>

<script>

export default {
    props: ['title', 'desc'],

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
