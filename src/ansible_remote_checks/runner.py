#!/usr/bin/env python

import ansible
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.playbook.play import Play
from ansible.plugins.loader import init_plugin_loader
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
from ansible import context
from collections import namedtuple
import os 
from os.path import expanduser 
import shutil

class ResultCallback(CallbackBase):
  def v2_runner_on_ok(self, result, **kwargs):
    self.status = 'ok'
    self.check_result(result)
         
  def v2_runner_on_failed(self, result, ignore_errors=False):
    self.status = 'failed'
    self.check_result(result)
    
  def v2_runner_on_unreachable(self, result):
    self.status = 'unreachable'
    self.check_result(result)    

  def check_result(self, res):
    try:
      result = res._result
      host = res._host.name
      self.set_result(host, result)
    except AttributeError:
      self.set_result('', '')
   
  def set_result(self, hostname, result):
    self.result = {'ansible_status': self.status, hostname: result}
  

class Runner():
  def __init__(self, host, remote_user='icinga-check', private_key_file=None):
    init_plugin_loader()
    self.host=host
    sources = '%s,' % (host)
    
    module_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "modules"))
    if private_key_file == None:
      private_key_file = '%s/.ssh/id_rsa' % (expanduser('~'))    
   
    # Options = namedtuple('Options', ['ask_pass','connection','module_path', 'forks', 'check' ,'become', 'become_method', 'become_user', 'private_key_file', 'remote_user', 'diff', 'ssh_extra_args'])
    context.CLIARGS = ImmutableDict(connection='smart', module_path=[module_path], forks=100, become=None,become_method=None, become_user=None, check=False, diff=False, ssh_extra_args='-o StrictHostKeyChecking=no', private_key_file=private_key_file, remote_user=remote_user,)

   # self.options = Options(ask_pass=False, connection='smart', module_path=[module_path], forks=100, check=False,  become=None, become_method=None, become_user=None,  private_key_file=private_key_file, remote_user=remote_user, diff=False , ssh_extra_args='-o StrictHostKeyChecking=no')

    #Since there is no possibility to use ssh passwords for decryption we do not use any passwords 
    self.passwords = dict()
    
    self.results_callback = ResultCallback()

    self.loader = DataLoader()
    self.inventory = InventoryManager(loader=self.loader, sources=sources)
    self.variable_manager = VariableManager(loader =self.loader, inventory=self.inventory)

  def run_play(self, module , args=dict(), playname="Ansible Remote Icinga Check"):    
    play_source = dict(
      name = playname,
      hosts = self.host,
      gather_facts = 'no',
      tasks = [dict(action=dict(module=module, args=args)) ]
    )

    self.play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

    self.tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=self.passwords,
            stdout_callback=self.results_callback             
       )

    try:
      self.tqm.run(self.play)
    finally:
      if self.tqm is not None:
        self.tqm.cleanup()
      
      # Remove ansible tmpdir
      shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
      
      if hasattr(self.results_callback, 'result'):
        return self.results_callback.result
      else:
        return {'status': 'no status'}
        
