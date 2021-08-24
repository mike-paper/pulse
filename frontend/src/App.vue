<template>
  <div class="bg-gray-900" id="app">
    <div class="h-screen flex bg-gray-50 overflow-y-scroll">
      <TransitionRoot as="template" :show="mobileMenuOpen">
        <Dialog as="div" static class="fixed inset-0 flex z-40 md:hidden" @close="mobileMenuOpen = false" :open="mobileMenuOpen">
          <TransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
            <DialogOverlay class="fixed inset-0 bg-gray-600 bg-opacity-75" />
          </TransitionChild>
          <TransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="-translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="-translate-x-full">
            <div class="relative flex-1 flex flex-col max-w-xs w-full bg-white focus:outline-none">
              <TransitionChild as="template" enter="ease-in-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-300" leave-from="opacity-100" leave-to="opacity-0">
                <div class="absolute top-0 right-0 -mr-12 pt-4">
                  <button type="button" class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white" @click="mobileMenuOpen = false">
                    <span class="sr-only">Close sidebar</span>
                    <XIcon class="h-6 w-6 text-white" aria-hidden="true" />
                  </button>
                </div>
              </TransitionChild>
              <div class="pt-5 pb-4">
                <div class="flex-shrink-0 flex items-center px-4">
                  <img class="h-8 w-auto" src="/paper-white-logo.png" alt="Logo">
                </div>
                <nav aria-label="Sidebar" class="mt-5">
                  <div class="px-2 space-y-1">
                    <div @click="navClick(item)" v-for="item in navigation.filter(nav => true === storeState.user.hasStripe)" :key="item.name" class="group p-2 rounded-md flex items-center text-base font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900">
                      <component :is="item.icon" class="mr-4 h-6 w-6 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                      {{ item.name }}
                    </div>
                  </div>
                </nav>
              </div>
              <!-- <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
                <a href="#" class="flex-shrink-0 group block">
                  <div class="flex items-center">
                    <div>
                      <img class="inline-block h-10 w-10 rounded-full" :src="user.imageUrl" alt="" />
                    </div>
                    <div class="ml-3">
                      <p class="text-base font-medium text-gray-700 group-hover:text-gray-900">
                        {{ user.name }}
                      </p>
                      <p class="text-sm font-medium text-gray-500 group-hover:text-gray-700">
                        Account Settings
                      </p>
                    </div>
                  </div>
                </a>
              </div> -->
              <Menu as="div" class="relative inline-block text-left">
                <MenuButton 
                  class="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600"
                >
                  <span class="sr-only">Open user menu</span>
                  <!-- <img class="h-8 w-8 rounded-full" :src="user.imageUrl" alt="" /> -->
                  <!-- <component :is="UserIcon" class="h-6 w-6" aria-hidden="true" /> -->
                  <UserIcon 
                    class="h-6 w-6 cursor-pointer text-white"
                  />
                </MenuButton>
                <!-- mobile -->
                <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                  <MenuItems class="origin-top-right absolute z-50 left-0 top-0 -mt-32 mb-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div v-if="storeState.user && storeState.user.email" class="py-1">
                      <MenuItem>
                        <a class="border-b block px-4 py-2 text-sm text-gray-700">
                          {{storeState.user.email}}
                        </a>
                      </MenuItem>
                      <MenuItem v-slot="{ active }">
                        <a @click="goToSettings" class="cursor-pointer" :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">
                          Your Profile
                        </a>
                      </MenuItem>
                      <MenuItem v-slot="{ active }">
                        <a @click="handleLogout" class="cursor-pointer" :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">
                          Sign Out
                        </a>
                      </MenuItem>
                    </div>
                    <div v-else>
                      <MenuItem v-slot="{ active }">
                        <a @click="goToLogin" class="cursor-pointer" :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">
                          Sign In
                        </a>
                      </MenuItem>
                    </div>
                  </MenuItems>
                </transition>
              </Menu>
            </div>
          </TransitionChild>
          <div class="flex-shrink-0 w-14" aria-hidden="true">
            <!-- Force sidebar to shrink to fit close icon -->
          </div>
        </Dialog>
      </TransitionRoot>

      <!-- Static sidebar for desktop -->
      <div 
        class="hidden md:flex md:flex-shrink-0"
        :class="{'md:hidden': !storeState.isLoggedIn}"
      >
        <div class="flex flex-col w-20">
          <div class="flex flex-col h-0 flex-1 bg-gray-900">
            <div class="flex-1 flex flex-col">
              <div class="flex-shrink-0 bg-gray-900 py-4 flex items-center justify-center">
                <img class="h-8 w-auto" src="/paper-white-logo.png" alt="Logo">
              </div>
              <nav aria-label="Sidebar" class="py-6 flex flex-col items-center space-y-3">
                <div 
                  @click="navClick(item)" 
                  v-for="item in navigation.filter(nav => ((true === storeState.user.hasStripe) && (true === storeState.user.hasMrrFacts)))" 
                  :key="item.name" 
                  class="cursor-pointer flex items-center p-4 rounded-lg text-gray-100 hover:bg-gray-700"
                >
                  <Popper class="inline" hover placement="right">
                    <component :is="item.icon" class="h-6 w-6" aria-hidden="true" />
                    <template #content>
                      <div class="bg-gray-700 text-gray-100 ml-4 px-3 py-2 rounded">{{ item.name }}</div>
                      <!-- <span class="sr-only"></span> -->
                    </template>
                  </Popper>
                </div>
              </nav>
            </div>
            <Menu as="div" class="relative flex flex-col items-center mb-8">
              <MenuButton 
                class="rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600"
              >
                <span class="sr-only">Open user menu</span>
                <div v-if="getPic()">
                  <img class="h-8 w-8 rounded-full" :src="getPic()" alt="" />
                </div>
                <!-- <img class="h-8 w-8 rounded-full" :src="user.imageUrl" alt="" /> -->
                <UserIcon 
                  v-else
                  class="h-6 w-6 cursor-pointer text-gray-100"
                  aria-hidden="true" 
                />
              </MenuButton>
              <!-- desktop -->
              <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                <MenuItems class="origin-bottom-left absolute z-50 left-0 top-0 -mt-32 w-56 rounded-sm shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
                  <div v-if="storeState.user && storeState.user.email" class="py-1">
                    <MenuItem>
                      <a class="border-b block px-4 py-2 text-sm text-gray-700">
                        {{storeState.user.email}}
                      </a>
                    </MenuItem>
                    <MenuItem v-slot="{ active }">
                      <a @click="goToSettings" class="cursor-pointer" :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">
                        Your Profile
                      </a>
                    </MenuItem>
                    <MenuItem v-slot="{ active }">
                      <a @click="handleLogout" class="cursor-pointer" :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">
                        Sign Out
                      </a>
                    </MenuItem>
                  </div>
                  <div v-else>
                    <MenuItem v-slot="{ active }">
                      <a @click="goToLogin" class="cursor-pointer" :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">
                        Sign In
                      </a>
                    </MenuItem>
                  </div>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>
      </div>

      <div class="divide-gray-800 divide-x flex-1 min-w-0 flex flex-col overflow-y-scroll">
        <!-- Mobile top navigation -->
        <div class="md:hidden">
          <div class="bg-gray-900 py-2 px-4 flex items-center justify-between sm:px-6 md:px-8">
            <div>
              <img class="h-8 w-auto" src="/paper-logo.png" alt="Logo">
            </div>
            <div>
              <button type="button" class="-mr-3 h-12 w-12 inline-flex items-center justify-center bg-gray-900 rounded-md text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white" @click="mobileMenuOpen = true">
                <span class="sr-only">Open sidebar</span>
                <MenuIcon class="h-6 w-6" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>

        <main class="flex-1 flex overflow-y-scroll">
          <div class="flex-1 flex xl:overflow-y-scroll">
            <!-- Primary column -->
            <section 
              v-if="storeState.checkedLogin"
              aria-labelledby="primary-heading" 
              class="min-w-0 flex-1 h-full flex flex-col overflow-y-scroll md:order-last"
            >
              <!-- <h1 id="primary-heading" class="sr-only">Account</h1> -->
              <router-view/>
            </section>
            <section 
              v-else
              aria-labelledby="primary-heading" 
              class="min-w-0 flex-1 h-full flex flex-col overflow-y-scroll md:order-last"
            >
              <div >
                <div class="flex justify-center space-y-8 w-full pt-32">
                  <svg class="animate-spin -ml-1 mr-3 h-20 w-20 text-gray-100" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
                <div class="flex justify-center space-y-8 w-full pt-8">
                  <div class="relative">
                    <blockquote class="mt-10">
                      <div class="max-w-3xl mx-auto text-center text-2xl leading-9 font-medium text-gray-500">
                        <p>
                          &ldquo;Everyone has a plan 'till they get punched in the mouth.&rdquo;
                        </p>
                      </div>
                      <footer class="mt-8">
                        <div class="md:flex md:items-center md:justify-center">
                          <!-- <div class="md:flex-shrink-0">
                            <img class="mx-auto h-10 w-10 rounded-full" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Mike_Tyson_2019_by_Glenn_Francis.jpg/1200px-Mike_Tyson_2019_by_Glenn_Francis.jpg" alt="" />
                          </div> -->
                          <div class="mt-3 text-center md:mt-0 md:flex md:items-center">
                            <div class="text-base font-medium text-gray-700">Mike Tyson</div>

                            <svg class="hidden md:block mx-1 h-5 w-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M11 0h3L9 20H6l5-20z" />
                            </svg>

                            <div class="text-base font-medium text-gray-700">Professional Boxer</div>
                          </div>
                        </div>
                      </footer>
                    </blockquote>
                  </div>
                </div>
              </div>
            </section>

            <!-- Secondary column (hidden on smaller screens) -->
            <!-- <aside class="hidden md:block md:flex-shrink-0 md:order-first">
              <div class="h-full relative flex flex-col w-96 border-r border-gray-200 bg-white">
                
              </div>
            </aside> -->
          </div>
        </main>
      </div>
    </div>
    <!-- ALERTS / NOTIFICATION -->
    <div>
      <div aria-live="assertive" class="fixed inset-0 flex items-end px-4 py-6 pointer-events-none sm:p-6 sm:items-start">
        <div class="w-full flex flex-col items-center space-y-4 sm:items-end">
          <!-- Notification panel, dynamically insert this into the live region when it needs to be displayed -->
          <transition enter-active-class="transform ease-out duration-300 transition" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
            <div v-if="storeState.msg.show" class="max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 overflow-hidden">
              <div class="p-4">
                <div class="flex items-start">
                  <div v-if="storeState.msg.type === 'error'" class="flex-shrink-0">
                    <ExclamationCircleIcon class="h-6 w-6 text-red-400" aria-hidden="true" />
                  </div>
                  <div v-else class="flex-shrink-0">
                    <CheckCircleIcon class="h-6 w-6 text-green-400" aria-hidden="true" />
                  </div>
                  <div class="ml-3 w-0 flex-1 pt-0.5">
                    <p class="text-sm font-medium text-gray-900">
                      {{storeState.msg.primary}}
                    </p>
                    <p v-html="storeState.msg.secondary" class="mt-1 text-sm text-gray-500">
                    </p>
                  </div>
                  <div class="ml-4 flex-shrink-0 flex">
                    <button @click="storeState.msg.show = false" class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                      <span class="sr-only">Close</span>
                      <XIcon class="h-5 w-5" aria-hidden="true" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { store } from './store.js';
import { Magic } from 'magic-sdk';
import { ref } from 'vue'
import Popper from "vue3-popper";

import { 
  Dialog, 
  DialogOverlay, 
  TransitionChild, 
  TransitionRoot,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  } from '@headlessui/vue'
import { 
  CheckCircleIcon,
  ExclamationCircleIcon,
  BookmarkAltIcon, 
  FireIcon, 
  HomeIcon, 
  InboxIcon, 
  MenuIcon, 
  UserIcon, 
  UserGroupIcon,
  CashIcon,
  CogIcon,
  XIcon, 
  ChartBarIcon } from '@heroicons/vue/outline'

const magic = new Magic(process.env.VUE_APP_PAPER_MAGIC_API_KEY);

export default {
  name: 'App',
  props: {
      msg: String
  },
  components: {
    Popper,
    CheckCircleIcon,
    ExclamationCircleIcon,
    Dialog,
    DialogOverlay,
    TransitionChild,
    TransitionRoot,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    MenuIcon,
    XIcon,
    UserIcon,
  },
  mounted() {
    this.checkIfLoggedIn()
    this.emitter.on('check-login', d => {
      this.checkIfLoggedIn()
    });
  },
  computed: {
  },
  data() {
      return {
        store: store,
        storeState: store.state,
        mobileMenuOpen: false,
        user: {
          name: 'Emily Selman',
          imageUrl:
            'https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
        },
        navigation: [
          { name: 'Home', href: 'Metrics', icon: HomeIcon },
          { name: 'Analyze', href: 'Analyze', icon: ChartBarIcon },
          { name: 'Settings', href: 'Settings', icon: CogIcon },
          { name: 'Team', href: 'Team', icon: UserGroupIcon },
          { name: 'Capital', href: 'Capital', icon: CashIcon },
        ]
      }
  },
  methods: {
    async handleLogout() {
      this.$router.push({ name: 'Logout'})
    },
    getRecentJobs() {
      this.storeState.gotDbt = false
      const path = this.getApiUrl('get_recent_jobs')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got get_recent_jobs: ', res.data)
          this.storeState.jobStatuses = res.data.jobs
          // this.metricData = reactive(res.data)
          // this.createCharts()
          // this.createCustomerTable()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getDbt() {
      this.storeState.gotDbt = false
      const path = this.getApiUrl('get_dbt')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got get_dbt: ', res.data)
          this.storeState.gotDbt = true
          this.storeState.dbt = res.data.data
          // this.metricData = reactive(res.data)
          // this.createCharts()
          // this.createCustomerTable()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getPic() {
      if (this.storeState.user.oauth) {
        try {
          return this.storeState.user.oauth.oauth.userInfo.picture  
        } catch (error) {
          return false
        }
      }
    },
    goToSettings() {
      this.$router.push({ name: 'Settings'})
    },
    goToLogin() {
      this.$router.push({ name: 'Login'})
    },
    navClick(nav) {
      if (nav.href == 'Capital') {
        window.open('https://trypaper.io?ref=pulse', '_blank').focus();
        return
      }
      console.log('nav: ', nav)
      this.$router.push({ name: nav.href})
    },
    getApiUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://127.0.0.1:5000/${endpoint}`
      return `https://pulse-backend.onrender.com/${endpoint}`
    },
    getUserData() {
      const path = this.getApiUrl('login')
      let d = this.storeState.user
      axios.post(path, d)
        .then((res) => {
          console.log('got getUserData: ', res.data)
          if (res.data.user) {
            this.storeState.user = res.data.user
            this.storeState.user.ok = true
            if (!res.data.user.hasStripe || !res.data.user.hasMrrFacts) {
              console.log('user doesnt have stripe...')
              this.$router.push({ name: 'Settings'})
            } 
          }
          this.storeState.gotUserData = true
          this.emitter.emit('user-data');
          
        })
        .catch((error) => {
          console.error(error)
          this.storeState.gotUserData = true
        })
    },
    checkUrl() {
      console.log('checkUrl...')
      if (this.$route.query.code) {
        console.log('checkUrl code...')
        if (this.storeState.isLoggedIn) {
          // send to backend secret store
          const path = this.getApiUrl('update_secret')
          let secretType = this.$route.name.toLowerCase().replace('2', '')
          let d = {
            user: this.storeState.user, 
            code: this.$route.query.code,
            type: secretType
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
          // this.$router.push({ name: 'Login', query: { goto: 'Landing', slackCode:  this.storeState.slackCode}})
        }
      }
    },
    getMetrics() {
      console.log('getMetrics...')
      this.storeState.gotMetrics = false
      const path = this.getApiUrl('get_metrics')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got get_metrics: ', res.data)
          this.storeState.gotMetrics = true
          // this.$forceUpdate()
          // this.storeState.metricData = reactive(res.data)
          this.storeState.metricData = res.data
          this.emitter.emit('got-metrics');
          
          // this.createCharts()
          // var self = this
          // setTimeout(() => self.createCustomerTable(), 0);
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getEvents() {
      console.log('getEvents...')
      this.storeState.gotEvents = false
      const path = this.getApiUrl('get_events')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got get_events: ', res.data)
          this.storeState.gotEvents = true
          // this.$forceUpdate()
          // this.storeState.metricData = reactive(res.data)
          this.storeState.events = res.data
          this.emitter.emit('got-events');
          
          // this.createCharts()
          // var self = this
          // setTimeout(() => self.createCustomerTable(), 0);
        })
        .catch((error) => {
          console.error(error)
        })
    },
    async checkIfLoggedIn() {
      console.log('checkIfLoggedIn1...', this.storeState.isLoggedIn)
      setTimeout(() => this.storeState.gotUserData = true, 2000);
      setTimeout(() => this.storeState.checkedLogin = true, 2000);
      if (!this.storeState.isLoggedIn) {
        this.storeState.isLoggedIn = await magic.user.isLoggedIn()
        console.log('checkIfLoggedIn2...', this.storeState.isLoggedIn)
      }
      this.storeState.checkedLogin = true
      if (this.storeState.isLoggedIn) {
        if (!this.storeState.user || (this.storeState.user && !this.storeState.user.ok)) {
          this.storeState.user = await magic.user.getMetadata();
          this.storeState.user.idToken = await magic.user.getIdToken();
          this.getUserData()
        }
        this.getDbt()
        this.getRecentJobs()
        this.checkUrl()
        this.getMetrics()
        this.getEvents()
      } else {
        this.storeState.gotUserData = true
        this.$router.push({ name: 'Login'})
      }
      console.log('checkIfLoggedIn3...', this.storeState.isLoggedIn)
      this.emitter.emit('user-login');
    },
  }
}
</script>

<style>
  @import './assets/styles/styles.css';
</style>
