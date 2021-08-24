<template>
  <div>
    <div>
      <div class="flex justify-center space-y-8 w-full pt-32">
        Success!
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
import { store } from '../store.js';
import { reactive, ref } from 'vue'
import axios from 'axios';


export default {
  name: 'Slack2',
  props: {
      msg: String
  },
  components: {
  },
  created() {
  },
  mounted() {
    this.emitter.on('user-login', d => {
      console.log('user-login', d);
    });
    // this.checkUrl();
  },
  data() {
      return {
        store: store,
        storeState: store.state,
      }
  },
  methods: {
    login() {
      this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
    },
    logout() {
      this.$router.push({ name: 'Logout', query: { goto: 'Landing' }})
    },
    getApiUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://127.0.0.1:5000/${endpoint}`
      return `https://pulse-backend.onrender.com/${endpoint}`
    },
    getAppUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://localhost:8080/${endpoint}`
      return `https://trypaper.io/${endpoint}`
    }, 
    checkUrl() {
      console.log('checkUrl...')
      if (this.$route.query.code) {
        console.log('checkUrl code...')
        this.storeState.slackCode = this.$route.query.code
        if (this.storeState.isLoggedIn) {
          // send to backend secret store
          const path = this.getApiUrl('update_secret')
          let d = {
            user: this.storeState.user, 
            slackCode: this.storeState.slackCode,
            type: 'slack'
            }
          axios.post(path, d)
            .then((res) => {
              this.updatingStripeKey = false
              console.log('got update_secret: ', res.data)
            })
            .catch((error) => {
              console.error(error)
            })
        } else {
          this.$router.push({ name: 'Login', query: { goto: 'Landing', slackCode:  this.storeState.slackCode}})
        }
      }
    }
  },
}
/* eslint-disable no-unused-vars */
</script>

