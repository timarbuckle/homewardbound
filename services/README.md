# Instructions
Link one of these files to /etc/systemd/system/

For example

    sudo ln -sf /home/tim/projects/homewardbound/services/cats.service.pi5 /etc/systemd/system/cats.service
    sudo systemctl daemon-reload
    sudo systemctl enable cats
    sudo systemctl start cats

Similar for user service, just add --user to the commands and place files in $HOME/.config/systemd/user/
