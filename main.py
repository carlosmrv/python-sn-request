import pysnow
import requests
from releases.rls import create_rls, update_rls_cert, approve_rls_pre, update_rls_pre, approve_rls_eval, \
    approve_rls_test
from tasks.tasks import create_task, get_task_status, create_delegate_task, close_task, close_test_task, \
    attachment_task, cancel_task
from status.get_status import get_rls_status, get_open_task
from datetime import datetime, timedelta
from itertools import chain
from config import USER, PASSWORD, INSTANCE, PARENT, REQGROUP, ASSGROUP, RLS, SNOWTECHNOLOGY, SNOWAPPLICATION
from dict_text import rls_text, tsk_text

# Create client object
c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)
number = ""

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
    # get_task_status(tsk="RTSK0972004")
    # close_test_task(tsk="RTSK0972004")
    # get_task_status(tsk="RTSK0972004")
    approve_rls_test(rls=RLS)
    create_delegate_task(rls=RLS)
    approve_rls_eval(rls=RLS)
    rls_id, rls_state = get_rls_status(rls=RLS)
    # for task in opent_task:
    #     get_task_status(tsk=task)
    # close_task(tsk=task)
