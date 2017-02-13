#WebLogic 12.2.1 infra (JRF) with SOA, BAM, OSB Cluster

with OSB & SOA with BPM, BAM, B2B & Enterprise schedular

##Details
- CentOS 6.5 vagrant box
- Puppet 3.5.0
- Vagrant >= 1.41
- Oracle Virtualbox >= 4.3.6

Download & Add the all the Oracle binaries to /software

edit Vagrantfile and update the software share to your own local folder
- soadb.vm.synced_folder "/Users/edwin/software", "/software"
- soa2admin2.vm.synced_folder "/Users/edwin/software", "/software"

Vagrant boxes
- vagrant up soadb
- vagrant up soa2admin2
- vagrant up mft1admin

## Database
- soadb 10.10.10.5, 11.2.0.4 with Welcome01 as password

###operating users
- root vagrant
- vagrant vagrant
- oracle oracle

###software
- Oracle Database 12.1.0.2 SE2 Linux
- linuxamd64_12102_database_se2_1of2.zip
- linuxamd64_12102_database_se2_2of2.zip

## Middleware

### default soa osb domain with 1 node
- soa2admin2 10.10.10.21, WebLogic 12.2.1 with Infra ( JRF, ADF, SOA, OSB ) requires RCU

http://10.10.10.21:7001/em with weblogic1 as password

###operating users
- root vagrant
- vagrant vagrant
- oracle oracle

###software
- JDK 1.8u121 jdk-8u121-linux-x64.tar.gz
- JDK 8 JCE policy jce_policy-8.zip
- fmw_12.2.1.2.0_infrastructure.jar
- fmw_12.2.1.2.0_osb_Disk1_1of1.zip
- fmw_12.2.1.2.0_soa_Disk1_1of1.zip

