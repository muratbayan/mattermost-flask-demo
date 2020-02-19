# mattermost-flask-demo
Small Flask service used to send data to Mattermost in various ways

Install flask in your environment, then execute **flask run** with additonal arguments if needed (for example, in my case 'flask run --host=0.0.0.0')

You can access the content of the service created by browsing http://<localhost-or-for-me-0.0.0.0>:5000/chosen-service to see the formatted results of the call

There are currently three services available
* forex - to get the forex data between a source and a target currency
* stock - to get the value of a chosen stock symbol
* holiday - to get a sample holiday allowance checker with a random number of days taken
