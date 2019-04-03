<template>
    <div>

        <page-title
            :title="'Edit warehouse ' + (warehouse ? warehouse.name : 'loading...')"
        ></page-title>

        <section class="section" v-if="warehouse != null">
            <div class="container is-flex justify-center">
                <div class="half-width">
                    <nuxt-link to="/merchant/warehouses" class="is-inline-block mb15">Back to all warehouses</nuxt-link>

                    <div class="box p30 pl50 pr50">
                        <form action="">
                            <div class="field">
                                <label class="label">Warehouse name:</label>
                                <div class="control">
                                    <input class="input" type="text" placeholder="Enter your warehouse name" v-model="warehouse.name">
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Image:</label>
                                <div class="control">
                                    <input class="input" type="file" placeholder="Enter your warehouse name" @change="uploadFile">
                                </div>
                                <img class="small-img mt15" :src="warehouse.image" alt="">
                            </div>
                            <div class="field">
                                <label class="label">Location coordinates:</label>
                                <div class="control columns">
                                    <div class="column is-6">
                                        <input class="input" type="text" placeholder="Enter latitude" v-model.number="warehouse.location.latitude">
                                    </div>
                                    <div class="column is-6">
                                        <input class="input" type="text" placeholder="Enter longitude" v-model.number="warehouse.location.longitude">
                                    </div>
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Warehouse schema:</label>
                                <p class="help is-size-8">
                                    Enter the dimensions of the warehouse. X and Y values are the amount of rows and columns that the warehouse phisically has for the robot.
                                </p>
                                <div class="control columns">
                                    <div class="column is-6">
                                        <input class="input" type="number" placeholder="Enter X dim" v-model.number="warehouse.dimensions.x">
                                    </div>
                                    <div class="column is-6">
                                        <input class="input" type="number" placeholder="Enter Y dim" v-model.number="warehouse.dimensions.y">
                                    </div>
                                </div>
                                <p class="help is-size-8">
                                    The Z values are the amount of shelfs and their respected heights from the robot's perspective. (Include bottom shelf as 0.0)
                                </p>
                                <input 
                                    type="number" 
                                    class="input half-width mb10" 
                                    v-for="(shelf, i) in warehouse.dimensions.z"
                                    :key="'shelf-' + i"
                                    :placeholder="'Enter shelf N' + (i + 1) + ' height'"
                                    v-model.number="warehouse.dimensions.z[i]">

                                <a href="javascript:;" class="button is-link is-outlined is-smallish mt15" @click="addShelf()">
                                    <span>Add a shelf</span>
                                </a>
                            </div>
                            
                            <div class="field">
                                <div class="control pt30">
                                    <a 
                                        href="javascript:;"
                                        class="button is-link" 
                                        @click.stop.prevent="updateWarehouse()">
                                        <span>Update warehouse</span>
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
            warehouseId: this.$nuxt._route.params.id,
            warehouse: null,
        }
    },
    methods: {
        addShelf: function () {
            this.warehouse.dimensions.z.push(this.warehouse.dimensions.z[this.warehouse.dimensions.z.length - 1])
        },
        uploadFile: function (event) {
            let file = event.target.files[0]
            this.createImage(file);
        },
        createImage(file) {
            var image = new Image();
            var reader = new FileReader();

            reader.onload = (e) => {
                this.warehouse.image = e.target.result;
            };

            reader.readAsDataURL(file);
        },
        getWarehouse () {
            axios.
                get(process.env.baseUrl + '/api/warehouse/' + this.warehouseId, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then((res) => {
                    console.log("Server response: ", res);
                    
                    this.warehouse = res.data.warehouse
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
        },
        updateWarehouse: function () {
            axios.
                post(process.env.baseUrl + '/api/warehouse/', this.warehouse, {
                    headers: {
                        'Content-Type': 'application/json',
                        'username': this.$store.state.user.username,
                    }
                })
                .then((res) => {
                    console.log("Server response: ", res);

                    if (res.status == 200) {
                        this.$router.push('/merchant/warehouses/' + this.warehouseId).go(1)
                    }
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
        }
    },
    mounted: function () {
        this.getWarehouse()
    }
};
</script>

<style lang="sass" scoped>

</style>
