# Build Instructions

The Dockerfile in this folder is used to build an Ubuntu test host with the
necessary tools to validate tcconfig functionality. 

The topology file in this folder is used to build a simple test topology for
validating impairment capabilities enabled by tcconfig.

```shell
$ sudo docker image build --tag local:debuff --build-arg USER=<VAR> --build-arg PSWD=<VAR> .
$ sudo containerlab deploy --topo debuff.yml
```

The hosts will be accessible via SSH from their assigned IP address in the
172.100.100.0/24 range. Containerlab will provide the IP address after the lab
is deployed. You can also view the **debuff.yml** file to find the mgmt IP. Use
the credentials specified in **docker image build** to establish an SSH session.

**Important!** 

On host1 and host2 you will need to specify an IP address on their **Eth1**
interfaces and an IP route so traffic can forward through the debuff host.

```shell
# configuration for host1
$ ssh admin@172.100.100.50
admin@host1:~$ sudo ip addr add 10.1.1.2/30 dev eth1
admin@host1:~$ sudo ip route add 10.0.0.0/8 via 10.1.1.1

# configuration for host2
$ ssh admin@172.100.100.51
admin@host2:~$ sudo ip addr add 10.2.2.2/30 dev eth1
admin@host2:~$ sudo ip route add 10.0.0.0/8 via 10.2.2.1

# configuration for debuff
$ ssh admin@172.100.100.10
admin@debuff:~$ sudo ip addr add 10.1.1.1/30 dev eth1
admin@debuff:~$ sudo ip addr add 10.2.2.1/30 dev eth2
```

At this point you should have IP connectivity from host1 to host2 via debuff.

```shell
admin@host1:~$ ping -c 3 10.2.2.2
PING 10.2.2.2 (10.2.2.2) 56(84) bytes of data.
64 bytes from 10.2.2.2: icmp_seq=1 ttl=63 time=0.088 ms
64 bytes from 10.2.2.2: icmp_seq=2 ttl=63 time=0.085 ms
64 bytes from 10.2.2.2: icmp_seq=3 ttl=63 time=0.074 ms
```

Now you are able to use **tcconfig** on **debuff** to test impairment settings.

```shell
# configuration for debuff
$ ssh admin@172.100.100.10
admin@debuff:~$ sudo tcset eth1 --delay 100ms

# confirm on host delay is set
$ ssh admin@172.100.100.50
admin@host1:~$ ping -c 3 10.2.2.2
PING 10.2.2.2 (10.2.2.2) 56(84) bytes of data.
64 bytes from 10.2.2.2: icmp_seq=1 ttl=63 time=100 ms
64 bytes from 10.2.2.2: icmp_seq=2 ttl=63 time=100 ms
64 bytes from 10.2.2.2: icmp_seq=3 ttl=63 time=100 ms 
```
