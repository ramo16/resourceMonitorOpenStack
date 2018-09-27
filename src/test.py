from keystoneauth1 import session
from keystoneauth1.identity import v3
from novaclient import client
from time import sleep
from influxdb import InfluxDBClient
from credentials import *




#auth = v3.Password(auth_url="http://172.16.0.3:5000/v3", username="admin",password="admin", project_name="admin",user_domain_id="default", project_domain_id="default")

auth = v3.Password(auth_url=auth_url1, username=username1,password=password1, project_name=project_name1,user_domain_id=user_domain_id1, project_domain_id=project_domain_id1)



sess = session.Session(auth=auth)
nova_client = client.Client("2.1",session=sess)
nova = client.Client("2.1",session=sess)
images = nova_client.hypervisors.list()




client2 = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'ANM3')

def host_used_ram(nova_client, host):
    """ Get the used RAM of the host using the Nova API.
    :param nova: A Nova client.
     :type nova: *
    :param host: A host name.
     :type host: str
    :return: The used RAM of the host.
     :rtype: int
    """
    data = nova_client.hosts.get(host)
    if len(data) > 2 and data[2].memory_mb != 0:
        return data[2].memory_mb
    return data[1].memory_mb


def vms_by_host(nova, host):
    """ Get VMs from the specified host using the Nova API.
    :param nova: A Nova client.
     :type nova: *
    :param host: A host name.
     :type host: str
    :return: A list of VM UUIDs from the specified host.
     :rtype: list(str)
    """
    return [str(vm.id) for vm in nova.servers.list()
            if vm_hostname(vm) == host]



def vms_by_hosts(nova, hosts):
    """ Get a map of host names to VMs using the Nova API.
    :param nova: A Nova client.
     :type nova: *
    :param hosts: A list of host names.
     :type hosts: list(str)
    :return: A dict of host names to lists of VM UUIDs.
     :rtype: dict(str: list(str))
    """
    result = dict((host, []) for host in hosts)
    for vm in nova.servers.list():
        result[vm_hostname(vm)].append(str(vm.id))
    return result


def vm_hostname(vm):
    """ Get the name of the host where VM is running.
    :param vm: A Nova VM object.
     :type vm: *
    :return: The hostname.
     :rtype: str
    """
    return str(getattr(vm, 'OS-EXT-SRV-ATTR:host'))


"""
print  nova_client.hosts.list()
a=(nova_client.servers.list())

for i in a:
	print  i.id+"  " +i.name +"   " +  vm_hostname(i)

k= vms_by_host(nova, "node-2.domain.tld" )


"""
#data = nova_client.hosts.get("node-1.domain.tld")


"""
print  nova_client.hosts.list()
for i in nova_client.hosts.list():
	print i.host
"""
print "CPU utl" + "             " + "HOST" + "          " + "Used Space" +  "   "+ " CPU" + "       "+ "Used RAM"


def start():
	while True:
		for j in nova_client.hypervisors.list():
			a=[]
			gb=[]
			cores=[]
			#print i.hypervisor_hostname
			data = nova_client.hosts.get(j.hypervisor_hostname)
		
	
			for i in data:
				a.extend([i.memory_mb])
				gb.extend([i.disk_gb])
				cores.extend([i.cpu])
				number_vm=(len(cores) -3)
			cpu_util= float((a[1]*100)/a[0])
			#print vm_hostname("1")
			print str(cpu_util) + "         " + j.hypervisor_hostname + "         " + str(gb[1]) +  "         "+ str(cores[2]) + "          "+ str(a[1])	


			json_body = [
				    {
					"measurement": "cpu_util",
					"tags": {
					    "host": str(j.hypervisor_hostname)
					},
					"fields": {
					    "value": cpu_util
					}
				    }
				]

			json_body2 = [
				    {
					"measurement": "used space",
					"tags": {
					    "host": str(j.hypervisor_hostname)
					},
					"fields": {
					    "value": gb[1]
					}
				    }
				]


			json_body3 = [
				    {
					"measurement": "CPU",
					"tags": {
					    "host": str(j.hypervisor_hostname)
					},
					"fields": {
					    "value": cores[2]
					}
				    }
				]


			json_body4 = [
				    {
					"measurement": "Used ram",
					"tags": {
					    "host": str(j.hypervisor_hostname)
					},
					"fields": {
					    "value": a[1]
					}
				    }
				]



			client2.create_database('ANM3')
			client2.write_points(json_body)
			client2.write_points(json_body2)
			client2.write_points(json_body3)
			client2.write_points(json_body4)




		print "____________________________________________________________________"
		sleep(4)
