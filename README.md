# YAMS Framework
Welcome to Yet Another Modular Security Framework. YAMS is a collection of Ansible roles, some hacky scripts, and a large amount of standing on the shoulders of giants.

# Thanks
YAMS is very much inspired by [The Penetration Tester's Framework](https://github.com/trustedsec/ptf) but attempts to build on the great work done there by adding strong support for environment-specific targeting (OS type, architecture, etc.), leveraging Ansible's solid module support for common tasks (git, apt, yum, etc.), and adding the ability to define a build script for easy deploy/rebuild.

## More Thanks
* https://leucos.github.io/ansible-files-layout for role layouts
* @pixel8ed for opening my eyes to the glory of automation with Ansible and sanity checking

# Getting Started
Getting started with YAMS is pretty straightforward. First, you're going to need to [install Ansible](https://docs.ansible.com/ansible/intro_installation.html#installing-the-control-machine) on your control machine. This is the system you'll use to configure your targets.

YAMS doesn't require any special configuration on the target - if you can SSH to it, you can configure it.

Once you've cloned the YAMS repo, you'll need to make a couple of changes:

1. Copy `templates\hosts.template` to `hosts`.
2. Update `hosts` with the appropriate IP/port for your target.
3. Update any `CHANGEME` values in `<module name>\defaults\main.yml` for modules you plan on using.

That's it! You can either tweak the sample `sample.yml` playbook to provision your first machine, or build your own.

Once you're happy with it, you can deploy your configuration using `ansible-playbook <playbook_name>.yml [--ask-become-pass]`.

## Keeping Things Current
Ansible makes it pretty simple to keep a role up to date. Once you've got things the way you want them, just make sure that you're making good use of `update: yes` and `state: latest` and then just re-run the playbook.

```
---
- name: Clone Empire
  become: true
  git:
    repo: https://github.com/EmpireProject/Empire.git
    dest: "{{ git_location }}/empire-git"
    update: yes

---
- name: Install pip
  become: true
  when: ansible_os_family ==  "Debian"
  apt:
    name: python-pip
    update_cache: yes
    state: latest
```

# The Plumbing
YAMS uses Ansible [roles](https://docs.ansible.com/ansible/playbooks_roles.html#roles) to define configurations for a host. A playbook is just a grouping of these roles to define the configuration of a system. YAMS provides the roles, you provide the targets.

Playbooks contain roles, roles contain plays, plays perform actions, and all of a sudden a box gets provisioned.

You can include a role in a playbook by adding it to the `roles` section:

```
---
- hosts: that_host
  remote_user: that_guy
  roles:
    - metasploit
    - sslscan
    - ...
    - kismet
```

Roles contain all the modular goodness we use to build playbooks. A role should define everything that needs to happen for the role to be succesfully provisioned on a target, including:

* Dependency on other roles
* Environment variables
* Service configurations
* Packages to install
* Files created (and contents edited!)

Roles can be simple:

```
# Installs Medusa
---
- name: Install Medusa
  become: true
  when: ansible_os_family ==  "Debian"
  apt:
    name: medusa
    update_cache: yes
```

Or a bit more involved:

```
---
# Installs and configures Metasploit
- name: Download Metasploit installer
  become: true
  get_url:
    url: https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb
    dest: /tmp/msfinstall
    mode: 0755

- name: Install Metasploit
  become: true
  command: /tmp/msfinstall

- name: Initialize Metasploit database
  command: msfdb init
```

Packaging tools as roles allows us to reuse them in different playbooks. That's the magic of YAMS. Build once, use all over the damn place.

## Role Structure
Here's how a basic role is structed in YAMS:

```
your-role/
├── docs.json          # Contains documentation for the role
├── defaults
│   └── main.yml       # Stores role-specific variables
├── files              # Stores any required files for your role
├── handlers
│   └── main.yml
├── meta
│    └── main.yml      # Declare dependencies here
└── tasks
    └── main.yml       # Imports and tags your role
    └── your-role.yml  # Contains all required plays for the role
```

The `main.yml` file under `tasks` is what is run when a role is added to a playbook. Rather than store all functionality in that, however, we just use it to import and tag actual role file — `your-role.yml`.

This may seem a bit silly but doing it this way allows us to selectively run roles from the playbook using `ansible-playbook your-playbook.yml --tags "your-role,another-role"`.

Using the `newmodule` command in YMS, you can create a basic role skeleton.

## Common Plays
Here's how to do some common operations using Ansible. You can get a full list of supported modules [here](https://docs.ansible.com/ansible/list_of_all_modules.html).

### Install a Package Using apt
```
- name: Install my-package
  become: true
  when: ansible_os_family ==  "Debian"
  apt:
    name: my-package
    update_cache: yes
    state: latest
```

The above command is the same as running `sudo apt update && sudo apt install my-package`. Re-running the task will update it (state: latest).

### Clone a Git Repository
```
- name: Clone my-repo
  become: true
  git:
    repo: https://github.com/foo/bar.git
    dest: /opt/bar-git
    update: yes
```

This is the same as running `sudo git clone https://github.com/foo/bar.git /opt/bar-git`. Re-running the task will perform a `git pull` operation (update: yes).

### Download Files
```
- name: Download my-file
  get_url:
    url: https://my.site/my-file.sh
    dest: /tmp/my-file.sh
    mode: 0755
```

The above command is the same as `wget https://my.site/my-file.txt -P /tmp && chmod 755 /tmp/my-file.txt`

### Run Commands
```
- name: Initialize Metasploit database
  command: msfdb init
```
This one is pretty straightforward.

## Targeting Using Conditionals
When adding distro-specific commands (e.g. `apt`, `yum`) to a play, make use of Ansible's [conditionals](https://docs.ansible.com/ansible/playbooks_conditionals.html) to target the commands appropriately.

For example:

```
- name: Install foo
  when: ansible_os_family ==  "Debian"
  apt:
    name: foo
    update_cache: yes
    state: latest
```

## Dependencies
You can easily implement a role dependency by defining that in `your-role/meta/main.yml` like so:

```
---
dependencies:
  - { role: autossh }
```

# Module Documentation
All module documentation can be found in either the module-level `docs.json` files, or using YMS.

# Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)