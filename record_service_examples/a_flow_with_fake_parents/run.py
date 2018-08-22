from pyopereto.client import OperetoClient
import sys, traceback
import time


class MyFlowService():

    def __init__(self):
        self.client = OperetoClient()
        self.input = self.client.input
        self.failed = False

    def run(self):
        try:

            def _end_fake_parent_process(parent_pid, child_process_pids=[]):
                if self.client.is_success(child_process_pids):
                    self.client.stop_process(parent_pid, 'success')
                else:
                    self.failed = True
                    self.client.stop_process(parent_pid, 'failure')


            ## create a "fake" parent process
            parent_1_pid = self.client.create_process('fake_parent_process', title='First commands group')

            ## attach some services to it as child processes
            cmd_1_pid = self.client.create_process('shell_command', title='df -k', command='df -k', pflow_id=parent_1_pid)
            cmd_2_pid = self.client.create_process('shell_command', title='netstat -rn', command='netstat -rn', pflow_id=parent_1_pid)

            _end_fake_parent_process(parent_1_pid, [cmd_1_pid,cmd_2_pid])


            time.sleep(10)


            ## create a second "fake" parent process
            parent_2_pid = self.client.create_process('fake_parent_process', title='Second commands group')

            ## attach some services to it as child processes
            cmd_3_pid = self.client.create_process('shell_command', title='df -k', command='df -k', pflow_id=parent_2_pid)
            cmd_4_pid = self.client.create_process('shell_command', title='netstat -rn', command='netstat -rn' ,pflow_id=parent_2_pid)

            _end_fake_parent_process(parent_2_pid, [cmd_3_pid, cmd_4_pid])

            time.sleep(5)
            ## set final result
            if self.failed:
                return self.client.FAILURE
            return self.client.SUCCESS

        except:
            traceback.format_exc()
            return self.client.FAILURE

if __name__ == "__main__":
    exit(MyFlowService().run())