# Pulse - Open source SaaS metrics

<img src="https://user-images.githubusercontent.com/74681824/130497241-94b2b6e3-c7be-4417-a723-7e9950262945.png" width="800">

\
&nbsp;

- **Transparency** - Easily drill down and see how metrics are calculated at the customer level
- **Open source &** **Private** - The entire app is open source and easy to self host
- **Extensible &** **Hackable** - Have some weird edge case you need to exclude? Easily update your data model with a little SQL.
- **Push first** - Metrics can be pushed to Slack, Sheets, and email so you don't need to check yet another dashboard

\
&nbsp;

<!-- ![Main App Screenshot](https://user-images.githubusercontent.com/74681824/130246369-7f5ddbc7-3e27-44c1-8a12-f5ab8d004cb4.png) -->

<img src="https://user-images.githubusercontent.com/74681824/130494900-50338886-5c7b-4aae-8d3c-cf88fd3a1f56.gif" width="800">


\
&nbsp;
\
&nbsp;

### There is a [free hosted version here](https://pulse.trypaper.io/?ref=github) 

## Self-Hosted

* Docker - See [docker-compose.yml](docker-compose.yml)
* Render - See [render.yaml](render.yaml) as a guide (you'll need to remove the domain)
* GCP - TODO
* AWS - TODO

## Google Sheets

1. Go to the Sheet you want to connect to Pulse
2. Click "Share" in the top right
3. Share the sheet with paperbot@paperfinancial.iam.gserviceaccount.com	
4. Add the Spreadsheet ID (long ID in the Sheet URL) and sheet name to https://pulse.trypaper.io/settings

![Sheets Auth](https://user-images.githubusercontent.com/74681824/129019362-3f3563e9-662d-4d76-b00e-bc21363ae2fb.png)


