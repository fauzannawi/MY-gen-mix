#https://stackoverflow.com/questions/5919981/getting-data-from-a-chart-that-is-displayed-on-a-website
#specify request date
import datetime
import pytz
my_zone = pytz.timezone('Asia/Kuala_Lumpur')
current_time = datetime.datetime.now(my_zone)
request_date = current_time - datetime.timedelta(days=1)
request_date_str = request_date.strftime("%d/%m/%Y")

#copy data from google storage bucket to bigquery
from google.cloud import bigquery
client = bigquery.Client()
dataset_id = 'mygenmix'
dataset_ref = client.dataset(dataset_id)
#### COPY FROM GOOGLE SORAGE TO BIGQUERY, DUNIT
job_config = bigquery.LoadJobConfig()
job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
job_config.schema = [
    bigquery.SchemaField("DT", "TIMESTAMP"),
    bigquery.SchemaField("Coal", "INTEGER"),
    bigquery.SchemaField("Gas", "INTEGER"),
    bigquery.SchemaField("CoGen", "INTEGER"),
    bigquery.SchemaField("Oil", "INTEGER"),
    bigquery.SchemaField("Hydro", "INTEGER"),
    bigquery.SchemaField("Solar", "INTEGER"),
]
job_config.skip_leading_rows = 1
# The source format defaults to CSV, so the line below is optional.
job_config.source_format = bigquery.SourceFormat.CSV
xname=request_date_str.replace("/","-")
uri = f'gs://my-gen-mix-bucket/{xname}.csv'

load_job = client.load_table_from_uri(
    uri, dataset_ref.table("gsodata"), job_config=job_config
)  # API request
print("Starting job {}".format(load_job.job_id))

load_job.result()  # Waits for table load to complete.
print("Job finished.")

destination_table = client.get_table(dataset_ref.table("gsodata"))
print("Loaded {} rows.".format(destination_table.num_rows))