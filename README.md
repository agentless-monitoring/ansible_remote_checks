# Ansible Remote Checks for Linux


Design goals:

 - Enable Icinga to execute agentless checks for linux machines

<pre>

    +-------------------------------------+
    |   Icinga Server                     |
    |                                     |
    |                                     |
    |  +-------------------------------+  |
    |  |  Icinga                       |  |
    |  |                               |  |
    |  | 1. Start check                |  |
    |  |        +                      |  |
    |  |        |                      |  |
    |  |        v                      |  |
    |  | +------+---------------+      |  |
    |  | | Nagios checks        |      |  |
    |  | |                      |      |  |
    |  | +----------------------+      |  |
    |  +-------------------------------+  |
    |             ^  |                    |
    | 6. Return   |  | 2. Call ansible to |
    |    module   |  |    execute module  |
    |    results  |  |    remotely        |
    |             |  |                    |
    |   +---------+--v----------------+   |
    |   | Linux Adapter               |   |                          +--------------------------+
    |   |                             |   |                          |  Remote Linux Server     |
    |   | (Ansible API client)        |   |                          |                          |
    |   |                             |   |      3. Send module      |                          |
    |   |                             |   |                          |   4. Execute  module     |
    |   +---------+--+----------------+   |     +--------------+     |                          |
    |             |  ^                    |     |Ansible module|     |    +--------------+      |
    |             |  |                    |     +--------------+     |    |Ansible module|      |
    |   +---------v--+----------------+   |                          |    +--------------+      |
    |   | Ansible                     |   +------------------------> |                          |
    |   |                             |   <------------------------+ |                          |
    |   +-----------------------------+   |  5. Send module results  +--------------------------+
    +-------------------------------------+

</pre>

# Commands 

```
object CheckCommand "service-linux" {
  import "plugin-check-command"

  command = [ PluginDir + "/check_service_ansible" ]

  arguments = {
    "-H" = "$ansible_host$"
    "-S" = "$service_name$"
  }

  timeout = 120

  vars.ansible_host = "$address$"
}


object CheckCommand "load-linux" {
  import "plugin-check-command"

  command = [ PluginDir + "/check_load_ansible" ]

  arguments = {
    "-H" = "$ansible_host$"
  }

  timeout = 120

  vars.ansible_host = "$address$"
}

object CheckCommand "cpu-linux" {
  import "plugin-check-command"

  command = [ PluginDir + "/check_cpu_ansible" ]

  arguments = {
    "-H" = "$ansible_host$"
  }

  timeout = 120

  vars.ansible_host = "$address$"
}


object CheckCommand "disk-linux" {
  import "plugin-check-command"

  command = [ PluginDir + "/check_fs_ansible" ]

  arguments = {
    "-H" = "$ansible_host$"
    "-F" = "$fs_regex$"
  }

  timeout = 120

  vars.ansible_host = "$address$"
}

object CheckCommand "memory-linux" {
  import "plugin-check-command"

  command = [ PluginDir + "/check_memory_ansible" ]

  arguments = {
    "-H" = "$ansible_host$"
  }

  timeout = 120

  vars.ansible_host = "$address$"
}

object CheckCommand "swap-linux" {
  import "plugin-check-command"

  command = [ PluginDir + "/check_swap_ansible" ]

  arguments = {
    "-H" = "$ansible_host$"
  }

  timeout = 120

  vars.ansible_host = "$address$"
}

object CheckCommand "updates-linux" {
  import "plugin-check-command"

  command = [ PluginDir + "/check_update_ansible" ]

  arguments = {
    "-H" = "$ansible_host$"
  }

  timeout = 120

  vars.ansible_host = "$address$"
}

object CheckCommand "sg-linux" {
  import "plugin-check-command"
 
  command = [ PluginDir + "/check_sg_ansible" ]

  arguments = {                                                                                                                                                                           
    "-H" = "$ansible_host$"
    "-C" = "$cluster$"
    "-N" = { value = "$node$" }
    "-P" = { value = "$package_regex$"}
  }

  timeout = 120

  vars.ansible_host = "$address$"
}


object CheckCommand "process-linux" {                                                                                                                                                     
  import "plugin-check-command" 

  command = [ PluginDir + "/check_process_ansible" ]
  arguments = {
    "-H" = "$ansible_host$",
    "-p" = "$process_name_regex$",
    "-r" = "$cmdline_regex$",
    "-m" = "$mode$",
    "-C" = "$process_count$"
  }
  timeout = 120
  vars.ansible_host = "$address$"
}

object CheckCommand "directory-linux" {
  import "plugin-check-command"
  command = [ PluginDir + "/check_directory_ansible"]
  arguments = {
    "-H" = "$ansible_host$",
    "-R" = "$directory_regex$",
    "-p" = "$path$"
    "-M" = "$mode$",
    "-c" = "$file_count$"
  }
  timeout = 120
  vars.ansible_host = "$address$"
}
```
