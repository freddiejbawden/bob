<template>

    <hero 
        :slides="[
            {
                title: 'Meet the Bob',
                short_description: 'Bob (Brilliant Online Buying) is a shopping assistant robot designed to help you.',
                
            }
        ]"
        :is_carousel="false"
        :has_icon="true"
    ></hero> 

</template>

<script>
import Hero from "~/components/Hero.vue";

export default {
    components: {
        Hero
    },
    data: function () {
        return {

        }
    },
    computed: {
        user: function () {
            return this.$store.state.user
        }
    }
};
</script>

<style lang="sass">
</style>
