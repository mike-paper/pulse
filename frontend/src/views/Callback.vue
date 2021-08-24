<template>
<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
  <div v-if="true" class="flex justify-center max-w-md space-y-8 w-full">
    <svg class="animate-spin -ml-1 mr-3 h-20 w-20 text-gray-100" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  </div>
</div>
</template>

<script>
/* eslint-disable no-unused-vars */
import axios from 'axios';
import { Magic } from 'magic-sdk';
import { OAuthExtension } from '@magic-ext/oauth';

import { store } from '../store.js';

const magic = new Magic('pk_live_7F06D4CDC50CBA64', {
  extensions: [new OAuthExtension()],
});

export default {
  name: 'Callback',
  props: {
      msg: String
  },
  created() {
    this.handleCallback()
    // this.getCallback()
  },
  methods: {
    async handleCallback() {
      const oauthResult = await magic.oauth.getRedirectResult();
      // debugger
      this.storeState.isLoggedIn = await magic.user.isLoggedIn();
      /* Show login form if user is not logged in */
      if (this.storeState.isLoggedIn) {
        /* Get user metadata including email */
        const userMetadata = await magic.user.getMetadata();
        this.storeState.user = userMetadata
        this.storeState.user.oauth = oauthResult
        console.log('logged in...', userMetadata.email)
        const idToken = await magic.user.getIdToken();
        this.loginUser(userMetadata, idToken)
        if (this.$route.query.goto) {
          this.$router.push({ name: this.$route.query.goto, params: { user: userMetadata }})
        } else {
          this.$router.push({ name: 'Landing', params: { user: userMetadata }})
        }
        this.checkedIfLoggedIn = true
      } else {
        this.checkedIfLoggedIn = true
      }
    },
    getApiUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://127.0.0.1:5000/${endpoint}`
      return `https://pulse-backend.onrender.com/${endpoint}`
    },
    getAppUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://localhost:8080/${endpoint}`
      return `https://trypaper.io/${endpoint}`
    },
    loginUser(userMetadata, idToken) {
      this.gotFunders = false
      userMetadata.idToken = idToken
      const path = this.getApiUrl('login')
      axios.post(path, userMetadata)
        .then((res) => {
          console.log('did login: ', res.data)
          if (this.$route.query.goto) {
            this.$router.push({ name: this.$route.query.goto, params: { user: userMetadata }})
          } else if (res.data.new) {
            this.$router.push({ name: 'Settings', params: { user: userMetadata }})
          } else {
            this.$router.push({ name: 'Metrics', params: { user: userMetadata }})
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    goHome() {
      this.$router.push({ name: 'Landing', params: { userId: 123 }})
    },
  },
  computed: {
  },
  watch: {
  },
  data() {
      return {
        store: store,
        storeState: store.state,
        checkedIfLoggedIn: false,
        email: '',
      }
  }
}
/* eslint-enable no-unused-vars */

</script>

