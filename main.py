import pysnow
import requests
from datetime import datetime, timedelta
from itertools import chain
from config import USER, PASSWORD, INSTANCE,RLS

# Create client object
c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)
number = ""
rls_text = {
    "1": "(Nuevo)",
    "2": "(Certificación)",
    "14": "(Esperando Aceptación)",
    "5": "(Pruebas)",
    "6": "(Evaluar)",
    "9": "(Implementación)",
    "10": "(Revisión)",
    "11": "(Cerrado)"
}


def get_status(rls=number):
    # Define a resource, here we'll use the release table API
    release = c.resource(api_path='/table/rm_release')

    response = release.get(query={'number': rls}, stream=True)
    # Iterate over the result and print out `sys_id` of the matching records.
    for record in response.all():
        print(record['number'], rls_text[record['state']])
        sys_id = record['sys_id']
        state = record['state']
        return sys_id, state


if __name__ == '__main__':
    rls_id, rls_state = get_status(rls=RLS)
