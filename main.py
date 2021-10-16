import pysnow
from releases.rls import create_rls, update_rls_cert, approve_rls_pre, update_rls_pre, update_rls_eval, \
    update_rls_test, approve_rls_eval, update_rls_scheduled, update_rls_implement, update_rls_closed, \
    approve_rls_authorize
from tasks.tasks import create_task, get_task_status, create_delegate_task, close_task, close_test_task, \
    attachment_task, cancel_task, attachment_delegate_task
from status.get_status import get_rls_status, get_open_task
from config import USER, PASSWORD, INSTANCE, PARENT, REQGROUP, ASSGROUP, RLS, SNOWTECHNOLOGY, SNOWAPPLICATION, TESTGROUP
from dict_text import rls_text, tsk_text

# Create client object
c = pysnow.Client(instance=INSTANCE, user=USER, password=PASSWORD)
number = ""


def create_release_step1():
    sys_id, state, rls_number = create_rls()
    rls_id, rls_state = get_rls_status(rls=rls_number)
    task = create_task(rls=rls_number)
    task_pro = create_task(rls=rls_number,enviroment="Implement")
    return rls_number


def update_cert_pre_step2(RLS=RLS):
    update_rls_cert(rls=RLS)
    rls_id, rls_state = get_rls_status(rls=RLS)
    update_rls_pre(rls=RLS)
    rls_id, rls_state = get_rls_status(rls=RLS)


def approve_close_pre_step3(RLS=RLS):
    approve_rls_pre(rls=RLS)
    rls_id, rls_state = get_rls_status(rls=RLS)
    opent_task = get_open_task(rls=RLS)
    print(opent_task)
    for task in opent_task:
        close_task(tsk=task)
    update_rls_test(rls=RLS)


def update_close_task_test_step4(RLS=RLS):
    opent_task = get_open_task(rls=RLS, group=TESTGROUP)
    print(opent_task)
    task_del = create_delegate_task(rls=RLS)
    print(task_del)
    attachment_delegate_task(tsk=task_del)
    for task in opent_task:
        close_test_task(tsk=task) # No tiene permisos
    rls_id, rls_state = get_rls_status(rls=RLS)
    update_rls_eval(rls=RLS) # No tiene permisos




if __name__ == '__main__':

    # RLS = create_release_step1()
    update_cert_pre_step2(RLS=RLS)
    approve_close_pre_step3(RLS=RLS)
    update_close_task_test_step4(RLS=RLS) # no work no tiene permisos



    # approve_rls_eval(rls=RLS)
    # rls_id, rls_state = get_rls_status(rls=RLS)
    # approve_rls_authorize(rls=RLS)

    # update_rls_scheduled(rls=RLS)
    # opent_task = get_open_task(rls=RLS)
    # for task in opent_task:
    #     get_task_status(tsk=task)
    #     print(task)
    #     close_task(tsk=task)
    #
    # update_rls_implement(rls=RLS)
    # update_rls_closed(rls=RLS)
