#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from paunch.builder import base


class PodmanBuilder(base.BaseBuilder):

    def __init__(self, config_id, config, runner, labels=None, log=None):
        super(PodmanBuilder, self).__init__(config_id, config, runner,
                                            labels, log)

    def container_run_args(self, cmd, container):
        cconfig = self.config[container]
        if cconfig.get('detach', True):
            cmd.append('--detach=true')
        self.list_or_string_arg(cconfig, cmd, 'env_file', '--env-file')
        # TODO(sbaker): support the dict layout for this property
        for v in cconfig.get('environment', []):
            if v:
                cmd.append('--env=%s' % v)
        self.boolean_arg(cconfig, cmd, 'remove', '--rm')
        self.boolean_arg(cconfig, cmd, 'interactive', '--interactive')
        self.boolean_arg(cconfig, cmd, 'tty', '--tty')
        self.string_arg(cconfig, cmd, 'net', '--net')
        self.string_arg(cconfig, cmd, 'ipc', '--ipc')
        self.string_arg(cconfig, cmd, 'pid', '--pid')
        self.string_arg(cconfig, cmd, 'uts', '--uts')
        # TODO(sbaker): implement ulimits property, deprecate this ulimit
        # property
        for u in cconfig.get('ulimit', []):
            if u:
                cmd.append('--ulimit=%s' % u)

        self.string_arg(cconfig, cmd, 'privileged', '--privileged', self.lower)
        self.string_arg(cconfig, cmd, 'user', '--user')
        self.list_arg(cconfig, cmd, 'group_add', '--group-add')
        self.list_arg(cconfig, cmd, 'volumes', '--volume')
        self.list_arg(cconfig, cmd, 'volumes_from', '--volumes-from')
        # TODO(sbaker): deprecate log_tag, implement log_driver, log_opt
        if 'log_tag' in cconfig:
            cmd.append('--log-opt=tag=%s' % cconfig['log_tag'])
        self.string_arg(cconfig, cmd, 'cpu_shares', '--cpu-shares')
        self.string_arg(cconfig, cmd, 'mem_limit', '--memory')
        self.string_arg(cconfig, cmd, 'memswap_limit', '--memory-swap')
        self.string_arg(cconfig, cmd, 'mem_swappiness', '--memory-swappiness')
        self.string_arg(cconfig, cmd, 'security_opt', '--security-opt')
        self.string_arg(cconfig, cmd, 'stop_signal', '--stop-signal')

        self.string_arg(cconfig, cmd,
                        'stop_grace_period', '--stop-timeout',
                        self.duration)

        self.list_arg(cconfig, cmd, 'cap_add', '--cap-add')
        self.list_arg(cconfig, cmd, 'cap_drop', '--cap-drop')
        self.string_arg(cconfig, cmd, 'check_interval', '--check-interval')

        cmd.append(cconfig.get('image', ''))
        cmd.extend(self.command_argument(cconfig.get('command')))
