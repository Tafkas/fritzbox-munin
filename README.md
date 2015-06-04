# fritzbox-munin
A collection of munin plugins to monitor your AVM FRITZ!Box router. The scripts have been developed using a FRITZ!Box 7362 SL running FRITZ!OS 06.20.
 
## Introduction

   These python scripts are [Munin](http://munin-monitoring.org) plugins for monitoring the [Fritz!Box](http://avm.de/produkte/fritzbox/) router by AVM.

## fritzbox_traffic

  fritzbox\_traffic shows you the traffic of the WAN interface.
 
## fritzbox_uptime

  fritzbox\_uptime shows you the connection uptime in days
## fritzbox\_wifi\_devices

  fritzbox\_wifi\_devices shows you the number of connected wifi clients (requires password)

## fritzbox\_cpu\_usage

  fritzbox\_cpu\_usage shows you the cpu usage (requires password)

## fritzbox\_cpu\_temperature

  fritzbox\_cpu\_temperature shows you the cpu temperature (requires password)
  
## fritzbox\_memory\_usage

  fritzbox\_memory\_usage shows you the memory usage (requires password)

##  fritzbox\_power\_consumption

  fritzbox\_power\_consumption shows you the power consumption (requires password)
  

## Installation & Configuration 

1. Copy all the scripts to =/usr/share/munin/plugins
   
2. Create entry in /etc/munin/plugin-cond.d/munin-node:  
    
    [fritzbox_\*]  
    env.fritzbox\_ip *ip_address_to_your_fritzbox*  
    env.fritzbox\_password *fritzbox_password*  

3. Create symbolic links to =/etc/munin/plugins=.

4. Restart the munin-node daemon: =/etc/init.d/munin-node restart=.

5. Done. You should now start to see the charts on the
      Munin pages.

## Environment Settings
   Do not forget to restart the munin-node daemon as described in step
   3 of the installation instructions above.
