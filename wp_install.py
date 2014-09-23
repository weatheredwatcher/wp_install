#!/bin/python

## This is a script to install a new instance of WordPress on the server.
## The syntax is wp_install domain_name

import os, sys, argparse, wget, tarfile
if not os.geteuid()==0:
    sys.exit("\nMust be run by root\n")
    
def main(argv):
    ##define options here
    server_root = '/var/www/vhosts/'
    plugin_path = '/var/resources/plugins/'
    theme_path = 'var/resources/themes/'
    domain = ''
    options = ''
        
    parser = argparse.ArgumentParser()
    parser.add_argument('domain')
    args = parser.parse_args(argv)
    domain = args.domain
##create folder    
    if not os.path.exists(server_root):
        print "Creating " + server_root
        os.makedirs(server_root)
##download wordpress
    download = wget.download('https://wordpress.org/latest.tar.gz')
    archive = tarfile.open(download, 'r:gz')
    archive.extractall(server_root)  
    os.rename("/var/www/vhosts/wordpress", "/var/www/vhosts/" + domain)    
##install base theme
##install base plugins
##create vhost file
    filename = domain + ".conf"
    target = open(filename, 'w')
    vhost = """
	<VirtualHost *:80>
	        ServerName %s
	        ServerAlias www.%s
	        DocumentRoot /var/www/%s
	        <Directory /var/www/%s>
	                Options -Indexes FollowSymLinks -MultiViews
	                AllowOverride All
	        </Directory>

	        CustomLog /var/log/httpd/%s-access.log combined
	        ErrorLog /var/log/httpd/%s-error.log

	        # Possible values include: debug, info, notice, warn, error, crit,
	        # alert, emerg.
	</VirtualHost>""" % (domain, domain, domain, domain, domain, domain)
    target.write(vhost)

if __name__ == "__main__":
    main(sys.argv[1:])