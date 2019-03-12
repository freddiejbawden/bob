<template>
    <div>

        <section class="section pt60 pt30t pb0">
            <div class="container has-text-centered">
                <h1 class="is-inline-block is-relative mb25">
                    All orders in 
                    <label class="transparent-label" @click="triggerSelect()"  v-if="selectedWarehouse">
                        {{ selectedWarehouse ? selectedWarehouse.name : 'loading...' }} <i class="mdi mdi-chevron-down"></i>
                    </label>
                    <select 
                        class="transparent-select" 
                        name="warehouse" 
                        v-model="selectedWarehouse"
                        @change="getOrders(selectedWarehouse._id)"
                        v-if="selectedWarehouse">
                        <option :value="warehouse" v-for="warehouse in warehouses" :key="warehouse._id" :selected="warehouse._id == selectedWarehouse._id">
                            {{ warehouse.name }}
                        </option>
                    </select>
                </h1>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="box is-full-width">
                    <table class="table is-full-width" v-if="selectedWarehouse && orders.length > 0">
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
                    <h3 class="has-text-centered m30-0" v-else-if="!selectedWarehouse">
                        You haven't added any warehouses.
                    </h3>
                    <h3 class="has-text-centered m30-0" v-else>
                        No orders have been placed.
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
            warehouses: [],
            selectedWarehouse: null,
            orders: []
        }
    },
    methods: {
        triggerSelect: function () {
            this.$refs.select.click()
        },
        filterWarehouses: function (warehouses) {
            return warehouses.filter((warehouse) => {
                return warehouse.merchantId == this.$store.state.user._id
            })
        },
        getWarehouses () {
            axios.
                get(process.env.baseUrl + '/api/warehouse/', {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then((res) => {
                    console.log("Server response: ", res);

                    // this.warehouses = res.data.warehouses
                    this.warehouses = this.filterWarehouses(res.data.warehouses)
                    this.selectedWarehouse = this.warehouses[0]
                    this.getOrders(this.selectedWarehouse._id)
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
        },
        getOrders: function (id) {
            axios.
                get(process.env.baseUrl + '/api/warehouse/' + id + '/orders', {
                    headers: {
                        'Content-Type': 'application/json',
                        'username': this.$store.state.user.username
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
    },
    mounted: function () {
        this.getWarehouses()
    }
};
</script>

<style lang="sass" scoped>

    // .box
    //     width: 32rem    

</style>
