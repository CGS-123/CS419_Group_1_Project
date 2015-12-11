CS 419 Group 1 F15
Colin Smith, Jesse Smidt, Alex Thomas

If you are running the program through vagrant.  After installing vagrant and following the necessary steps for vagrant to run on your OS.  Open a terminal inside the code directory which contains Vagrantfile.  Simply type vagrant up.  Vagrant will now begin downloading and running necessary commands to provision this VM.
After issuing the vagrant up command the VM is now working and ready to be accessed.  You can SSH into the VM by typing vagrant ssh (if prompted, the password is “vagrant”).
Vagrant is set up to share the repository where the Vagrantfile is located.  If you were running this on your own server you would need to copy the code file over to the server with postgresql 9.3 already installed.  Navigate to the code file, in case of vagrant the directory is simply /vagrant

To run the program type python main.py  

A welcome animation displays and then the user can choose to login or create an account.
user: vagrant pass:vagrant  has prepopulated database worlddb in it.