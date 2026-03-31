# Homelab Upgrade Pt.1 - New hardware!

*2025-10-15*

Did somebody say server? Wait server cluster? Multi-node server chassis?!?!? Count me in.

# The eBay find

Every once in a while I like to peruse eBay for interesting deals, and a few weeks ago I got interested in a specific type of server...

![Example blade server](/static/homelab-hardware/blade-server.png)

I'm sure we've all seen huge multi-blade chassis servers, and thought "damn those would be impractical" for a homelab. They're usually at a minimum 6-8U, the loudest machines in existence, and endlessly thirsty for power. Well, they actually have a slightly more manageable little sibling: node servers.

![Example node server](/static/homelab-hardware/node-server.png)

After looking around at the various options, anything from the [Dell PowerEdge C6300](https://www.dell.com/support/product-details/en-us/product/poweredge-c6300/overview) series seemed like a decent fit. They were modern enough to have DDR4 RAM, but old enough to be fairly cheap on the used market. They were small enough to fit under a sofa (don't ask), but large enough to house 4 nodes with a number of drives each which I thought would be a reasonable number to have for a clustered environment (3 being the minimum for most clustered applications).

![Ebay listing](/static/homelab-hardware/ebay.png)

After a few weeks of searching I found an impossibly good price for one (update Mar 2026: yeah... the same device is ~£900 now) - it seemingly had everything I needed as well so I pulled the trigger and decided to work out the details once it arrived.

# The hardware

Once the hardware arrived (and I worked out how to haul 2 giant boxes up the stairs) I gave it a very quick check over.

![First look at node after unboxing](/static/homelab-hardware/unbox.jpg)

The spec as delivered was (with 4x for the chassis-total):
- 2x Intel(R) Xeon(R) CPU E5-2630 v3 -> 32c64t @2.4GHz
- 32GB DDR4 -> 128GB DDR4

I also had 128GB of RAM and a bunch of drives in my old server, but until I had migrated the workload off of that it had to stay intact for now, and that's a story for my next blog post :)

# Fans go brrr... too much brrr

Another thing I noticed was that despite me thinking that node servers should have been the more manageable, quieter cousin to blade servers... that might have just been me finding an excuse to purchase some cool hardware. In reality, when the servers were booted they would run their fans at near 100% all the time (and these are some of the beefier server fans I've had the misfortune of dealing with), with absolutely no way to spin them down even through IPMI as fan control was handled by the interface-less chassis and not the nodes.

I initially thought it'd be fine, but after a few weeks of being unable to solve the problem in software, and a very quickly dropping partner-approval-factor, I decided I'd have to remediate the issue in hardware.

![Old fans](/static/homelab-hardware/old-fan.png)

The fans that came in the server were an odd size - 60mm square and 40mm deep, and they also came with a weird proprietary fan connector that in reality was just a more annoying way to wire a standard 4-pin fan. I decided I'd try and replace them with some [Noctua NF-A6x25](https://www.noctua.at/en/products/nf-a6x25-pwm)s, as they seemed to be the closest match that had a chance of being quiet. I had some concerns that they might not have enough airflow or pressure, or that I wouldn't be able to get the connector situation sorted out... but given the rapidly declining partner-approval-factor decided to purchase the fans and work it out once I had them.

![New fans installed](/static/homelab-hardware/new-fans.png)

Installing the fans was... interesting. I was able to take the foam off of the old fans and stick it back to the Noctua ones to allow them to slot into the same place on the chassis, but the power connector situation proved a bit tricky. With a little dupont connector fuckery (literally shaving them down on one corner to fit them into the weird PCIE-power-ish connector I got things working though.

Once the fans were installed I booted the server back up, and to my surprise... everything seemed to work? The chassis was even able to read the fan speeds correctly, and while it became pretty apparent that the BMC would not be turning the fans below 100% speed ever, this was still a lot quieter than the old fans, and barely audible once the server was closed.

And well... that's that. I may be the only person with a node server under their sofa with Noctua fans in existence, and only time will tell whether it throttles under load, but at least it's quiet and I can play around with clustered technologies at home.
