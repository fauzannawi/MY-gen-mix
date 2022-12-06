#https://stackoverflow.com/questions/5919981/getting-data-from-a-chart-that-is-displayed-on-a-website
#specify request date
import datetime
import pytz
my_zone = pytz.timezone('Asia/Kuala_Lumpur')
current_time = datetime.datetime.now(my_zone)
request_date = current_time - datetime.timedelta(days=1)
request_date_str = request_date.strftime("%d/%m/%Y")

#request data from GSO server
headers = """Host: www.gso.org.my
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/json; charset=utf-8
X-Requested-With: XMLHttpRequest
Content-Length: 47
Origin: https://www.gso.org.my
Connection: keep-alive
Referer: https://www.gso.org.my/SystemData/SystemDemand.aspx
Cookie: ASP.NET_SessionId=5wvdwpvcyi2aoauwr0dzg3gn
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
TE: trailers"""
headers = dict([[s.strip() for s in line.split(':', 1)]
                for line in headers.strip().split('\n')])
#data available since 01/09/2016
body = '{"Fromdate":"'+request_date_str+'","Todate":"'+request_date_str+'"}'
import httplib2 
h = httplib2.Http()
url = 'https://www.gso.org.my/SystemData/CurrentGen.aspx/GetChartDataSource'
resp, content = h.request(url, 'POST', body=body, headers=headers)

#clean-up  data
#create dataframe for data
generation = str(content)
data = generation.replace("[","").replace("]","").replace("'","").replace("b","").replace('"d"',"").replace('\\',"").replace("{:","")
data = data[1:-2]
import pandas as pd
df = pd.read_json(data, lines=True)

#export to google cloud bucket
from google.cloud import storage
client = storage.Client()
xname=request_date_str.replace("/","-")
source_file_name=f'{xname}.csv'
destination_blob_name='my-gen-mix-bucket'
bucket = client.bucket(destination_blob_name)
blob = bucket.blob(source_file_name)
blob.upload_from_string(df.to_csv(index=False), 'text/csv')
print('File {} uploaded to {}.'.format(
      source_file_name,
      destination_blob_name))