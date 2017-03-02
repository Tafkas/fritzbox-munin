# fritzbox-munin
A collection of munin plugins to monitor your AVM FRITZ!Box router. The scripts have been developed using a 
FRITZ!Box 7362 SL running FRITZ!OS:131.06.36-32026 BETA. AVM has modified the web interface if the Fritz!Box 
in the current version that the old scripts do not work anymore. This branch also only works if the language 
of the Fritz!Box is set to German.

If you are using FRITZ!OS 6.30 use the master branch. 
 
## Introduction

   These python scripts are [Munin](http://munin-monitoring.org) plugins for monitoring the [Fritz!Box](http://avm.de/produkte/fritzbox/) router by AVM.

## fritzbox\_traffic

  fritzbox\_traffic shows you the traffic of the WAN interface (requires fritzconnection)  
  ![http://i.imgur.com/8BwNMOL.png](http://i.imgur.com/8BwNMOL.png)
  
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

  fritzbox\_uptime shows you the uptime in days (requires password)  
  ![http://i.imgur.com/Jr8OibH.png](http://i.imgur.com/Jr8OibH.png)

## fritzbox\_wifi\_devices

  fritzbox\_wifi\_devices shows you the number of connected wifi clients (requires password)
  ![http://i.imgur.com/lqvK1b2.png](http://i.imgur.com/lqvK1b2.png)
  

## Installation & Configuration 

0. Pre-requesites for the fritzbox\_traffic and fritzbox\_uptime plugins is the [fritzconnection](https://pypi.python.org/pypi/fritzconnection) package. To install it  
    
        pip install fritzconnection

1. Copy all the scripts to =/usr/share/munin/plugins
   
2. Create entry in /etc/munin/plugin-cond.d/munin-node:  
    
        [fritzbox_*]  
        env.fritzbox_ip <ip_address_to_your_fritzbox>  
        env.fritzbox_username <fritzbox_username>
        env.fritzbox_password <fritzbox_password>  

3. Create symbolic links to /etc/munin/plugins.

4. Restart the munin-node daemon: /etc/init.d/munin-node restart.

5. Done. You should now start to see the charts on the Munin pages.

## Environment Settings
  
  Do not forget to restart the munin-node daemon as described in step
  3 of the installation instructions above.

## Multiple Fritz!Boxes

  To generate graphs for additional boxes create new symbolic links (like in step 3) but chgange the first part of th
  e.g.: ```ln -s /usr/share/munin/plugins/fritzbox_uptime.py /etc/munin/plugins/freetz_uptime```

  And create a new section in ```/etc/munin/plugin-cond.d/munin-node``` with the alternative name.

```
[freetz_*]
env.fritzbox_ip <ip_address_to_your_second_fritzbox>
env.fritzbox_username <fritzbox_username>
env.fritzbox_password <fritzbox_password>
```

Restart the munin-node daemon.