Getting started
---------------

* Install [Vagrant](http://vagrantup.com),
  [Fabric](http://fabric.readthedocs.org/en/latest/installation.html),
  and [fabtools](http://fabtools.readthedocs.org/en/latest/).

* Change config.ini to have your project name (currently called
  fab-tools-start-kit).  Only use letters, numbers, hyphens

* From the command line, run `vagrant up`. This will
  create and power up a virtual machine
  
* Run `fab dev provision`. This will install all the necessary packages
  on the virtual machine.

* SSH to the virtual machine with `vagrant ssh FabTools_StartKit` #
  project name from config.ini

* Put in any python or other unix tools you want in REQUIREMENTS or
  REQUIREMENTS-DEB

