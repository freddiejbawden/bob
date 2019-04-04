<template>
    <div>
        <page-title
            title="Create a new warehouse"
        ></page-title>

        <section class="section">
            <div class="container is-flex justify-center">
                <div class="half-width">
                    <nuxt-link to="/merchant/warehouses" class="is-inline-block mb15">Back to all warehouses</nuxt-link>

                    <div class="box p30 pl50 pr50">
                        <form action="">
                            <div class="field">
                                <label class="label">* Warehouse name:</label>
                                <div class="control">
                                    <input class="input" type="text" placeholder="Enter your warehouse name" v-model="name">
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Image:</label>
                                <div class="control">
                                    <input class="input" type="file" placeholder="Enter your warehouse name" @change="uploadFile">
                                </div>
                                <img class="small-img mt15" :src="image" alt="">
                            </div>
                            <div class="field">
                                <label class="label">Location coordinates:</label>
                                <div class="control columns">
                                    <div class="column is-6">
                                        <input class="input" type="text" placeholder="Enter latitude" v-model.number="location.latitude">
                                    </div>
                                    <div class="column is-6">
                                        <input class="input" type="text" placeholder="Enter longitude" v-model.number="location.longitude">
                                    </div>
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Warehouse schema:</label>
                                <p class="help is-size-8">
                                    Enter the dimensions of the warehouse. X and Y values are the amount of rows and columns that the warehouse physically has for the robot.
                                </p>
                                <div class="control columns">
                                    <div class="column is-6">
                                        <input class="input" type="number" placeholder="* Enter X dim" v-model.number="dimensions.x">
                                    </div>
                                    <div class="column is-6">
                                        <input class="input" type="number" placeholder="* Enter Y dim" v-model.number="dimensions.y">
                                    </div>
                                </div>
                                <p class="help is-size-8">
                                    The Z values are the amount of shelfs and their respected heights from the robot's perspective. (Include bottom shelf as 0.0)
                                </p>
                                <div
                                    v-for="(shelf, i) in dimensions.z"
                                    :key="'shelf-' + i"
                                    class="is-flex align-center mb10">

                                    <input 
                                        type="number" 
                                        class="input half-width" 
                                        :placeholder="'Enter shelf N' + (i + 1) + ' height'"
                                        v-model.number="dimensions.z[i]">
                                    <a 
                                        href="javascript:;" 
                                        class="is-inline-block has-text-danger ml10" 
                                        @click="deleteShelf(i)">
                                       
                                        <i class="mdi mdi-minus-circle is-size-4"></i>
                                    </a>
                                </div>

                                <a href="javascript:;" class="button is-link is-outlined is-smallish mt15" @click="addShelf()">
                                    <span>Add a shelf</span>
                                </a>
                            </div>
                            
                            <div class="field">
                                <div class="control pt30">
                                    <a 
                                        href="javascript:;"
                                        class="button is-link" 
                                        :disabled="!can_submit"
                                        @click.stop.prevent="addWarehouse()">
                                        <span>Add warehouse</span>
                                    </a>
                                </div>
                            </div>
                        </form>
                    </div>

                    <nuxt-link to="/merchant/warehouses" class="is-inline-block">Back to all warehouses</nuxt-link>
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
            name: "",
            image: null,
            location: {
                latitude: "",
                longitude: ""
            },
            dimensions: {
                x: "",
                y: "",
                z: [
                    0.0
                ]
            }
        }
    },
    methods: {
        addShelf: function () {
            this.dimensions.z.push(this.dimensions.z[this.dimensions.z.length - 1])
        },
        deleteShelf: function (i) {
            this.dimensions.z.splice(i, 1)
        },
        uploadFile: function (event) {
            let file = event.target.files[0]
            this.createImage(file);
        },
        createImage(file) {
            var image = new Image();
            var reader = new FileReader();

            reader.onload = (e) => {
                this.image = e.target.result;
            };

            reader.readAsDataURL(file);
        },
        addWarehouse () {
            if (this.can_submit) {
                axios.
                    post(process.env.baseUrl + '/api/warehouse/', {
                        name: this.name,
                        image: this.image,
                        location: this.location,
                        dimensions: this.dimensions,
                        items: []
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                            'username': this.$store.state.user.username,
                        }
                    })
                    .then((res) => {
                        console.log("Server response: ", res);
    
                        if (res.status == 200) {
                            this.$router.push('/merchant/warehouses/' + res.data.warehouse._id).go(1)
                        }
                    })
                    .catch(function(error) {
                        console.error("Error adding document: ", error);
                    });
            }
        }
    },
    computed: {
        can_submit: function () {
            return this.name.toString().length > 0 && this.dimensions.x.toString().length > 0 && this.dimensions.y.toString().length > 0
        }
    }
};
</script>

<style lang="sass" scoped>


</style>
