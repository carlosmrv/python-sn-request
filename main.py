import pysnow
import requests
from datetime import datetime, timedelta
from itertools import chain
from config import USER, PASSWORD, INSTANCE,PARENT,REQGROUP,ASSGROUP,RLS,SNOWTECHNOLOGY,SNOWAPPLICATION

# Create client object
c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)
number = ""
rls_text = {
    "1": "(New)",
    "2": "(Certification)",
    "14": "(Waiting Accept)",
    "5": "(Test)",
    "6": "(Evaluation)",
    "9": "(Implementation)",
    "10": "(Revision)",
    "11": "(Closed)"
}


def create_rls():
    # Define a resource, here we'll use the incident table API
    rls = c.resource(api_path='/table/rm_release')
    # Define Time date for rls management
    proposed_date = datetime.now()
    start_date = proposed_date + timedelta(minutes=30)
    end_date = proposed_date + timedelta(days=15)
    # Convert to string to parse Json
    proposed_date = proposed_date.strftime("%Y-%m-%d %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M")

    # Set the payload
    new_record = {
        "parent": PARENT,
        "u_requested_group": REQGROUP,
        "u_reason": "New Application",
        "u_risk": "4",
        "assignment_group": ASSGROUP,
        "short_description": "Prueba Creacion RLSE 2",
        "description": "Prueba Creacion RLSE 2",
        "u_justification": "Prueba Creacion RLSE 2",
        "u_implementation_plan": "Prueba Creacion RLSE 2",
        "u_preproduction_proposed_date": proposed_date,
        "u_start_date": start_date,
        "u_end_date": end_date
    }
    # Create a new incident record
    result = rls.create(payload=new_record)
    for record in result.all():
        print(record['number'], rls_text[record['state']])
        sys_id_new = record['sys_id']
        state_new = record['state']
        rls_number_new = record['number']
        return sys_id_new, state_new, rls_number_new


def get_rls_status(rls=number):
    # Define a resource, here we'll use the release table API
    release = c.resource(api_path='/table/rm_release')

    response = release.get(query={'number': rls}, stream=True)
    # Iterate over the result and print out `sys_id` of the matching records.
    for record in response.all():
        print(record['number'], rls_text[record['state']])
        sys_id_local = record['sys_id']
        state_check = record['state']
        return sys_id_local, state_check


def update_rls(rls=number):
    release = c.resource(api_path='/table/rm_release')
    update = {'short_description': 'New short description', 'state': 5}

    updated_record = release.update(query={'number': rls}, payload=update)

    # Print out the updated record
    print(updated_record)


def create_task(rls=number, enviroment="Pre-Production"):
    # Define a resource, here we'll use the incident table API
    task = c.resource(api_path='/table/rm_task')
    # Define Time date for rls management
    proposed_date = datetime.now()
    start_date = proposed_date + timedelta(minutes=30)
    end_date = proposed_date + timedelta(days=15)
    # Convert to string to parse Json
    proposed_date = proposed_date.strftime("%Y-%m-%d %H:%M")
    start_date = start_date.strftime("%Y-%m-%d %H:%M")
    end_date = end_date.strftime("%Y-%m-%d %H:%M")

    # Set the payload
    new_record = {
        "top_task": rls,
        "u_release": rls,
        "start_date": start_date,
        "end_date": end_date,
        "short_description": "test 2",
        "description": "test 2",
        "u_state_to_resolve": enviroment,
        "type": "Other Deployment",
        "assignment_group": ASSGROUP,
        "order": "100",
        "u_technology": SNOWTECHNOLOGY,
        "u_version": "NA",
        "u_application": SNOWAPPLICATION
    }
    # Create a new incident record
    result = task.create(payload=new_record)
    for record in result.all():
        print(record['number'], record['state'])
        task_new = record['state']
        return task_new,


if __name__ == '__main__':
    # sys_id, state, rls_number = create_rls()
    rls_id, rls_state = get_rls_status(rls=RLS)
    # task = create_task(rls=RLS)
    # task_pro = create_task(rls=RLS,enviroment="Implement")
