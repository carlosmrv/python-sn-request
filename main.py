import pysnow
import requests
from config import USER,PASSWORD,INSTANCE

# Create client object
c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)

# Define a resource, here we'll use the incident table API
incident = c.resource(api_path='/v2/table/incident')

# Set the payload
new_record = {
    'short_description': 'Pysnow created incident',
    'description': 'This is awesome'
}

# Create a new incident record
result = incident.create(payload=new_record)