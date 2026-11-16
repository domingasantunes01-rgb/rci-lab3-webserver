# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
  config.ssh.insert_key = false
  # false: as Guest Additions 4.3 do trusty64 funcionam com o VirtualBox 7.2;
  # a actualizacao automatica falha no kernel 3.13 do trusty
  config.vbguest.auto_update = false
  config.ssh.forward_x11 = true

  config.vm.define "webserver" do |web_config|
    web_config.vm.box = "ubuntu/trusty64"
    web_config.vm.hostname = "webserver"
    web_config.vm.network "private_network", ip: "192.168.56.21"
    #web_config.vm.network "forwarded_port", guest: 80, host: 8080
    web_config.vm.synced_folder "html", "/home/vagrant/html"
    web_config.vm.provider "virtualbox" do |vb|
      vb.name = "lab3-webserver"  # nome no VirtualBox ("webserver" ja usado pelo LAB#2)
      opts = ["modifyvm", :id, "--natdnshostresolver1", "on"]
      vb.customize opts
      vb.memory = "256"
    end # of vb
    # web_config.vm.provision "shell", path: "bootstrap_web.sh"
   end # of web_config

   config.vm.define "client" do |client_config|
     client_config.vm.box = "ubuntu/trusty64"
     client_config.vm.hostname = "client"
     client_config.vm.network "private_network", ip: "192.168.56.11"
     client_config.vm.synced_folder "html", "/home/vagrant/html"
     client_config.vm.provider "virtualbox" do |vb|
       vb.name = "lab3-client"  # nome no VirtualBox ("client" ja usado pelo LAB#2)
       opts = ["modifyvm", :id, "--natdnshostresolver1", "on"]
       vb.customize opts
       vb.memory = "256"
     end # of vb
     client_config.vm.provision "shell", path: "bootstrap-client.sh"
   end # of client_config

end # of config
