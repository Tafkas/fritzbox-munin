# fritzbox-munin
A collection of munin plugins to monitor your AVM FRITZ!Box router 
 
## Introduction

   These python scripts are [Munin](http://munin-monitoring.org) plugins for monitoring the [Fritz!Box](http://avm.de/produkte/fritzbox/) router by AVM.

## fritzbox_traffic

  fritzbox_traffic shows you the traffic of the WAN interface.
 
## fritzbox_uptime

  fritzbox_uptime shows you the connection uptime in days

## Installation & Configuration 

   1. Copy all the scripts to =/usr/share/munin/plugins

   2. Create symbolic links to =/etc/munin/plugins=.

   3. Restart the munin-node daemon: =/etc/init.d/munin-node restart=.

   4. Done. You should now start to see the charts on the
      Munin pages.

## Environment Settings
   Do not forget to restart the munin-node daemon as described in step
   3 of the installation instructions above.

