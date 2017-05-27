from concurrent import futures
from queue import Queue
from bson import ObjectId

__author__ = 'Amir H. Nejati'


class ChainExecutorBase:
    retry = None
    task_pool_module = None
    _executor_pool = None
    _task_queue = None
    _sys_functions_chain = None
    _job_stats = None

    def __init__(self, tasks_order_tuple, job_elements, task_pool_module, concurrent_chains_max=100, retry=3, auto_start=True):
        """
        :param tuple `tasks_order_tuple`: a tuple containing task names to be chained and executed
        :param python_module `task_pool_module`: the module containing all tasks mentioned in 'tasks_order_tuple' param
        """
        self.retry = retry
        self.task_pool_module = task_pool_module
        self._executor_pool = futures.ThreadPoolExecutor(min(concurrent_chains_max, len(job_elements)))
        self._task_queue = Queue()
        self._sys_functions_chain = tasks_order_tuple
        self._job_stats = dict()
        for i in job_elements:
            self._task_queue.put(i[0])
            d = dict()
            d['job_id'] = i[1].get('job_id') or ObjectId()
            d['last_done_task'] = i[1].get('last_done_task')
            d['latter_task_tries'] = i[1].get('latter_task_tries') or 0
            d['last_result'] = i[1].get('last_result')
            self._job_stats[i[0]] = d
        if auto_start:
            self.run()

    def run(self):
        while True:
            if all([i['last_done_task'] == self._sys_functions_chain[-1] or i['latter_task_tries'] == self.retry
                    for i in self._job_stats.values()]):
                break
            e = self._task_queue.get(block=True)
            if self.logger: self.logger.debug('j_elem `{}` picked up.'.format(e))
            self.execute_chains(e)
        self._executor_pool.shutdown(wait=True)

    def execute_chains(self, elem):
        func_name, task_ix = self.task_chain_get_next(elem)
        if func_name:
            func = getattr(self.task_pool_module, func_name)  # func = getattr(sys.modules[__name__], func_name)
            self._job_stats[elem]['latter_task_tries'] += 1
            timeout_minutes = getattr(self.task_pool_module, 'timeout_estimations')[func_name]
            self.pickup_phase(self._job_stats[elem]['job_id'], self._sys_functions_chain, task_ix, elem, timeout_minutes)
            # if job_id and not self._job_stats[elem]['job_id']:
            #     self._job_stats[elem]['job_id'] = job_id
            if type(self._job_stats[elem]['last_result']) is dict:
                f = self._executor_pool.submit(func, **self._job_stats[elem]['last_result'])
            elif type(self._job_stats[elem]['last_result']) in [tuple, list]:
                f = self._executor_pool.submit(func, *self._job_stats[elem]['last_result'])
            else:
                f = self._executor_pool.submit(func, self._job_stats[elem]['last_result'])
            f.elem_name = elem
            f.func_name = func_name
            f.add_done_callback(self.post_exec_act)

    def task_chain_get_next(self, element):
        last_ran_task = self._job_stats[element]['last_done_task']
        if not last_ran_task:
            return self._sys_functions_chain[0], 0
        pos = self._sys_functions_chain.index(last_ran_task) + 1
        return (self._sys_functions_chain[pos], pos) if pos < len(self._sys_functions_chain) else (None, -1)

    def post_exec_act(self, f):
        # print(f.result())
        if f.cancelled():
            if self.logger: self.logger.warning('j_elem `{}` canceled.'.format(f.elem_name))
        elif f.done():
            error = f.exception()
            if error:
                if self.logger: self.logger.error('j_elem `{}` task `{}` failed!\terr_msg: `{}`'.format(f.elem_name, f.func_name, error))
                self.terminate_phase(self._job_stats[f.elem_name]['job_id'], f.func_name, f.elem_name,
                                     self._job_stats[f.elem_name]['latter_task_tries'], error=str(error))
                if self._job_stats[f.elem_name]['latter_task_tries'] >= self.retry:
                    return
            else:
                if self.logger: self.logger.info('j_elem `{}` task `{}` done.\tret_val: `{}`'.format(f.elem_name, f.func_name, f.result()))
                self.terminate_phase(self._job_stats[f.elem_name]['job_id'], f.func_name, f.elem_name,
                                     self._job_stats[f.elem_name]['latter_task_tries'], result=f.result())
                self._job_stats[f.elem_name]['last_done_task'] = f.func_name
                self._job_stats[f.elem_name]['last_result'] = f.result()
                self._job_stats[f.elem_name]['latter_task_tries'] = 0
            self._task_queue.put(f.elem_name)

    def pickup_phase(self, *args, **kwargs):
        """ override for custom pickup action """
        raise NotImplementedError

    def terminate_phase(self, *args, **kwargs):
        """ override for custom termination action """
        raise NotImplementedError

    @property
    def logger(self):
        """ in case of logger to be used, property must return instance of python logging,
            with any custom handlers set. """
        return None
