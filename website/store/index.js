export const strict = false

export const state = () => ({
    counter: 0,
    user: null
})
  
export const mutations = {
    increment (state) {
        state.counter++
    },
    setUser (state, payload) {
        state.user = payload
    },
    unsetUser (state) {
        state.user = null
    },
    getUserFromSession (state) {
        state.user = window.$nuxt.$cookies.get('user')
    }

    // signUpWithEmail ({commit}) {
    //     return new Promise((resolve, reject) => {
            
    //     })
    // }
}

export const actions = {

}