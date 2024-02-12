import atexit

from . import defines, setting


@atexit.register
def cleanup():
    gs = setting.getGlobalSetting()
    for key, value in list(gs.worker_table.items()):
        if gs.worker_table[key].status != defines.Status.CLOSED: 
            gs.worker_table[key].close()
        gs.unregister(value)
    for key, value in list(gs.pool_table.items()):
        if not gs.pool_table[key]['pool'].closed:
            gs.pool_table[key]['pool'].close()
        gs.unregister(value['pool'])
