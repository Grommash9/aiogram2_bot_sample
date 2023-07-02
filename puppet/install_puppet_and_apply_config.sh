#!/bin/bash

# Обновление списка пакетов
sudo apt-get update

# Скачивание и установка репозитория Puppet
wget https://apt.puppetlabs.com/puppet7-release-focal.deb
sudo dpkg -i puppet7-release-focal.deb

# Обновление списка пакетов после установки репозитория Puppet
sudo apt update

# Установка пакета puppet-agent
sudo apt install puppet-agent -y

# Применение конфигурационного файла Puppet
sudo /opt/puppetlabs/bin/puppet apply python310.pp
