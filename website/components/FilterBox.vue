<template>
    <section class="section is-medium element-loader loading">
        <div class="container">
            <div class="box p30">
                <div class="is-flex">
                    <div class="is-flex pl15 pr15" v-for="filter in filters">
                        <p>{{ filter.label }}</p>
                        <select name="" id="" class="select-input">
                            <option :value="option.value" v-for="option in filter.options">{{ option.name }}</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
<script>

export default {
    props: ['filters'],

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
