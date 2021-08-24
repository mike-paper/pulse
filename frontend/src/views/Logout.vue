<template>
<!--
  This example requires Tailwind CSS v2.0+ 
  
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ]
  }
  ```
-->
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
import { store } from '../store.js';

const magic = new Magic('pk_live_7F06D4CDC50CBA64');
// magic.preload;

export default {
  name: 'Logout',
  props: {
      msg: String
  },
  created() {
    this.handleLogout()
  },
  methods: {
    countryCodeEmoji(cc) {
      if (!cc) return ''
      if (!cc.geo) return ''
      if (!cc.geo.countryCode) return ''
      cc = cc.geo.countryCode
      const CC_REGEX = /^[a-z]{2}$/i;
      const OFFSET = 127397;
      if (!CC_REGEX.test(cc)) {
        const type = typeof cc;
        throw new TypeError(
          `cc argument must be an ISO 3166-1 alpha-2 string, but got '${
            type === 'string' ? cc : type
          }' instead.`,
        );
      }
      const chars = [...cc.toUpperCase()].map(c => c.charCodeAt() + OFFSET);
      return String.fromCodePoint(...chars);
    },
    async handleLogout() {
      console.log('handleLogout1...')
      await magic.user.logout();
      console.log('handleLogout2...')
      this.storeState.isLoggedIn = false
      this.storeState.user = {}
      this.$router.push({ name: 'Login'})
      // this.render();
    },
    getApiUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://127.0.0.1:5000/${endpoint}`
      return `https://pulse-backend.onrender.com/${endpoint}`
    },
  },
  data() {
      return {
        store: store,
        storeState: store.state,
        checkedIfLoggedIn: false
      }
  }
}
/* eslint-enable no-unused-vars */

</script>

