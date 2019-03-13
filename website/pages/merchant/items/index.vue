<template>
    <div>

        <section class="section pt60 pt30t pb0">
            <div class="container has-text-centered">
                <h1 class="is-inline-block is-relative mb25">
                    All items in 
                    <label class="transparent-label" @click="triggerSelect()" v-if="selectedWarehouse">
                        {{ selectedWarehouse ? selectedWarehouse.name : 'loading...' }} <i class="mdi mdi-chevron-down"></i>
                    </label>
                    <select 
                        class="transparent-select" 
                        name="warehouse" 
                        v-model="selectedWarehouse"
                        @change="getItems(selectedWarehouse._id)"
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
                <div class="is-flex justify-end">
                    <nuxt-link 
                        :to="'/merchant/items/create/' + (selectedWarehouse ? selectedWarehouse._id : '')" 
                        class="button is-link mb15"
                        v-if="selectedWarehouse">
                        <span>Add an item to this warehouse</span>
                    </nuxt-link>
                </div>

                <div class="box is-full-width">
                    <table class="table is-full-width" v-if="selectedWarehouse && items.length > 0">
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
                                    <nuxt-link :to="'/merchant/items/edit/' + selectedWarehouse._id + '_' + item._id" class="has-text-success">
                                        <i class="mdi mdi-pencil"></i>
                                        Edit
                                    </nuxt-link>
                                </td>
                                <td>
                                    <a href="javascript:;" class="has-text-danger" @click="deleteItem(selectedWarehouse._id, item._id, i)">
                                        <i class="mdi mdi-delete"></i>
                                        Delete
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <h3 class="has-text-centered m30-0" v-else-if="!selectedWarehouse">
                        You haven't added any warehouses.
                    </h3>
                    <h3 class="has-text-centered m30-0" v-else>
                        You haven't added any items.
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
            items: []
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
                    this.getItems(this.selectedWarehouse._id)

                    // if (res.status == 200) {
                    //     this.$router.push('/merchant/orders').go(1)
                    // }
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
        },
        getItems: function (id) {
            axios.
                get(process.env.baseUrl + '/api/warehouse/' + id, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then((res) => {
                    console.log("Server response: ", res);
                    
                    this.items = res.data.warehouse ? res.data.warehouse.items : []
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
        this.getWarehouses()
    }
};
</script>

<style lang="sass" scoped>

    // .box
    //     width: 32rem    

</style>
