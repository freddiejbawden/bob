<template>
    <div>

        <page-title
            title="A list of all warehouses"
        ></page-title>


        <section class="section">
            <div class="container">
                <div class="is-flex justify-end">
                    <nuxt-link to="/merchant/warehouses/create" class="button is-link mb15">
                        <span>Add a warehouse</span>
                    </nuxt-link>
                </div>
                <div class="box is-full-width">
                    <table class="table is-full-width" v-if="warehouses.length > 0">
                        <thead>
                            <tr>
                                <td>Warehouse name</td>
                                <td>Location</td>
                                <td>Dimensions</td>
                                <td>Shelves count</td>
                                <td>Items count</td>
                                <td>View warehouse</td>
                                <td>Edit warehouse</td>
                                <td>Delete warehouse</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(warehouse, i) in warehouses" :key="warehouse._id">
                                <td>
                                    <b>{{ warehouse.name }}</b>
                                </td>
                                <td>
                                    {{ warehouse.location ? warehouse.location.latitude : 'not set' }}, 
                                    {{ warehouse.location ? warehouse.location.longitude : 'not set' }} 
                                </td>
                                <td>
                                    X: {{ warehouse.dimensions ? warehouse.dimensions.x : 'not set' }}, 
                                    Y: {{ warehouse.dimensions ? warehouse.dimensions.y : 'not set' }}
                                </td>
                                <td>
                                    {{ warehouse.dimensions ? warehouse.dimensions.z.length : 0 }}
                                </td>
                                <td>
                                    {{ warehouse.items ? warehouse.items.length : 0 }}
                                </td>
                                <td>
                                    <nuxt-link :to="'/merchant/warehouses/' + warehouse._id" class="has-text-info">
                                        <i class="mdi mdi-eye"></i>
                                        View
                                    </nuxt-link>
                                </td>
                                <td>
                                    <nuxt-link :to="'/merchant/warehouses/edit/' + warehouse._id" class="has-text-success">
                                        <i class="mdi mdi-pencil"></i>
                                        Edit
                                    </nuxt-link>
                                </td>
                                <td>
                                    <a href="javascript:;" class="has-text-danger" @click="deleteWarehouse(warehouse._id, i)">
                                        <i class="mdi mdi-delete"></i>
                                        Delete
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <h3 class="has-text-centered m30-0" v-else>
                        You still haven't added any warehouses.
                    </h3>
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
            warehouses: []
        }
    },
    methods: {
        filterWarehouses: function (warehouses) {
            return warehouses.filter((warehouse) => {
                return warehouse.merchantId == this.$store.state.user._id
            })
        },
        getWarehouses () {
            axios.
                get('http://localhost:9000/api/warehouse/', {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then((res) => {
                    console.log("Server response: ", res);

                    this.warehouses = this.filterWarehouses(res.data.warehouses)
                    // this.warehouses = res.data.warehouses

                    // if (res.status == 200) {
                    //     this.$router.push('/merchant/orders').go(1)
                    // }
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
        },
        deleteWarehouse: function (warehouseId, i) {
            this.warehouses.splice(i, 1)
        }
    },
    mounted: function () {
        this.getWarehouses()
    }
};
</script>

<style lang="sass" scoped>

</style>
