import pysnow
import requests
from datetime import datetime, timedelta
from itertools import chain
from config import USER, PASSWORD, INSTANCE, PARENT, REQGROUP, ASSGROUP, RLS, SNOWTECHNOLOGY, SNOWAPPLICATION

# Create client object
c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)
number = ""
rls_text = {
    "1": "(New)",
    "2": "(Certification)",
    "14": "(Waiting Accept)",
    "15": "Pre-Production",
    "5": "(Test)",
    "6": "(Evaluation)",
    "9": "(Implementation)",
    "10": "(Revision)",
    "11": "(Closed)",
    "-5": "Pending"
}

tsk_text = {
    "-5": "Pending",
    "1": "Open",
    "3": "Closed Complete",
    "7": "Closed Skipped"
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


def update_rls_cert(rls=number):
    release = c.resource(api_path='/table/rm_release')

    update = {
        "state": "2",
        "work_notes": "Se pasa la Release a Certificación"
    }
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "1":
        # Update 'short_description' and 'state' for 'INC012345'
        updated_record = release.update(query={'number': rls}, payload=update)
        # Print out the updated record
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def update_rls_pre(rls=number):
    release = c.resource(api_path='/table/rm_release')

    update = {
        "state": "14",
        "work_notes": "Se pasa la Release a PRE"
    }
    rls_id, rls_state = get_rls_status(rls=rls)
    # Update 'short_description' and 'state' for 'INC012345'
    if rls_state == "2":
        # Update 'short_description' and 'state' for 'INC012345'
        updated_record = release.update(query={'number': rls}, payload=update)
        # Print out the updated record
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def approve_rls_pre(rls=number):
    approve_sys_id = ""
    release = c.resource(api_path='/table/sysapproval_approver')
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "14":
        response = release.get(query={"approver.user_name": USER, "sysapproval.number": rls}, stream=True)
        for record in response.all():
            approve_sys_id = record['sys_id']
        update = {
            "state": "approved"
        }
        updated_record = release.update(query={'sys_id': approve_sys_id}, payload=update)
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def approve_rls_test(rls=number):
    approve_sys_id = ""
    release = c.resource(api_path='/table/rm_release')
    rls_id, rls_state = get_rls_status(rls=rls)
    open_task = get_open_task(rls=rls)
    if rls_state == "15" and len(open_task) == 0:
        update = {
            "state": "5",
            "work_notes": "Se pasa la Release a Pruebas"
        }
        updated_record = release.update(query={'number': rls}, payload=update)
        print(updated_record)
    else:
        print("RLS state is", rls_text[rls_state])


def get_open_task(rls=number):
    task_list = []
    task = c.resource(api_path='/table/rm_task')
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "15" or rls_state == "9" or rls_state == '5':
        response = task.get(query={'top_task.number': rls, 'state': '1', 'assignment_group.name': ASSGROUP},
                            stream=True)
        for record in response.all():
            # print(record['number'])
            task_list.append(record['number'])
        return task_list
    else:
        print("RLS state %s not Match with open Task" % rls_state)


def get_task_status(tsk=number):
    task = c.resource(api_path='/table/rm_task')
    response = task.get(query={'number': tsk}, stream=True)
    for record in response.all():
        print(record)
        state_check = record['state']
        print(tsk_text[record['state']])
        return state_check


def close_task(tsk=number):
    task = c.resource(api_path='/table/rm_task')
    update = {
        "work_notes": "Desplegado",
        "state": "Closed Complete",
        "u_close_code": "Successful automatic",
        "close_notes": "Desplegado en PRE-STG",
        "assigned_to": "u4x7TAn4Aq@co-example.com",

    }
    task_state = get_task_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5"):
        updated_record = task.update(query={'number': tsk}, payload=update)
        print(updated_record)
    else:
        print("Task %s Already Closed" % tsk)

def close_test_task(tsk=number):
    task = c.resource(api_path='/table/rm_task')
    update = {
        "state": "Closed Complete",
        "u_close_code": "Successful automatic",
        "close_notes": "Desplegado en PRE-STG",
        "assigned_to": "u4x7TAn4Aq@co-example.com",
        'u_performance_test_type': 'Unitary',
        'u_performance_result': 'OK',
    }
    task_state = get_task_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5"):
        updated_record = task.update(query={'number': tsk}, payload=update)
        print(updated_record)
    else:
        print("Task %s Already Closed" % tsk)


def attachment_task(tsk=number, file='requirements.txt'):
    task = c.resource(api_path='/table/rm_task')

    task_state = get_task_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5") and (task_state != "-7"):
        upload_record = task.get(query={'number': tsk})
        upload_record.upload(file_path=file)
        print(upload_record)
    else:
        print("Task %s Already Closed" % tsk)


def cancel_task(tsk=number):
    task = c.resource(api_path='/table/rm_task')
    update = {
        "work_notes": "Desplegado",
        "state": "Closed Skipped",
        "u_close_code": "Cancelled",
        "close_notes": "Problem in task",
        "assigned_to": "u4x7TAn4Aq@co-example.com"
    }
    task_state = get_task_status(tsk=tsk)
    if (task_state != "3") and (task_state != "-5") and (task_state != "7"):
        updated_record = task.update(query={'number': tsk}, payload=update)
        print(updated_record)
    else:
        print("Task %s Already Closed" % tsk)


if __name__ == '__main__':
    # sys_id, state, rls_number = create_rls()
    # rls_id, rls_state = get_rls_status(rls=RLS)
    # task = create_task(rls=RLS)
    # task_pro = create_task(rls=RLS,enviroment="Implement")
    # update_rls_cert(rls=RLS)
    # rls_id, rls_state = get_rls_status(rls=RLS)
    # update_rls_pre(rls=RLS)
    # rls_id, rls_state = get_rls_status(rls=RLS)
    # approve_rls_pre(rls=RLS)
    rls_id, rls_state = get_rls_status(rls=RLS)
    opent_task = get_open_task(rls=RLS)
    print(len(opent_task))
    # attachment_task(tsk="RTSK0972004")
    get_task_status(tsk="RTSK0972004")
    close_test_task(tsk="RTSK0972004")
    get_task_status(tsk="RTSK0972004")
    approve_rls_test(rls=RLS)
    for task in opent_task:
        get_task_status(tsk=task)
        # close_task(tsk=task)
