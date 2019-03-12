<template>
    <div>

        <page-title
            :title="warehouse.name"
        ></page-title>

        <section class="section">
            <div class="container">
                <div class="box is-full-width p30 pl50 pr50">
                    <div class="columns">
                        <div class="column">
                            <div class="mb10">
                                <b>Image</b>
                            </div>
                            <img class="small-img" :src="warehouse.image" :alt="warehouse.name" v-if="warehouse.image">
                        </div>
                        <div class="column">
                            <div class="mb10">
                                <b>Location</b>
                            </div>
                            Latitude: <i>{{ warehouse.location ? warehouse.location.latitude : 'not set' }}</i> <br>
                            Longitude: <i>{{ warehouse.location ? warehouse.location.longitude : 'not set' }} </i>
                        </div>
                        <div class="column">
                            <div class="mb10">
                                <b>Dimensions</b>
                            </div>
                            X: <i>{{ warehouse.dimensions ? warehouse.dimensions.x : 'not set' }}</i> <br>
                            Y: <i>{{ warehouse.dimensions ? warehouse.dimensions.y : 'not set' }} </i>
                        </div>
                        <div class="column">
                            <div class="mb10">
                                <b>Shelves ({{ warehouse.dimensions ? warehouse.dimensions.z.length : 0 }})</b>
                            </div>
                            <div v-if="warehouse.dimensions">
                                <div v-for="(shelf, i) in warehouse.dimensions.z" :key="'shelf-' + i">
                                    Shelf {{ i }}: <i>{{ shelf }} m</i>
                                </div>
                            </div>
                        </div>
                        <div class="column">
                            <div class="mb10">
                                <b>Stats</b>
                            </div>
                            <div class="mb10">
                                Items: <i>{{ items.length }}</i>
                            </div>
                            <div class="mb10">
                                Orders: <i>{{ orders.length }}</i>
                            </div>
                        </div>
                        <div class="column">
                            <div class="mb10">
                                <b>Controls</b>
                            </div>
                            <nuxt-link :to="'/merchant/warehouses/edit/' + warehouse._id" class="is-inline-block has-text-success mb10">
                                <i class="mdi mdi-pencil"></i>
                                Edit
                            </nuxt-link> <br>
                            <a href="#" class="is-inline-block has-text-danger mb10">
                                <i class="mdi mdi-delete"></i>
                                Delete
                            </a>
                        </div>
                    </div>
                </div>

                <h3 class="has-text-centered mt50 mb20">Orders</h3>

                <div class="box is-full-width">
                    <table class="table is-full-width" v-if="orders.length > 0">
                        <thead>
                            <tr>
                                <td>Items</td>
                                <td>Timestamp</td>
                                <td>Status</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="order in orders" :key="order._id">
                                <td>
                                    <span v-for="item in order.items" :key="item._id">
                                        {{ item.name }}, 
                                    </span>
                                </td>
                                <td>
                                    {{ order.timestamp }}
                                </td>
                                <td>
                                    <span :class="[
                                        {'has-text-warning': order.status == 'PENDING'},
                                        {'has-text-info': order.status == 'IN_TRANSIT'},
                                        {'has-text-success': order.status == 'COMPLETE'},
                                        {'has-text-danger': order.status == 'CANCELED'},
                                    ]">
                                        <b>{{ order.status }}</b>
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <h3 class="has-text-centered m30-0" v-else>
                        No orders have been placed.
                    </h3>
                </div>

                <h3 class="has-text-centered mt50 mb20">Items</h3>

                <div class="box is-full-width">
                    <table class="table is-full-width" v-if="items.length > 0">
                        <thead>
                            <tr>
                                <td>Name</td>
                                <td>Image</td>
                                <td>Position</td>
                                <td>Quantity</td>
                                <td>Unit</td>
                                <td>Price</td>
                                <td>Edit items</td>
                                <td>Delete items</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, i) in items" :key="item._id">
                                <td>
                                    <b>{{ item.name }}</b>
                                </td>
                                <td>
                                    <img class="small-img" :src="item.image" :alt="item.name" v-if="item.image">
                                </td>
                                <td>
                                    X: <i>{{ item.position ? item.position.x : 'not set' }},</i>
                                    Y: <i>{{ item.position ? item.position.y : 'not set' }}</i> <br>
                                    Shelf: <i>{{ item.position ? item.position.z : 'not set' }} </i><br>
                                </td>
                                <td>
                                    {{ item.quantity }}
                                </td>
                                <td>
                                    {{ item.unit }}
                                </td>
                                <td>
                                    {{ item.price }} GBP
                                </td>

                                <td>
                                    <nuxt-link :to="'/merchant/items/edit/' + warehouseId + '_' + item._id" class="has-text-success">
                                        <i class="mdi mdi-pencil"></i>
                                        Edit
                                    </nuxt-link>
                                </td>
                                <td>
                                    <a href="javascript:;" class="has-text-danger" @click="deleteItem(warehouseId, item._id, i)">
                                        <i class="mdi mdi-delete"></i>
                                        Delete
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <h3 class="has-text-centered m30-0" v-else>
                        You still haven't added any items.
                    </h3>
                </div>
                <div class="is-flex justify-start align-center">
                    <nuxt-link 
                        :to="'/merchant/items/create/' + warehouseId" 
                        class="button is-link">
                        <span>Add an item to this warehouse</span>
                    </nuxt-link>
                    <nuxt-link to="/merchant/warehouses" class="is-inline-block ml20">Back to all warehouses</nuxt-link>
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
            warehouse: {},
            items: [],
            orders: [],
        }
    },
    methods: {
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
                    this.items = res.data.warehouse ? res.data.warehouse.items : []
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });

            axios.
                get(process.env.baseUrl + '/api/warehouse/' + this.warehouseId + '/orders', {
                    headers: {
                        'Content-Type': 'application/json',
                        'username': this.$store.state.user.username,
                    }
                })
                .then((res) => {
                    console.log("Server response: ", res);
                    
                    this.orders = res.data.orders
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
        },
        deleteItem: function (warehouseId, itemId, i) {
            axios.
                delete(
                    process.env.baseUrl + '/api/warehouse/' + warehouseId + '/items/' + itemId, {
                    headers: {
                        'Content-Type': 'application/json',
                        'username': this.$store.state.user.username,
                    }
                })
                .then((res) => {
                    console.log("Server response: ", res);
                    
                    this.items.splice(i, 1)
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
        }
    },
    mounted: function () {
        this.getWarehouse()
        console.log(this.warehouse)
        console.log(process.env.baseUrl)
    }
};
</script>

<style lang="sass" scoped>

</style>
