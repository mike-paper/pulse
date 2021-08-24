// import axios from 'axios';

export const store = {
  state: {
      showDebugStuffNow: false,
      isLoggedIn: false,
      checkedLogin: false,
      gotUserData: false,
      gotDbt: false,
      hideSidebar: false,
      gotMetrics: false,
      gotEvents: false,
      metricData: {},
      events: {data: []},
      user: {
        ok: false,
        oauth: false,
        hasStripe: false,
        settings: {}
      },
      slackCode: false,
      // settings: {
      //   notifications: {
      //     alerts: {
      //       slack: true,
      //       email: false,
      //     },
      //     weekly: {
      //       slack: true,
      //       email: true,
      //     },
      //     monthly: {
      //       slack: true,
      //       email: true,
      //     },
      //   }
      // },
      dbt: {},
      jobStatuses: {},
      analysis: {
        uuid: false,
        mode: 'search',
        code: 'select *\nfrom customers as c',
        results: {
          rows: [],
          cols: [],
        },
        viz: {
          type: 'grid',
          encoding: {
            "x": {"field": false, "type": "ordinal"},
            "y": {"field": false, "type": "quantitative"},
          }
        }
      },
      userData: {
        savedFunders: []
      },
      msg: {
        show: false,
        primary: '',
        secondary: '',
        icon: '',
        type: '',
        time: 8000,
      }
  }
}