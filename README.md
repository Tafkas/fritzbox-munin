# fritzbox-munin

A collection of munin plugins to monitor your AVM FRITZ!Box router. The scripts have been developed using a [FRITZ!Box 7590](http://geni.us/OO2c7S)(Amazon link) running FRITZ!OS 7.25.

If you are using the scripts on a different Fritz!Box model please let me know by

- opening an issue
- submitting a pull request

 So far the following models (running FRITZ!OS 06.83) have been confirmed working:

- [FRITZ!Box 3370](http://geni.us/zh3U)
- [FRITZ!Box 5490](http://geni.us/ACtUyFt)
- [FRITZ!Box 7362 SL](http://geni.us/fTyoY)
- [FRITZ!Box 7390](http://geni.us/BlAP)
- [FRITZ!Box 7430](http://geni.us/BlAP)
- [FRITZ!Box 7490](http://geni.us/fTyoY)
- [FRITZ!Box 7530](https://geni.us/h8oqYd)
- [FRITZ!Box 7530 AX](https://geni.us/a4dS5)  
- [FRITZ!Box 7560](http://geni.us/6gPZNI)
- [FRITZ!Box 7580](http://geni.us/yUYyQTE)
- [FRITZ!Box 7590](http://geni.us/OO2c7S)

 If you are still running an older Fritz!OS version check out the [releases section](https://github.com/Tafkas/fritzbox-munin/releases/).

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

  fritzbox\_cpu\_usage shows you the cpu usage (requires username & password)
  ![http://i.imgur.com/A9uGvWP.png](http://i.imgur.com/A9uGvWP.png)

## fritzbox\_cpu\_temperature

  fritzbox\_cpu\_temperature shows you the cpu temperature (requires username & password)
  ![http://i.imgur.com/duHYhw6.png](http://i.imgur.com/duHYhw6.png)

## fritzbox\_memory\_usage

  fritzbox\_memory\_usage shows you the memory usage (requires username & password)
  ![http://i.imgur.com/WhxrINK.png](http://i.imgur.com/WhxrINK.png)

##  fritzbox\_power\_consumption

  fritzbox\_power\_consumption shows you the power consumption (requires username & password)
  ![http://i.imgur.com/a7uQzn6.png](http://i.imgur.com/a7uQzn6.png)

## fritzbox\_uptime

  fritzbox\_uptime shows you the uptime in days (requires username & password) (language dependant, see below).
  ![http://i.imgur.com/Jr8OibH.png](http://i.imgur.com/Jr8OibH.png)

## fritzbox\_wifi\_devices

  fritzbox\_wifi\_devices shows you the number of connected wifi clients (requires username & password) (language dependant, see below).
  ![http://i.imgur.com/lqvK1b2.png](http://i.imgur.com/lqvK1b2.png)

## Installation & Configuration

1. Pre-requesites for the fritzbox\_traffic and fritzbox\_uptime plugins are the [fritzconnection](https://pypi.python.org/pypi/fritzconnection) and [requests](https://pypi.python.org/pypi/requests) package. To install it

        pip install -r requirements.txt
 
 fritzconnection requires python3. Make sure python --version is >= 3.6.  

2. Make sure the FritzBox has UPnP status information enabled. (German interface: Heimnetz > Heimnetzübersicht > Netzwerkeinstellungen > Statusinformationen über UPnP übertragen)

3. Copy all the scripts to `/usr/share/munin/plugins`

4. Create entry in `/etc/munin/plugin-conf.d/munin-node`:

        [fritzbox_*]
        env.fritzbox_ip <ip_address_to_your_fritzbox>
        env.fritzbox_username <fritzbox_username>
        env.fritzbox_password <fritzbox_password>
        env.traffic_remove_max true # if you do not want the possible max values
        host_name fritzbox

5. Create symbolic links to `/etc/munin/plugins`.

6. Restart the munin-node daemon: `/etc/init.d/munin-node restart`.

7. Done. You should now start to see the charts on the Munin pages.

## Localization

Two scripts depend on the language selected in your fritzbox: the uptime and wifi\_devices. Currently, two locales are
supported:

1. German: `de` (default)
2. English: `en`

You can change the used locale by setting an environment variable in your plugin configuration:

    env.locale en

## Different hosts for the fritzbox and your system

You can split the graphs of your fritzbox from the localhost graphs by following the next steps:

1. Use the following as your host configuration in `/etc/munin/munin.conf`

        [home.yourhost.net;server]
            address 127.0.0.1
            use_node_name yes


        [home.yourhost.net;fritzbox]
            address 127.0.0.1
            use_node_name no

2. Add the following to your munin-node configuration

    env.host_name fritzbox

3. Restart your munin-node: `systemctl restart munin-node`

## Environment Settings

  Do not forget to restart the munin-node daemon as described in step 3 of the installation instructions above.
