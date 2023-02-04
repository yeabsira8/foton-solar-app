from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import json




app=Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods =["GET", "POST"])
def hello_world():
   
   
   token = '80859a806cf967f5575278cb32df4f3685211615'
   api_base = 'https://www.renewables.ninja/api/'

   s = requests.session()
 # Send token header with each request
   s.headers = {'Authorization': 'Token ' + token}


  

 ##
 # PV example
 ##



   url = api_base + 'data/pv'

   lat1 = None
   lon1 = None
   date_from1 = None   
   date_to1 = None
   capacity1 = None

   if request.method == "POST":
    
       # getting inputs from in HTML form
       lat1 = request.form.get("lat1")
       lon1 = request.form.get("lon1")
       date_from1 = request.form.get("date_from1")
       date_to1 = request.form.get("date_to1")
       capacity1 = request.form.get("capacity1")


      # Create the API request parameters
       args = {
        'lat': lat1,
        'lon': lon1,
        'date_from': date_from1,
        'date_to': date_to1,
        'dataset': 'merra2',
        'capacity': capacity1,
        'system_loss': 0.1,
        'tracking': 0,
        'tilt': 35,
        'azim': 180,
        'format': 'json'
          }
        
   

       r = s.get(url, params=args)

   
   

       # Parse JSON to get a pandas.DataFrame of data and dict of metadata
       parsed_response = json.loads(r.text)

       data = pd.read_json(json.dumps(parsed_response['data']), orient='index')

      # Convert the data to a pandas dataframe
      # df = pd.DataFrame(data)
      # Resample the DataFrame into monthly intervals
       monthly_data = data.resample('M').sum()

       monthly_data.index = pd.to_datetime(monthly_data.index)
       monthly_data['Month'] = monthly_data.index.month_name()

       monthly_data = monthly_data[['Month', 'electricity']]

       print(monthly_data)
       
       return render_template('index.html', data=monthly_data.to_html(classes='table table-striped'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
