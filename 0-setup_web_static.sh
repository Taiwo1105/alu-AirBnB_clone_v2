#!/usr/bin/env bash
# Static website setup script

# Update and upgrade the system packages
sudo apt-get -y update
sudo apt-get -y upgrade

# Install Nginx if not already installed
sudo apt-get -y install nginx

# Create the necessary directories for the web content
sudo mkdir -p /var/www/web_static/releases/demo /var/www/web_static/shared

# Create a sample HTML file
echo "This is a sample HTML file." | sudo tee /var/www/web_static/releases/demo/sample.html

# Create a custom HTML file for Nginx configuration
echo "<!DOCTYPE html>
<html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\" />
        <title>Demo Page</title>
    </head>
    <body style=\"margin: 0px; padding: 0px;\">
        <header style=\"height: 70px; width: 100%; background-color: #0000FF\">
        </header>
        <footer style=\"position: absolute; left: 0; bottom: 0; height: 60px; width: 100%; background-color: #FFFF00; text-align: center; overflow: hidden;\">
            <p style=\"line-height: 60px; margin: 0px;\">Demo Company</p>
        </footer>
    </body>
</html>" | sudo tee /var/www/web_static/releases/demo/index.html

# Remove any existing symbolic link
sudo rm -rf /var/www/web_static/current

# Create a new symbolic link to the demo release
sudo ln -s /var/www/web_static/releases/demo/ /var/www/web_static/current

# Change ownership of the /var/www/ directory
sudo chown -R webuser:webuser /var/www/

# Update the Nginx configuration to serve content from the static directory
sudo sed -i '44i \\\n\tlocation /demo_static/ {\n\t\talias /var/www/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx to apply the new configuration
sudo service nginx restart

