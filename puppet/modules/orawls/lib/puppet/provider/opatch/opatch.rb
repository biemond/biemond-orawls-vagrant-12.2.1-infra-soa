
Puppet::Type.type(:opatch).provide(:opatch) do

  def self.instances
    []
  end

  def opatch(action)
    user                    = resource[:os_user]
    patchName               = resource[:patch_id]
    oracle_product_home_dir = resource[:oracle_product_home_dir]
    jdk_home_dir            = resource[:jdk_home_dir]
    extracted_patch_dir     = resource[:extracted_patch_dir]

    if action == :present
      command = "#{oracle_product_home_dir}/OPatch/opatch apply -silent -jre #{jdk_home_dir}/jre -oh #{oracle_product_home_dir} #{extracted_patch_dir}"
    else
      command = "#{oracle_product_home_dir}/OPatch/opatch rollback -id #{patchName} -silent -jre #{jdk_home_dir}/jre -oh #{oracle_product_home_dir}"
    end

    Puppet.debug "opatch action: #{action} with command #{command}"
    kernel = Facter.value(:kernel)
    su_shell = kernel == 'Linux' ? '-s /bin/bash' : ''

    if Puppet.features.root?
        output = `su #{su_shell} - #{user} -c '#{command}'`
    else
        output = `#{command}`
    end
    Puppet.debug "opatch result: #{output}"

    result = false
    output.each_line do |li|
      unless li.nil?
        if li.include? 'OPatch completed' or li.include? 'OPatch succeeded'
          result = true
        end
      end
    end
    fail(output) if result == false
  end

  def opatch_status
    user                    = resource[:os_user]
    patchName               = resource[:patch_id]
    oracle_product_home_dir = resource[:oracle_product_home_dir]
    orainst_dir             = resource[:orainst_dir]

    command  = oracle_product_home_dir + '/OPatch/opatch lsinventory -patch_id -oh ' + oracle_product_home_dir + ' -invPtrLoc ' + orainst_dir + '/oraInst.loc'
    Puppet.debug "opatch_status for patch #{patchName} command: #{command}"

    kernel = Facter.value(:kernel)
    su_shell = kernel == 'Linux' ? '-s /bin/bash' : ''
    
    if Puppet.features.root?
        output = `su #{su_shell} - #{user} -c '#{command}'`
    else
        output = `#{command}`
    end

    output.each_line do |li|
      opatch = li[5, li.index(':') - 5].strip if li['Patch'] && li[': applied on']
      unless opatch.nil?
        Puppet.debug "line #{opatch}"
        patchNum = patchName.to_i
        if opatch.to_i == patchNum
          Puppet.debug 'found patch'
          return patchName
        end
      end
    end
    'NotFound'
  end

  def present
    opatch :present
  end

  def absent
    opatch :absent
  end

  def status
    output  = opatch_status
    patchId = resource[:patch_id]
    Puppet.debug "opatch_status output #{output} for patchId #{patchId}"
    if output == patchId
      return :present
    else
      return :absent
    end
  end
end
