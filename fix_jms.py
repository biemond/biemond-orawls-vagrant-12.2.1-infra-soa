
WLHOME         ='/opt/oracle/middleware12c/wlserver'
DOMAIN_PATH    ='/opt/oracle/wlsdomains/domains/soa_domain'

bpmEnabled     = true
bamEnabled     = true
soaEnabled     = true
osbEnabled     = true
b2bEnabled     = true
essEnabled     = true
y
SOAClusterName = 'SoaCluster'
BAMClusterName = 'BamCluster'
OSBClusterName = 'OsbCluster'
ESSClusterName = ''
Admin          = 'AdminServer'

AllClustersArray = []
if bamEnabled == true:
    AllClustersArray.append(BAMClusterName)
if soaEnabled == true:
    AllClustersArray.append(SOAClusterName)
if osbEnabled == true:
    AllClustersArray.append(OSBClusterName)
if essEnabled == true and ESSClusterName:
    AllClustersArray.append(ESSClusterName)

AllClusters  = ','.join(AllClustersArray)

def getClusterServers(cluster, adminserver_name):
    servers = []
    s = ls('/Server')
    clustername = " "
    for token in s.split("drw-"):
        token=token.strip().lstrip().rstrip()
        path="/Server/"+token
        cd(path)
        if not token == adminserver_name and not token == '':
            clustername = get('Cluster')
            searchClusterStr = cluster+":"
            clusterNameStr = str(clustername)
            if not clusterNameStr.find(searchClusterStr) == -1:
                servers.append(token)

    return servers

def createFileStore(storeName, serverName):
    create(storeName, 'FileStore')
    cd('/FileStore/'+storeName)
    set ('Target', serverName)
    set ('Directory', storeName)
    cd('/')

def createJMSServers(cluster, track, currentServerCnt, adminserver_name):
    print ' '
    print "Creating JMS Servers for the cluster :- ", cluster
    s = ls('/Server')
    print ' '
    clustername = " "
    serverCnt = currentServerCnt
    for token in s.split("drw-"):
        token=token.strip().lstrip().rstrip()
        path="/Server/"+token
        cd(path)
        if not token == adminserver_name and not token == '':
            clustername = get('Cluster')
            print "Cluster Associated with the Server [",token,"] :- ",clustername
            print ' '
            searchClusterStr = cluster+":"
            clusterNameStr = str(clustername)
            print "searchClusterStr = ",searchClusterStr
            print "clusterNameStr = ",clusterNameStr
            if not clusterNameStr.find(searchClusterStr) == -1:
                print token, " is associated with ", cluster
                print ' '
                print "Creating JMS Servers for ", track
                print ' '
                cd('/')

                if track == 'BamCQ':
                    jmsServerName = 'BamCQServiceJmsServer_auto_'+str(serverCnt)
                    fileStoreName = 'BamCQServiceJmsFileStore_auto_'+str(serverCnt)
                elif track == 'Bam':
                    jmsServerName = 'BamServerJmsServer_auto_'+str(serverCnt)
                    fileStoreName = 'BamServerJmsFileStore_auto_'+str(serverCnt)
                elif track == 'ums':
                    jmsServerName = 'UMSJMSServer_auto_'+str(serverCnt)
                    fileStoreName = 'UMSJMSServerFileStore_auto_'+str(serverCnt)


                createFileStore(fileStoreName, token)
                print "Created File Store :- ", fileStoreName

                create(jmsServerName, 'JMSServer')
                print "Created JMS Server :- ", jmsServerName
                print ' '
                assign('JMSServer', jmsServerName, 'Target', token)
                print jmsServerName, " assigned to server :- ", token
                print ' '
                cd('/JMSServer/'+jmsServerName)
                set ('PersistentStore', fileStoreName)

                serverCnt = serverCnt + 1

def getCurrentUMSServerCnt():
    s = ls('/JMSServer')
    count = s.count("UMSJMSServer_auto")
    return count + 1

def getClusterName(targetServer):
        targetServerStr = str(targetServer)
        s = ls('/Server')
        print ' '
        clustername = " "
        for token in s.split("drw-"):
                token=token.strip().lstrip().rstrip()
                path="/Server/"+token
                cd(path)
                if not token == 'AdminServer' and not token == '':
                        if not targetServerStr.find(token+":") == -1:
                                clustername = get('Cluster')
        return clustername

def getUMSJMSServers(cluster):
        s = ls('/JMSServers')
        jmsServersStr = " "
        print ' '
        clustername = " "
        for token in s.split("drw-"):
                token=token.strip().lstrip().rstrip()
                if not token == '' and not token.find("UMSJMSServer_auto") == -1:
                        cd('/JMSServers/'+token)
                        targetServer = get('Target')
                        clustername = getClusterName(targetServer)
                        searchClusterStr = cluster+":"
                        clusterNameStr = str(clustername)
                        print "searchClusterStr = ",searchClusterStr
                        print "clusterNameStr = ",clusterNameStr
                        if not clusterNameStr.find(searchClusterStr) == -1:
                                jmsServersStr = jmsServersStr + token + ","
        print "UMS JMS Servers for Cluster :- ", cluster , " is :- ", jmsServersStr
        return jmsServersStr

def cleanJMS(jms_module_pattern, jms_server_pattern, filestore_pattern):
  if jms_module_pattern:
    s = ls('/JMSSystemResources')
    for token in s.split("drw-"):
      token=token.strip().lstrip().rstrip()
      if not token == '' and not token.find(jms_module_pattern) == -1:
        print "token "+token
        try:
          delete(token, 'JMSSystemResource')
        except:
          print "delete of " + token + " jmsmodule failed", sys.exc_info()[0]
          pass

  if jms_server_pattern:
    s = ls('/JMSServers')
    for token in s.split("drw-"):
      token=token.strip().lstrip().rstrip()
      if not token == '' and not token.find(jms_server_pattern) == -1:
        print "token "+token
        try:
          delete(token, 'JMSServer')
        except:
          print "delete of " + token + " jmsserver failed", sys.exc_info()[0]
          pass

  if filestore_pattern:
    s = ls('/FileStore')
    for token in s.split("drw-"):
      token=token.strip().lstrip().rstrip()
      if not token == '' and not token.find(filestore_pattern) == -1:
        print "token "+token
        try:
          delete(token, 'FileStore')
        except:
          print "delete of " + token + " filestore failed", sys.exc_info()[0]
          pass



readDomain(DOMAIN_PATH)

cd('/')

if soaEnabled == true or bamEnabled == true or essEnabled == true:

    cleanJMS(None, None, 'UMSJMSServerFileStore_auto')
    cleanJMS('UMSJMSSystemResource', 'UMSJMSServer_auto', 'UMSJMSFileStore_auto')

    if soaEnabled == true:
        print "fix SOA UMS JMS"
        createJMSServers(SOAClusterName, 'ums', getCurrentUMSServerCnt(), Admin)

    if bamEnabled == true:
        print "fix BAM UMS JMS"
        createJMSServers(BAMClusterName, 'ums', getCurrentUMSServerCnt(), Admin)

    if osbEnabled == true:
        print "fix OSB UMS JMS"
        createJMSServers(OSBClusterName, 'ums', getCurrentUMSServerCnt(), Admin)

    if essEnabled == true and ESSClusterName:
        print "fix ESS UMS JMS"
        createJMSServers(ESSClusterName, 'ums', getCurrentUMSServerCnt(), Admin)


    print "create UMSJMSSystemResource"
    cd('/')
    create('UMSJMSSystemResource','JMSSystemResource')

    print "target UMSJMSSystemResource"
    cd('/')
    cd('JMSSystemResource/UMSJMSSystemResource')
    assign('JMSSystemResource', 'UMSJMSSystemResource', 'Target', AllClusters)

    print("*** Creating Connection Factories for UMS ***");
    cd('/')
    cd('JMSSystemResource/UMSJMSSystemResource/JmsResource/NO_NAME_0')

    cf1=create('OraSDPMQueueConnectionFactory','ConnectionFactory')
    cf1.setJNDIName('OraSDPM/QueueConnectionFactory')

    print ("*** Enabling XA ***")
    cd('/JMSSystemResource/UMSJMSSystemResource/JmsResource/NO_NAME_0/ConnectionFactory/OraSDPMQueueConnectionFactory')
    set('DefaultTargetingEnabled', 'true')
    create('TransactionParams', 'TransactionParams')
    cd('TransactionParams/NO_NAME_0')
    cmo.setXAConnectionFactoryEnabled(true)

    if soaEnabled == true:
        print "create subdeployment SOA UMS JMS"
        cd('/')
        cd('JMSSystemResource/UMSJMSSystemResource')
        create('UMSJMSSubDMSOA', 'SubDeployment')

        umsJMSServerStr = getUMSJMSServers(SOAClusterName)
        umsJMSServerStr = umsJMSServerStr.strip().lstrip().rstrip()
        assign('JMSSystemResource.SubDeployment', 'UMSJMSSystemResource.UMSJMSSubDMSOA', 'Target', umsJMSServerStr)

        print ("*** Creating Queues for UMS ***")
        cd('/')
        cd('JMSSystemResource/UMSJMSSystemResource/JmsResource/NO_NAME_0')
        print ' '

        udd=create('OraSDPMEngineSndQ1_soa','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMEngineRcvQ1_soa','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMDriverDefSndQ1_soa','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMDriverDefSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMAppDefRcvQ1_soa','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMAppDefRcvErrorQ1_soa','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvErrorQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMWSRcvQ1_soa','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMWSRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMEnginePendingRcvQ_soa','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEnginePendingRcvQ')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

    if bamEnabled == true:
        print "create subdeployment BAM UMS JMS"
        cd('/')
        cd('JMSSystemResource/UMSJMSSystemResource')
        create('UMSJMSSubDMBAM', 'SubDeployment')

        umsJMSServerStr = getUMSJMSServers(BAMClusterName)
        umsJMSServerStr = umsJMSServerStr.strip().lstrip().rstrip()
        assign('JMSSystemResource.SubDeployment', 'UMSJMSSystemResource.UMSJMSSubDMBAM', 'Target', umsJMSServerStr)

        print ("*** Creating Queues for UMS ***")
        cd('/')
        cd('JMSSystemResource/UMSJMSSystemResource/JmsResource/NO_NAME_0')
        print ' '

        udd=create('OraSDPMEngineSndQ1_bam','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMEngineRcvQ1_bam','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMDriverDefSndQ1_bam','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMDriverDefSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMAppDefRcvQ1_bam','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMAppDefRcvErrorQ1_bam','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvErrorQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMWSRcvQ1_bam','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMWSRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMEnginePendingRcvQ_bam','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEnginePendingRcvQ')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

    if osbEnabled == true:
        print "create subdeployment OSB UMS JMS"
        cd('/')
        cd('JMSSystemResource/UMSJMSSystemResource')
        create('UMSJMSSubDMOSB', 'SubDeployment')

        umsJMSServerStr = getUMSJMSServers(OSBClusterName)
        umsJMSServerStr = umsJMSServerStr.strip().lstrip().rstrip()
        assign('JMSSystemResource.SubDeployment', 'UMSJMSSystemResource.UMSJMSSubDMOSB', 'Target', umsJMSServerStr)

        print ("*** Creating Queues for UMS ***")
        cd('/')
        cd('JMSSystemResource/UMSJMSSystemResource/JmsResource/NO_NAME_0')
        print ' '

        udd=create('OraSDPMEngineSndQ1_osb','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMOSB')

        udd=create('OraSDPMEngineRcvQ1_osb','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMOSB')

        udd=create('OraSDPMDriverDefSndQ1_osb','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMDriverDefSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMOSB')

        udd=create('OraSDPMAppDefRcvQ1_osb','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMOSB')

        udd=create('OraSDPMAppDefRcvErrorQ1_osb','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvErrorQ1')
        udd.setSubDeploymentName('UMSJMSSubDMOSB')

        udd=create('OraSDPMWSRcvQ1_osb','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMWSRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMOSB')

        udd=create('OraSDPMEnginePendingRcvQ_osb','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEnginePendingRcvQ')
        udd.setSubDeploymentName('UMSJMSSubDMOSB')

    if essEnabled == true and ESSClusterName:
        print "create subdeployment ESS UMS JMS"
        cd('/')
        cd('JMSSystemResource/UMSJMSSystemResource')
        create('UMSJMSSubDMESS', 'SubDeployment')

        umsJMSServerStr = getUMSJMSServers(ESSClusterName)
        umsJMSServerStr = umsJMSServerStr.strip().lstrip().rstrip()
        assign('JMSSystemResource.SubDeployment', 'UMSJMSSystemResource.UMSJMSSubDMESS', 'Target', umsJMSServerStr)

        print ("*** Creating Queues for UMS ***")
        cd('/')
        cd('JMSSystemResource/UMSJMSSystemResource/JmsResource/NO_NAME_0')
        print ' '

        udd=create('OraSDPMEngineSndQ1_ess','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMESS')

        udd=create('OraSDPMEngineRcvQ1_ess','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMESS')

        udd=create('OraSDPMDriverDefSndQ1_ess','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMDriverDefSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMESS')

        udd=create('OraSDPMAppDefRcvQ1_ess','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMESS')

        udd=create('OraSDPMAppDefRcvErrorQ1_ess','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvErrorQ1')
        udd.setSubDeploymentName('UMSJMSSubDMESS')

        udd=create('OraSDPMWSRcvQ1_ess','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMWSRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMESS')

        udd=create('OraSDPMEnginePendingRcvQ_ess','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEnginePendingRcvQ')
        udd.setSubDeploymentName('UMSJMSSubDMESS')


updateDomain()
dumpStack()

closeDomain()
