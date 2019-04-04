<template>
    <div>

        <page-title
            title="About the Team"
            desc="Meet the young team responsible for bringing the vision of Bob to life. Our success has been built upon our team's vast skillset and excellent teamwork."
        ></page-title>

        <section class="section">
            <div class="container">
                <img src="~/assets/images/team.jpg" class="box p0" alt="Assis10t">

                <div class="columns flex-wrap mt30">
                    <div 
                        class="column is-3 has-text-centered"
                        v-for="(member, i) in members"
                        :key="'member-' + i">

                        <h3>{{ member.name }}</h3>
                        <h5 class="has-text-grey">{{ member.position }}</h5>
                    </div>
                </div>
            </div>
        </section>

    </div>
</template>

<script>
import PageTitle from '~/components/PageTitle'
import axios from 'axios'

export default {
    components: {
        PageTitle
    },
    data: function () {
        return {
            members: [
                {
                    name: 'Alex',
                    position: 'Robot Vision and Movement'
                },
                {
                    name: 'Jacob',
                    position: 'Hardware and Construction'
                },
                {
                    name: 'Anna',
                    position: 'Hardware, Construction and Admin'
                },
                {
                    name: 'Freddie',
                    position: 'Robot Networking and Pathfinding'
                },
                {
                    name: 'Harry',
                    position: 'Web Development and Design'
                },
                {
                    name: 'Kieran',
                    position: 'Server Development'
                },
                {
                    name: 'Claire',
                    position: 'Robot Vision and Movement'
                },
                {
                    name: 'Oktay',
                    position: 'App and Server Development'
                },
            ]
        }
    },
    methods: {

    }
};
</script>

<style lang="sass" scoped>

</style>
