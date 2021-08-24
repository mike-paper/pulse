<template>
  <div>
    <div v-if="!storeState.gotUserData || !storeState.user.ok">
      <div class="flex justify-center space-y-8 w-full pt-32">
        <svg class="animate-spin -ml-1 mr-3 h-20 w-20 text-gray-100" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    </div>
    <div v-else>
      <div class="pt-8 pl-8 mr-8">
        <div class="text-3xl font-extrabold text-gray-100">
          Settings
        </div>
        <div v-if="storeState.user.hasStripe" class="pt-8">
          <div class="font-medium leading-6 text-gray-100 text-lg">
            Notifications
          </div>
          <p class="max-w-2xl text-sm text-gray-500">
            Get notifications about your companies performance pushed to your preferred channel
          </p>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <div class="col-span-1">

            </div>
            <div class="col-span-1 text-sm font-medium text-gray-500">
              Slack
            </div>
            <div class="col-span-1 text-sm font-medium text-gray-500">
              Email
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <div class="text-sm font-medium text-gray-500">
              Alerts (New Subscribers, Churn, etc.)
            </div>
            <div>
              <Switch v-model="storeState.user.settings.notifications.alerts.slack" :class="[storeState.user.settings.notifications.alerts.slack ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500']">
                <span :class="[storeState.user.settings.notifications.alerts.slack ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.user.settings.notifications.alerts.slack ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.user.settings.notifications.alerts.slack ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-blue-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
            <div>
              <Switch v-model="storeState.user.settings.notifications.alerts.email" :class="[storeState.user.settings.notifications.alerts.email ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500']">
                <span :class="[storeState.user.settings.notifications.alerts.email ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.user.settings.notifications.alerts.email ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.user.settings.notifications.alerts.email ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-blue-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <div class="text-sm font-medium text-gray-500">
              Weekly
            </div>
            <div>
              <Switch v-model="storeState.user.settings.notifications.weekly.slack" :class="[storeState.user.settings.notifications.weekly.slack ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500']">
                <span :class="[storeState.user.settings.notifications.weekly.slack ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.user.settings.notifications.weekly.slack ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.user.settings.notifications.weekly.slack ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-blue-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
            <div>
              <Switch v-model="storeState.user.settings.notifications.weekly.email" :class="[storeState.user.settings.notifications.weekly.email ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500']">
                <span :class="[storeState.user.settings.notifications.weekly.email ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.user.settings.notifications.weekly.email ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.user.settings.notifications.weekly.email ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-blue-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <div class="text-sm font-medium text-gray-500">
              Monthly
            </div>
            <div>
              <Switch v-model="storeState.user.settings.notifications.monthly.slack" :class="[storeState.user.settings.notifications.monthly.slack ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500']">
                <span :class="[storeState.user.settings.notifications.monthly.slack ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.user.settings.notifications.monthly.slack ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.user.settings.notifications.monthly.slack ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-blue-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
            <div>
              <Switch v-model="storeState.user.settings.notifications.monthly.email" :class="[storeState.user.settings.notifications.monthly.email ? 'bg-blue-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500']">
                <span :class="[storeState.user.settings.notifications.monthly.email ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.user.settings.notifications.monthly.email ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.user.settings.notifications.monthly.email ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-blue-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
          </div>
        </div>
        <div class="pt-8">
          <div class="font-medium leading-6 text-gray-100 text-lg">
            Stripe
          </div>
          <p class="max-w-2xl text-sm text-gray-500">
            Import your Stripe data by 
              <a 
                href="https://dashboard.stripe.com/apikeys/create"
                class="font-medium text-blue-600 hover:text-blue-500"
                target="_blank"
              >
                creating a key here.
              </a>
            Give the key a name and the "Read" permission for "All core resources" and "All Billing resources".
          </p>
          <div 
            class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4"
          >
            <div class="col-span-6 sm:col-span-2">
              <label for="stripe_api_key" class="block text-sm font-medium text-gray-100">API Key</label>
              <input 
                type="password" 
                v-model="stripeApiKey"
                ref="stripe_api_key" 
                name="stripe_api_key" 
                id="stripe_api_key" 
                autocomplete="password" 
                class="mt-1 block w-full border border-gray-900 text-gray-100 bg-gray-800 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-gray-900 focus:border-gray-200 sm:text-sm" 
              />
            </div>
            <div class="col-span-6 sm:col-span-2">
              <button 
                @click="updateStripeApiKey"
                :disabled="updatingStripeKey"
                class="py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 shadow-sm hover:bg-blue-500 focus:outline-none focus:shadow-outline-blue focus:bg-blue-500 active:bg-blue-600 transition duration-150 ease-in-out"
                :class="{
                  'opacity-50': updatingStripeKey, 
                  'cursor-not-allowed': updatingStripeKey
                  }"
              >
                Update API Key
              </button>
              <div v-if="!storeState.user.hasStripe" class="pt-8">
                <img src="/stripeApiKeyCreation.png" alt="">
              </div>
            </div>
          </div>
          
        </div>
        <div v-if="storeState.user.hasStripe" class="pt-8">
          <div class="font-medium leading-6 text-gray-100 text-lg">
            Data
          </div>
          <p class="max-w-2xl text-sm text-gray-500">
            View and edit your data model and syncing schedule
          </p>
          <div class="pt-8">
            <div class="font-medium leading-6 text-gray-100">
              Raw Objects
            </div>
            <div class="mt-4 shadow overflow-hidden rounded">
              <table class="border border-gray-700 min-w-full">
                <thead class="bg-gray-800 border border-gray-700">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rows
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-700 bg-gray-800">
                  <tr
                    v-for="(job, jobId, jobIndex) in storeState.jobStatuses"
                    :key="jobIndex"
                    class="bg-gray-800 text-gray-100"
                  >
                    <template v-if="job.count">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <div class="ml-0">
                            <div class="text-sm font-medium text-gray-100">
                              {{ job.obj }}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span v-if="job.status === 'running'" class="px-2 -ml-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-600 text-yellow-200">
                          {{ job.status }}
                        </span>
                        <span v-else class="px-2 -ml-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-700 text-green-200">
                          {{ job.status }}
                        </span>
                        <div v-if="job.status === 'running'" class="whitespace-nowrap text-sm text-gray-500">
                          ...
                        </div>
                        <div v-else class="whitespace-nowrap text-sm text-gray-500 inline ml-3">
                          Updated {{ job.rows }} rows 
                          <span v-if="job.updated_on">
                            {{ timeSince(job.updated_on*1000) }} ago
                          </span>
                          
                        </div>
                        
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ job.count }}
                      </td>
                    </template>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="pt-8">
            <div class="font-medium leading-6 text-gray-100">
              Modeled Data (dbt)
            </div>
            <div v-if="storeState.user.hasMrrFacts" class="mt-4 shadow overflow-hidden rounded">
              <table class="border border-gray-700 min-w-full">
                <thead class="bg-gray-800 border border-gray-700">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rows
                    </th>
                    <!-- <th scope="col" class="relative px-6 py-3">
                      <span class="sr-only">Edit</span>
                    </th> -->
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-700 bg-gray-800">
                  <tr
                    v-for="(table, tableIndex) in storeState.dbt.models"
                    :key="tableIndex"
                  >
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="ml-0">
                          <div class="text-sm font-medium text-gray-100">
                            {{ table.name }}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span v-if="runningDbt || !storeState.user.hasMrrFacts" class="px-2 -ml-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-600 text-yellow-200">
                        running
                      </span>
                      <span v-else class="px-2 -ml-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-700 text-green-200">
                        complete
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <a 
                        @click="viewTable(table)" 
                        class="text-blue-600 hover:text-blue-400 cursor-pointer"
                      >
                        <!-- <span v-if="table.count">
                          {{ table.count }}
                        </span> -->
                        <span v-if="storeState.user.hasMrrFacts">
                          View
                        </span>
                      </a>  
                      
                    </td>
                    <!-- <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <a 
                        @click="viewTable(table)" 
                        class="text-blue-600 hover:text-blue-400 cursor-pointer"
                      >
                        View
                      </a>
                    </td> -->
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="mt-4 shadow overflow-hidden rounded leading-6 text-gray-100">
              Completing initial sync, this may take a few minutes... Please refresh this page in 2 minutes.
            </div>
          </div>
          <div class="pt-8">
            <button 
              @click="runDbt"
              :disabled="runningDbt"
              class="py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 shadow-sm hover:bg-blue-500 focus:outline-none focus:shadow-outline-blue focus:bg-blue-500 active:bg-blue-600 transition duration-150 ease-in-out"
              :class="{
                'opacity-50': runningDbt, 
                'cursor-not-allowed': runningDbt
                }"
            >
              Run dbt
            </button>
          </div>
        </div>
        <div class="pt-8">
          <div class="font-medium leading-6 text-gray-100 text-lg">
            Sheets
          </div>
          <p class="max-w-2xl text-sm text-gray-500">
            Get your SaaS metrics in Google Sheets
              <a 
                href="https://github.com/mike-paper/pulse"
                class="font-medium text-blue-600 hover:text-blue-500"
                target="_blank"
              >
              (see here to set up)
              </a>
          </p>
          <div 
            class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4"
          >
            <div class="col-span-6 sm:col-span-2">
              <label for="spreadsheetId" class="block text-sm font-medium text-gray-100">
                Spreadsheet ID
                <Popper class="inline" hover placement="top">
                  <QuestionMarkCircleIcon class="mb-1 inline h-5 w-5 text-gray-500" aria-hidden="true" />
                  <template #content>
                    <div class="bg-gray-700 text-gray-100 px-3 py-2 rounded">This is the long ID in the Google Sheet URL
                      <img 
                        src="https://user-images.githubusercontent.com/74681824/129022058-0bab1143-6cef-4cc9-80c5-021e6b7733b7.png" alt=""
                        width="400"
                      >
                    </div>
                  </template>
                </Popper>
              </label>
              <input 
                v-model="storeState.user.settings.sheets.spreadsheetId"
                ref="spreadsheetId" 
                name="spreadsheetId" 
                id="spreadsheetId" 
                autocomplete="off" 
                class="mt-1 block w-full border text-gray-100 bg-gray-800 border-gray-900 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-gray-900 focus:border-gray-100 sm:text-sm" 
              />
            </div>
            <!-- <div class="col-span-6 sm:col-span-2">
              <label for="sheetName" class="block text-sm font-medium text-gray-100">Sheet Name</label>
              <input 
                v-model="storeState.user.settings.sheets.sheetName"
                ref="sheetName" 
                name="sheetName" 
                id="sheetName" 
                autocomplete="off" 
                class="mt-1 block w-full border text-gray-100 bg-gray-800 border-gray-900 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-gray-900 focus:border-gray-100 sm:text-sm" 
              />
            </div> -->
          </div>
          <div class="pt-4">
            <button 
              @click="saveSpreadsheetId"
              class="py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 shadow-sm hover:bg-blue-500 focus:outline-none focus:shadow-outline-blue focus:bg-blue-500 active:bg-blue-600 transition duration-150 ease-in-out"
            >
              Save
            </button>
          </div>
        </div>
        <div class="pt-8">
          <div class="font-medium leading-6 text-gray-100 text-lg">
            Slack
          </div>
          <p class="max-w-2xl text-sm text-gray-500">
            Get your SaaS metrics in Slack
          </p>
          <div 
            class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4"
          >
            <div class="col-span-6 sm:col-span-2">
              <a :href="slackAuthUrl" target="_blank">
                <img alt="Add to Slack" height="40" width="139" 
                  src="https://platform.slack-edge.com/img/add_to_slack.png" 
                  srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" />
                </a>
            </div>
          </div>
          <div 
            class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4"
          >
            <div class="col-span-6 sm:col-span-2">
              <div>
                <label for="price" class="block text-sm font-medium text-gray-100">Channel</label>
                <div class="mt-1 relative rounded-md shadow-sm">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <span class="text-gray-500 sm:text-sm">
                      #
                    </span>
                  </div>
                  <input 
                    type="text" 
                    name="slackChannel" 
                    autocomplete="off" 
                    v-model="storeState.user.settings.notifications.slackChannel"
                    id="slackChannel" 
                    class="pl-6 mt-1 block w-full border text-gray-100 bg-gray-800 border-gray-900 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-gray-900 focus:border-gray-100 sm:text-sm" 
                    placeholder="channel-name" 
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        
      </div>
      <div class="pt-16">
        <!-- jobStatuses: {{storeState.jobStatuses}} -->
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
/* eslint-disable no-empty */
/* eslint-disable vue/no-unused-components */
import { store } from '../store.js';
import { reactive, ref } from 'vue'
// import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import { Listbox, ListboxButton, ListboxLabel, ListboxOption, ListboxOptions, Switch } from '@headlessui/vue'
import axios from 'axios';
import * as vega from "vega";
// import embed from 'vega-embed';
// import * as embed from "vega-embed";
// embed = require('vega-embed')
import Mousetrap from 'mousetrap'
import SSF from 'ssf'
import { Grid, html } from "gridjs";
import Popper from "vue3-popper";

import { 
  ArrowSmUpIcon, 
  ArrowSmDownIcon, 
  SearchIcon, 
  XIcon, 
  CheckCircleIcon,
  ExclamationCircleIcon,
  QuestionMarkCircleIcon,
  PlayIcon,
  // ChartBarIcon,
  // PresentationChartLineIcon,
  // ViewGridIcon,
  CheckIcon,
  SelectorIcon,
  } from '@heroicons/vue/solid'

import { 
  ChartBarIcon,
  ViewGridIcon,
  PresentationChartLineIcon,
  PresentationChartBarIcon,
  } from '@heroicons/vue/outline'

export default {
  name: 'Metrics',
  props: {
      msg: String
  },
  components: {
    Popper,
    SearchIcon,
    XIcon,
    CheckCircleIcon,
    ExclamationCircleIcon,
    QuestionMarkCircleIcon,
    PlayIcon,
    ChartBarIcon,
    PresentationChartLineIcon,
    PresentationChartBarIcon,
    ViewGridIcon,
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOption,
    ListboxOptions,
    Switch,
    CheckIcon,
    SelectorIcon,
  },
  created() {
    this.setupMousetrap()
    var yourVlSpec = {
      $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
      description: 'A simple bar chart with embedded data.',
      data: {
        values: [
          {a: 'A', b: 28},
          {a: 'B', b: 55},
          {a: 'C', b: 43},
          {a: 'D', b: 91},
          {a: 'E', b: 81},
          {a: 'F', b: 53},
          {a: 'G', b: 19},
          {a: 'H', b: 87},
          {a: 'I', b: 52}
        ]
      },
      mark: 'bar',
      encoding: {
        x: {field: 'a', type: 'ordinal'},
        y: {field: 'b', type: 'quantitative'}
      }
    };
    window.analyzeGrid = new Grid({
      sort: true,
      search: false,
      pagination: {
        limit: 20
      },
      fixedHeader: true,
      height: '400px',
      // columns: ["Name", "Email", "Phone Number"],
      data: [],
      className: {
        td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-100 divide-y divide-gray-200',
        th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 tracking-wider',
        table: 'min-w-full divide-gray-200',
        tbody: 'bg-white '
      }
    })
    // window.vegaEmbed('#view', yourVlSpec);
  },
  mounted() {
    this.focusStripe()
    // this.startTyped()
  },
  data() {
      return {
        store: store,
        storeState: store.state,
        slackAuthUrl: 'https://slack.com/oauth/v2/authorize' + 
          '?client_id=2068350445268.2075584116417&scope=channels:read' + 
          ',chat:write.public,chat:write,files:write&user_scope=' +
          '&redirect_uri=https://pulse.trypaper.io/slack2',
        dbtLogs: [],
        stripeApiKey: '',
        sheetsCreds: '',
        runningDbt: false,
        updatingStripeKey: false,
        analysisChanged: false,
        searchTerm: '',
        searching: true,
        running: false,
        updatingField: false,
        gotMetrics: false,
        gotDbt: false,
        fieldInUpdate: {},
        tableFilters: {
          active: false,
        },
        vizOptions: {
          axis: [
            { id: 1, value: 'none', label: 'None' },
            { id: 2, value: 'x', label: 'X-Axis' },
            { id: 3, value: 'y', label: 'Y-Axis' },
          ]
        },
        metricData: [],
        stats: [
          { name: 'Total Subscribers', stat: '71,897', previousStat: '70,946', change: '12%', changeType: 'increase' },
          { name: 'Avg. Open Rate', stat: '58.16%', previousStat: '56.14%', change: '2.02%', changeType: 'increase' },
          { name: 'Avg. Click Rate', stat: '24.57%', previousStat: '28.62%', change: '4.05%', changeType: 'decrease' },
        ],
        vegaConfig: {
          "view": {
            "stroke": "transparent"
          },
          "arc": {"fill": "#fff"},
          "area": {"fill": "#fff"},
          "path": {"stroke": "#fff"},
          "rect": {"fill": "#fff"},
          "shape": {"stroke": "#fff"},
          "symbol": {"stroke": "#fff"},
          "circle": {"fill": "#fff"},
          "background": "transparent",
          "padding": {"top": 10, "right": 10, "bottom": 10, "left": 10},
          "style": {
            "guide-label": {"font": "Inter, sans-serif", "fontSize": 12},
            "guide-title": {"font": "Inter, sans-serif", "fontSize": 12},
            "group-title": {"font": "Inter, sans-serif", "fontSize": 12}
          },
          "title": {
            "font": "Inter, sans-serif",
            "fontSize": 14,
            "fontWeight": "bold",
            "dy": -3,
            "anchor": "start"
          },
          "axis": {
            "gridColor": "#ccc",
            "tickColor": "#fff",
            "domain": false,
            "grid": false
          }
        },
        vegaSpec: {
          "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
          "description": "MRR by Month",
          "width": "container",
          "mark": {
            "type": "line", 
            "tooltip": false, 
            "fill": null, 
            "stroke": "#010101",
            "point": {"color": "#010101"},
            },
          "encoding": {
              "x": {
                "field": "month_dt", 
                "timeUnit": "yearmonth", 
                "title": null,
                // "axis": {"tickCount": {"interval": "month", "step": 6}}
                "axis": {
                  "values": [
                    {"year": 2019, "month": "may", "date": 1},
                    {"year": 2021, "month": "may", "date": 1}
                    ]
                  }
                },
              "y": {
                "field": "mrr", 
                "aggregate": "sum", 
                "type": "quantitative",
                "title": null
                },
              "tooltip": [
                  {"field": "month_dt", "timeUnit": "yearmonth", "title": "Date"},
                  {
                    "field": "mrr", 
                    "aggregate": "sum", 
                    "type": "quantitative",
                    "format": "$,.0f",
                    "title": "MRR"
                  }
              ]
          },
          data: {values: []},
        },
      }
  },
  computed: {
    // dbtColumns() {
    //   let allCols = []
    //   for (let index = 0; index < this.storeState.dbt.models.length; index++) {
    //     const cols = this.storeState.dbt.models[index].columns;
    //     for (let i2 = 0; i2 < cols.length; i2++) {
    //       const col = cols[i2];
    //       col.modelName = this.storeState.dbt.models[index].name
    //       col.label = this.getLabel(col)
    //       allCols.push(col)
    //     }
    //   }
    //   return allCols
    // }
  },
  methods: {
    login() {
      this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
    },
    logout() {
      this.$router.push({ name: 'Logout', query: { goto: 'Landing' }})
    },
    saveSpreadsheetId() {
      this.updateSettings()
      let opts = {
        primary: 'Updated Spreadsheet ID',
        secondary: 'Syncs to Sheets occur hourly.',
        }
      this.showMsg(this, opts)
    },
    getLabel(column) {
      if (column.meta && column.meta.dimension && column.meta.dimension.label) {
        return column.meta.dimension.label
      }
      if (column && column.label) return column.label
      if (column.name) return column.name
      return 'no label'
    },
    viewTable(table) {
      this.$router.push({ name: 'Analyze', query: { table: table.name }})
    },
    timeSince(date) {
      var seconds = Math.floor((new Date() - date) / 1000);
      var interval = seconds / 31536000;
      if (interval > 1) {
        return Math.floor(interval) + " years";
      }
      interval = seconds / 2592000;
      if (interval > 1) {
        return Math.floor(interval) + " months";
      }
      interval = seconds / 86400;
      if (interval > 1) {
        return Math.floor(interval) + " days";
      }
      interval = seconds / 3600;
      if (interval > 1) {
        return Math.floor(interval) + " hours";
      }
      interval = seconds / 60;
      if (interval > 1) {
        return Math.floor(interval) + " minutes";
      }
      return Math.floor(seconds) + " seconds";
    },
    checkJobStatus(jobId) {
      const path = this.getApiUrl('get_job')
      let d = {
        user: this.storeState.user, 
        jobId: jobId,
        }
      axios.post(path, d)
        .then((res) => {
          console.log('got get_job: ', res.data)
          var self = this
          if (!res.data.ok) {
            setTimeout(() => self.checkJobStatus(jobId), 500);
          } else if (res.data.ok && res.data.job.status === 'running') {
            this.storeState.jobStatuses[jobId] = res.data.job
            setTimeout(() => self.checkJobStatus(jobId), 1000);
          } else {
            this.storeState.jobStatuses[jobId] = res.data.job
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    checkJobStatuses() {
      this.storeState.jobStatuses = {}
      for (let index = 0; index < this.jobIds.length; index++) {
        const jobId = this.jobIds[index];
        this.checkJobStatus(jobId)
      }
    },
    focusStripe() {
      if (!this.storeState.user.hasStripe && this.$refs.stripe_api_key) {
        this.$refs.stripe_api_key.focus()
      }
    },
    updateStripeApiKey() {
      if (this.stripeApiKey.length < 5) {
        let secondary = `
          Go to your 
          <a 
            href="https://dashboard.stripe.com/apikeys/create"
            class="font-medium text-blue-600 hover:text-blue-500"
            target="_blank"
          >
            dashboard
          </a>
          to create a key.
        `
        let opts = {
          primary: 'Invalid Stripe API key',
          secondary: secondary,
          type: 'error'
          }
        this.showMsg(this, opts)
        return
      }
      this.updatingStripeKey = true
      const path = this.getApiUrl('update_secret')
      let d = {
        user: this.storeState.user, 
        stripeApiKey: this.stripeApiKey,
        type: 'stripe'
        }
      axios.post(path, d)
        .then((res) => {
          this.updatingStripeKey = false
          console.log('got update_secret: ', res.data)
          if (res.data.ok) {
            let opts = {
              primary: 'Stripe API key successfully added!',
              secondary: 'Starting sync, this will take a few minutes.',
              }
            this.showMsg(this, opts)
            this.storeState.user.hasStripe = true
            this.jobIds = res.data.jobIds
            this.checkJobStatuses()
          } else {
            let opts = {
              primary: 'Stripe API key error.',
              secondary: res.data.error,
              type: 'error'
              }
            this.showMsg(this, opts)
          }
        })
        .catch((error) => {
          this.updatingStripeKey = false
          console.error(error)
        })
    },
    runDbt() {
      if (!this.storeState.isLoggedIn || !this.storeState.gotUserData) return
      this.runningDbt = true
      const path = this.getApiUrl('run_dbt')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          this.runningDbt = false
          console.log('got run_dbt: ', res.data)
          if (res.data.ok) {
            this.dbtLogs = res.data.dbtLogs
            this.storeState.user.hasMrrFacts = true
            this.dbtErrors = res.data.dbtErrors
            for (let index = 0; index < this.dbtLogs.length; index++) {
              const log = this.dbtLogs[index];
              let ti = this.storeState.dbt.models.findIndex(m => m.name === log.table)
              if (ti >= 0) this.storeState.dbt.models[ti].count = log.count
            }
            for (let index = 0; index < this.dbtErrors.length; index++) {
              const log = this.dbtErrors[index];
              console.error(log.message)
            }
          }
        })
        .catch((error) => {
          this.runningDbt = false
          console.error(error)
        })
    },
    updateDimensionNow(index, index2, column) {
      this.updatingField = true
      this.fieldInUpdate = column
      this.fieldInUpdate.index = index
      this.fieldInUpdate.index2 = index2
      this.fieldInUpdate.dimOrMeas = 'dimension'
      let label = this.getDimensionLabel(column)
      if (this.storeState.analysis.viz.encoding.x.field === label) {
        this.fieldInUpdate.axis = this.vizOptions.axis[1]
      }
      if (this.storeState.analysis.viz.encoding.y.field === label) {
        this.fieldInUpdate.axis = this.vizOptions.axis[2]
      }
      if (!this.fieldInUpdate.axis) this.fieldInUpdate.axis = this.vizOptions.axis[0]
    },
    updateMeasureNow(index, index3, measureName) {
      let model = this.storeState.dbt.models[index]
      let column = model.columns[index3]
      
      let measure = this.storeState.dbt.models[index].columns[index3].meta.measures[measureName]
      this.fieldInUpdate = measure
      this.fieldInUpdate.description = `${measure.type} of ${model.name}.${column.name}`
      // this.fieldInUpdate.column = column
      this.updatingField = true
      this.fieldInUpdate.index = index
      this.fieldInUpdate.index3 = index3
      this.fieldInUpdate.dimOrMeas = 'measure'
      let label = this.getMeasureLabel(measure)
      if (this.storeState.analysis.viz.encoding.x.field === label) {
        this.fieldInUpdate.axis = this.vizOptions.axis[1]
      }
      if (this.storeState.analysis.viz.encoding.y.field === label) {
        this.fieldInUpdate.axis = this.vizOptions.axis[2]
      }
      if (!this.fieldInUpdate.axis) this.fieldInUpdate.axis = this.vizOptions.axis[0]
    },
    flipVizType(type) {
      this.storeState.analysis.viz.type = type
      this.createViz({})
    },
    createViz(opts) {
      console.log('createViz...')
      this.searching = false
      this.updatingField = false
      this.searchTerm = ''
      if (this.storeState.analysis.results.rows.length === 0) return
      let vegaOpts = {
        config: this.vegaConfig,
        actions: false,
      }
      let viz = this.deepCopy(this.vegaSpec)
      viz.encoding = this.storeState.analysis.viz.encoding
      viz.encoding.tooltip = []
      if (viz.encoding.x.field) {
        let ttX = {"field": viz.encoding.x.field, "title": viz.encoding.x.field}
        viz.encoding.tooltip.push(ttX)
      }
      if (viz.encoding.y.field) {
        let ttY = {"field": viz.encoding.y.field, "title": viz.encoding.y.field}
        viz.encoding.tooltip.push(ttY)
      }
      
//       {
//     "x": {
//         "field": "Month",
//         "type": "ordinal"
//     },
//     "y": {
//         "field": "Avg MRR",
//         "type": "quantitative"
//     }
// }
      // customers.encoding.tooltip = [
      //     {"field": "mrr_month_dt", "timeUnit": "yearmonth", "title": "Date"},
      //     {
      //       "field": "active", 
      //       "aggregate": "sum", 
      //       "type": "quantitative",
      //       "format": ",.0f",
      //       "title": "Customers"
      //     }
      // ]
      viz.mark.type = this.storeState.analysis.viz.type
      // viz.data.values = []
      for (let index = 0; index < this.storeState.analysis.results.rows.length; index++) {
        let row = {}
        const element = this.storeState.analysis.results.rows[index];
        for (let index2 = 0; index2 < this.storeState.analysis.results.cols.length; index2++) {
          row[this.storeState.analysis.results.cols[index2].name] = element[index2]
        }
        viz.data.values.push(row)
      }
      window.vegaEmbed('#viz', viz, opts);
    },
    setupMousetrap() {
      var self = this
      Mousetrap.bind('4', function(e) { console.log('4'); });
      Mousetrap.bind('/', function(e) { 
        if (e && e.preventDefault) e.preventDefault()
        self.$refs.search.focus()
      });
      Mousetrap.bind('esc', function(e) { 
        if (e && e.preventDefault) e.preventDefault()
        self.$refs.search.blur()
        self.searching = false
        self.updatingField = false
        self.searchTerm = ''
      });
      Mousetrap.bind('command+enter', function(e) { 
        if (e && e.preventDefault) e.preventDefault()
        self.runAnalysis()
      });
      
    },
    closeSearch() {
      this.$refs.search.blur()
      this.searching = false
      this.searchTerm = ''
    },
    generateDemoTable() {
      new Grid({
        sort: true,
        // search: true,
        columns: ["Name", "Email", "Phone Number"],
        data: [
          ["John", "john@example.com", "(353) 01 222 3333"],
          ["Mark", "mark@gmail.com", "(01) 22 888 4444"],
          ["Eoin", "eoin@gmail.com", "0097 22 654 00033"],
          ["Sarah", "sarahcdd@gmail.com", "+322 876 1233"],
          ["Afshin", "afshin@mail.com", "(353) 22 87 8356"]
        ],
        className: {
          td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-100 divide-y divide-gray-200',
          th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
          table: 'min-w-full divide-gray-200',
          tbody: 'bg-white '
        }
      }).render(document.getElementById("testtable"));
    },
    createGrid(data) {
      console.log('createGrid...')
  //     columns: [
  //     { 
  //       name: 'Name',
  //       formatter: (cell) => `Name: ${cell}`
  //     },
  //     'Email',
  //  ],
      let columns = []
      for (let index = 0; index < data.cols.length; index++) {
        const col = data.cols[index];
        if (col.format) col.formatter = (cell) => `${SSF.format(col.format, cell)}`
        // col.formatter = (cell) => `${col.format}: ${cell}`
        columns.push(col)
      }
      window.analyzeGrid.updateConfig({
      // lets update the columns field only
        data: data.rows,
        columns: columns
      })
      if (window.analyzeGrid.config.container) {
        window.analyzeGrid.forceRender()
      } else {
        window.analyzeGrid.render(document.getElementById("gridInner"));
      }
      // document.getElementById("customerTable").innerHTML = ''
    },
    getApiUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://127.0.0.1:5000/${endpoint}`
      return `https://pulse-backend.onrender.com/${endpoint}`
    },
    getAppUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://localhost:8080/${endpoint}`
      return `https://trypaper.io/${endpoint}`
    },
    updateSavedFunders() {
      this.storeState.userData.savedFunders = []
      for (let index = 0; index < this.filteredFunders.length; index++) {
        const row = this.filteredFunders[index];
        if (row.saved) this.storeState.userData.savedFunders.push(row.public_id)
      }
      this.updateUserData()
    },
    updateSavedOnFunders() {
      for (let index = 0; index < this.funderData.length; index++) {
        const f = this.funderData[index]
        if (this.storeState.userData.savedFunders.includes(f.public_id)) f.saved = true
      }
    },
    saveFunder(row) {
      row.saved = true
      if (!this.storeState.isLoggedIn || !this.storeState.user.publicAddress) {
        this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
      }
    },
    updateUserData() {
      if (!this.storeState.isLoggedIn || !this.storeState.gotUserData) return
      const path = this.getApiUrl('update_user_data')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got update_user_data: ', res.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    removeFunder(row) {
      row.saved = false
      // this.storeState.userData.savedFunders.pop(row.domain)
      if (!this.storeState.isLoggedIn || !this.storeState.user.publicAddress) {
        this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
      } else {
        // save funder to users db
        this.updateUserData()
      }
    },
    applyNow() {
      this.$router.push({ name: 'Apply'})
    },
    moreInfo(row) {
      // this.saveFunder(row)
      if (!this.storeState.isLoggedIn || !this.storeState.user.publicAddress) {
        this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
      } else {
        let url = `http://${row.domain}/?ref=trypaperio`
        window.open(url, '_blank');
      }
    },
    searchMatch(model, column) {
      if (this.searchTerm.length === 0) return true
      // var searchIn = `${model.name} ${column.name}`
      var searchIn = `${column.name}`
      let label = this.getLabel(column)
      if (label) searchIn += ` ${label}`
      if (searchIn.includes(this.searchTerm)) return true
      return false
    },
    selectColumnTimeframe(index, index2, column, timeframe) {
      let dimOrMeas = 'dimension'
      let curVal = this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].timeframe
      if (curVal === timeframe) {
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].timeframe = false
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = false
      } else {
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].timeframe = timeframe
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = true
      }
      this.searchTerm = ''
    },
    removeColumn(index, index2, column, dimOrMeas) {
      if (this.isDateColumn(column)) {
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].timeframe = false
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = false
        return
      }
      let curVal = this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected
      this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = !curVal
      this.searchTerm = ''
      var self = this
      setTimeout(() => self.updatingField = false, 0);
      // this.$nextTick(function() {
      //   // DOM is now updated
      //   // `this` is bound to the current instance
      //   console.log('removeColumn: ', column)
      //   this.updatingField = false
      // })
    },
    selectColumn(index, index2, column, dimOrMeas) {
      if (this.isDateColumn(column)) {
        return
      }
      let curVal = this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected
      this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = !curVal
      this.searchTerm = ''
    },
    selectMeasure(index, index2, measureName) {
      let curVal = this.storeState.dbt.models[index].columns[index2].meta.measures[measureName].selected
      this.storeState.dbt.models[index].columns[index2].meta.measures[measureName].selected = !curVal
      this.searchTerm = ''
      this.$forceUpdate()
      setTimeout(() => this.updatingField = false, 0);
    },
    isMeasureSelected(index, index2, measureName) {
      let curVal = this.storeState.dbt.models[index].columns[index2].meta.measures[measureName].selected
      return curVal
    },
    isDimOrMeas(index, index2, column, dimOrMeas) {
      let exists = this.storeState.dbt.models[index].columns.find(c => c.name === column.name)
      return exists.meta && exists.meta[dimOrMeas]
    },
    isDateColumn(column) {
      return column.meta && column.meta.dimension && column.meta.dimension.timeframes
    },
    isSelected(index, index2, column, dimOrMeas) {
      if (this.storeState.dbt.models[index].columns[index2] && 
          this.storeState.dbt.models[index].columns[index2].meta && 
          this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas]
          ) {
            return this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected
          }
      return false
    },
    getFieldLabel(fieldInUpdate) {
      if (fieldInUpdate.dimOrMeas === 'measure') {
        return fieldInUpdate.label
      }
      return this.getDimensionLabel(fieldInUpdate)
    },
    getDimensionLabel(column) {
      if (column.meta && column.meta.dimension && column.meta.dimension.label) {
        return column.meta.dimension.label
      }
      return column.name
    },
    getMeasureLabel(column, columnName) {
      if (column && column.label) {
        return column.label
      }
      return columnName
    },
    getSelected(column) {
      if (column.meta && column.meta.dimension && column.meta.dimension.label) {
        return column.meta.dimension.label
      }
      if (column.meta && column.meta.measure && column.meta.measure.label) {
        return column.meta.measure.label
      }
      return column.name
    },
    getDbt() {
      this.gotDbt = false
      const path = this.getApiUrl('get_dbt')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got get_dbt: ', res.data)
          this.gotDbt = true
          this.storeState.dbt = res.data.data
          // this.metricData = reactive(res.data)
          // this.createCharts()
          // this.createCustomerTable()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    cancelRun() {
      this.running = false
      this.searching = false
    },
    showMsg(self, opts) {
      self.storeState.msg.show = true
      self.storeState.msg.primary = opts.primary
      self.storeState.msg.secondary = opts.secondary
      self.storeState.msg.type = opts.type
      setTimeout(() => self.storeState.msg.show = false, self.storeState.msg.time);
    },
    deepCopy(c) {
      return JSON.parse(JSON.stringify(c))
    },
    updateSettings() {
      const path = this.getApiUrl('update_settings')
      if (!this.storeState.user.settings) return
      let d = {user: this.storeState.user}
      axios.post(path, d)
        .then((res) => {
          console.log('update_settings: ', res.data)
        })
        .catch((error) => {
          console.error('update_settings: ', error)
        })
    }
  },
  watch: {
    'storeState.user.settings.notifications': {
        handler: function () {
          if (this.storeState.gotUserData) this.updateSettings()
        },
        deep: true
    },
    // 'storeState.user.settings.sheets': {
    //     handler: function () {
    //       if (this.storeState.gotUserData) this.updateSettings()
    //     },
    //     deep: true
    // },
  },
}
/* eslint-disable no-unused-vars */
/* eslint-disable no-empty */
/* eslint-disable vue/no-unused-components */

</script>