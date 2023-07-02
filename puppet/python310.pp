$bot_port = 2001
$bot_domain = 'aiogram-sample.telegram-crm.work'
$projectDirectory = '/home/aiogram2_bot_sample'
$certbotEmail = 'asda@gmail.com'
$databaseName = 'test_db'

# Устанавливаем Python 3.10 репозиторий
exec { 'install-python3.10':
  command => 'apt-get update && apt-get install -y python3.10',
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  creates => '/usr/bin/python3.10',
}

package { 'python3.10-dev':
  ensure => installed,
}

package { 'build-essential':
  ensure => installed,
}

package { 'default-libmysqlclient-dev':
  ensure => installed,
}

# Установка certbot и python3-certbot-nginx
package { 'certbot':
  ensure => installed,
}

package { 'python3-certbot-nginx':
  ensure => installed,
}

# Устанавливаем venv
package { 'python3-venv':
  ensure => installed,
}

# Установка пакета Redis
package { 'redis-server':
  ensure => installed,
}

# Запуск и включение службы Redis
service { 'redis-server':
  ensure => running,
  enable => true,
}

# Установка пакета Nginx
package { 'nginx':
  ensure => installed,
}

# Запуск и включение службы Nginx
service { 'nginx':
  ensure => running,
  enable => true,
}


# Конфигурация UFW и разрешение портов
exec { 'ufw-allow-ssh':
  command => 'sudo ufw allow 22',
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
}

exec { 'ufw-allow-nginx-full':
  command => 'sudo ufw allow "Nginx Full"',
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
}

exec { 'ufw-delete-nginx-http':
  command => 'sudo ufw delete allow "Nginx HTTP"',
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
}

exec { 'ufw-enable':
  command => 'sudo ufw enable',
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
}



# Проверяем конфигурацию Nginx с помощью nginx -t
exec { 'nginx-config-test':
  command     => 'nginx -t',
  path        => '/usr/sbin:/usr/bin:/sbin:/bin',
  refreshonly => true,
}

# Перезагружаем Nginx, если тест конфигурации успешен
exec { 'nginx-reload':
  command     => '/etc/init.d/nginx reload',
  refreshonly => true,
  subscribe   => Exec['nginx-config-test'],
}

# Определяем путь к файлу sites-available/default
$nginxConfigFile = '/etc/nginx/sites-available/default'

# Добавляем информацию в файл sites-available/default

# Создание директории sites-available
file { '/etc/nginx/sites-available':
  ensure => directory,
}

# Добавление информации в файл sites-available/default
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => template("${projectDirectory}/nginx_config.erb"),
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Выполнение certbot с настройкой Nginx
exec { 'certbot-nginx':
  command => "sudo certbot --nginx -d ${bot_domain} --email ${certbotEmail} --agree-tos --renew-by-default",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  creates => "/etc/letsencrypt/live/${bot_domain}/fullchain.pem"
}



# Установка пакета MySQL сервера
package { 'mysql-server':
  ensure => installed,
}

# Запуск и включение службы MySQL сервера
service { 'mysql':
  ensure => running,
  enable => true,
  require => Package['mysql-server'],
}

# Создание базы данных
exec { 'create-mysql-database':
  command => "mysql -e 'CREATE DATABASE IF NOT EXISTS ${databaseName}'",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  require => Service['mysql'],
}

# Загрузка дампа в базу данных
exec { 'load-mysql-dump':
  command => "mysql ${databaseName} < ${projectDirectory}/dump.sql",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  require => Exec['create-mysql-database'],
}

# Создание пользователя root с паролем "root"
exec { 'create-mysql-root-user':
  command => 'mysql -e "ALTER USER \'root\'@\'localhost\' IDENTIFIED WITH mysql_native_password BY \'root\'"',
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  require => Service['mysql'],
}


exec { 'change-directory-to-systemd':
  command => "bash -c 'cd ${projectDirectory}/systemd && python3.10 create_and_install_systemctl_files.py'",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  creates => "${projectDirectory}/systemd",
}

# Вход в директорию проекта
file { $projectDirectory:
  ensure  => directory,
}

exec { 'change-directory-to-venv':
  command => "bash -c 'cd ${projectDirectory}'",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  creates => "${projectDirectory}/env",
}

# Создание виртуального окружения с использованием Python 3.10
exec { 'create-venv':
  command => "/usr/bin/python3.10 -m venv ${projectDirectory}/env",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  creates => "${projectDirectory}/env/bin/activate",
  require => Exec['change-directory-to-venv'],
}

# Активация виртуального окружения и установка requirements
exec { 'install-dependencies':
  command => "${projectDirectory}/env/bin/pip install -r ${projectDirectory}/requirements.txt",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  require => Exec['create-venv'],
}

# Создание службы бота
exec { 'install-systemctl':
  command => "${projectDirectory}/env/bin/python ${projectDirectory}/systemd/create_and_install_systemctl_files.py",
  path    => '/usr/sbin:/usr/bin:/sbin:/bin',
  require => Exec['install-dependencies'],
}
