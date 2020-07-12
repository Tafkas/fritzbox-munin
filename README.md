# fritzbox-munin

A collection of munin plugins to monitor your AVM FRITZ!Box router. The scripts have been developed using a [FRITZ!Box 7490](http://geni.us/OO2c7S)(Amazon link) running FRITZ!OS 07.12.

If you are using the scripts on a different Fritz!Box model please let me know by

## Introduction

   These python scripts are [Munin](http://munin-monitoring.org) plugins for monitoring the [Fritz!Box](http://avm.de/produkte/fritzbox/) router by AVM.

## fritzbox\_traffic

  fritzbox\_traffic shows you the traffic of the WAN interface (requires fritzconnection)
  ![http://i.imgur.com/8BwNMOL.png](http://i.imgur.com/8BwNMOL.png)

  If you do not want to show the interface maximum values, add the following to your plugin-configuration:

    env.traffic_remove_max true

## fritzbox\_connection\_uptime

  fritzbox\_connection\_uptime shows you the connection uptime in days (requires fritzconnection)
  ![http://i.imgur.com/8oE1OYL.png](http://i.imgur.com/8oE1OYL.png)

## fritzbox\_cpu\_usage

  fritzbox\_cpu\_usage shows you the cpu usage (requires password)
  ![http://i.imgur.com/A9uGvWP.png](http://i.imgur.com/A9uGvWP.png)

## fritzbox\_cpu\_temperature

  fritzbox\_cpu\_temperature shows you the cpu temperature (requires password)
  ![http://i.imgur.com/duHYhw6.png](http://i.imgur.com/duHYhw6.png)

## fritzbox\_memory\_usage

  fritzbox\_memory\_usage shows you the memory usage (requires password)
  ![http://i.imgur.com/WhxrINK.png](http://i.imgur.com/WhxrINK.png)

##  fritzbox\_power\_consumption

  fritzbox\_power\_consumption shows you the power consumption (requires password)
  ![http://i.imgur.com/a7uQzn6.png](http://i.imgur.com/a7uQzn6.png)

## fritzbox\_uptime

  fritzbox\_uptime shows you the uptime in days (requires password) (language dependant, see below).
  ![http://i.imgur.com/Jr8OibH.png](http://i.imgur.com/Jr8OibH.png)

## fritzbox\_wifi\_devices

  fritzbox\_wifi\_devices shows you the number of connected wifi clients (requires password) (language dependant, see below).
  ![http://i.imgur.com/lqvK1b2.png](http://i.imgur.com/lqvK1b2.png)

## Installation & Configuration

1. Pre-requesites for the fritzbox\_traffic and fritzbox\_uptime plugins are the [fritzconnection](https://pypi.python.org/pypi/fritzconnection) and [requests](https://pypi.python.org/pypi/requests) package. To install it

        pip install fritzconnection
        pip install lxml

2. Make sure the FritzBox has UPnP status information enabled. (German interface: Heimnetz > Heimnetzübersicht > Netzwerkeinstellungen > Statusinformationen über UPnP übertragen)

3. Copy all the scripts (*.py) to `/usr/share/munin/plugins`

4. Make all the scripts execute able (chmod 755 /usr/share/munin/plugins.*py)

5. Create entry in `/etc/munin/plugin-conf.d/munin-node`:
     1. only one fritzbox or all fritzboxes use the same password:

            [fritzbox_*]
               env.fritzbox_password <fritzbox_password>
               env.traffic_remove_max true # if you do not want the possible max values
  
    2. multiple fritzboxes:
    
           [fritzbox_<fqdn1>_*]
             env.fritzbox_password <fritzbox_password>
             env.traffic_remove_max true # if you do not want the possible max values

           [fritzbox_<fqdn2>_*]
             env.fritzbox_password <fritzbox_password>
             env.traffic_remove_max true # if you do not want the possible max values

6. Create symbolic link in `/etc/munin/plugins` for `fritzbox_helper.py`.

       cd /etc/munin/plugins
       ln -d /usr/share/munin/plugins/fritzbox_helper.py fritzbox_helper.py

7. Create symbolic link in `/etc/munin/plugins` for probes.
  
       link `/usr/share/munin/plugins/fritzbox__<probe>.py` to `fritzbox_<fqdn>_<probe>`

       example
         cd /etc/munin/plugins
         ln -d /usr/share/munin/plugins/fritzbox__cpu_usage.py fritzbox_fritz.box_cpu_usage
         ln -d /usr/share/munin/plugins/fritzbox__cpu_temperature.py fritzbox_fritz.box_cpu_temperature  
         ...

       if you have multiple fritz box just create multiple sets of links with a different fqdn or ip.

       example
         cd /etc/munin/plugins
         ln -d /usr/share/munin/plugins/fritzbox__cpu_usage.py fritzbox_fritz.box_cpu_usage
         ln -d /usr/share/munin/plugins/fritzbox__cpu_usage.py fritzbox_box2.fritz.box_cpu_usage
         ln -d /usr/share/munin/plugins/fritzbox__cpu_usage.py fritzbox_192.168.100.1_cpu_usage
         ln -d /usr/share/munin/plugins/fritzbox__cpu_temperature.py fritzbox_box2.fritz.box_cpu_temperature  
         ln -d /usr/share/munin/plugins/fritzbox__cpu_temperature.py fritzbox_box2.fritz.box_cpu_temperature  
         ln -d /usr/share/munin/plugins/fritzbox__cpu_temperature.py fritzbox_192.168.100.1_cpu_temperature  
         ...

8. Restart the munin-node daemon: `systemctl restart munin-node`.

9. Done. You should now start to see the charts on the Munin pages.

## Localization

Two scripts depend on the language selected in your fritzbox: the uptime and wifi\_devices. Currently, two locales are
supported:

1. German: `de` (default)
2. English: `en`

You can change the used locale by setting an environment variable in your plugin configuration:

    env.locale en

## Set a group for your fritzboxes

You can group the graphs of your fritzbox:

1. Use the following as your host configuration in `/etc/munin/munin.conf` or by creating a file in `/etc/munin/munin-conf.d`

        [<groupname>;<fqdn>]
            address 127.0.0.1
            use_node_name no

        example:
        [Network;fritz.box]
            address 127.0.0.1
            use_node_name no

2. Restart your munin-node: `systemctl restart munin-node`

## Environment Settings

  Do not forget to restart the munin-node daemon as described in step 3 of the installation instructions above.
