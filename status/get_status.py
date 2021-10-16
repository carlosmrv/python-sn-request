from config import USER, PASSWORD, INSTANCE, ASSGROUP

import pysnow
from dict_text import rls_text

c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)

number = ''


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


def get_open_task(rls=number, group=ASSGROUP):
    task_list = []
    task = c.resource(api_path='/table/rm_task')
    rls_id, rls_state = get_rls_status(rls=rls)
    if rls_state == "15" or rls_state == "9" or rls_state == '5':
        response = task.get(query={'top_task.number': rls, 'state': '1', 'assignment_group.name': group},
                            stream=True)
        for record in response.all():
            # print(record['number'])
            task_list.append(record['number'])
        return task_list
    else:
        print("RLS state %s not Match with open Task" % rls_state)
