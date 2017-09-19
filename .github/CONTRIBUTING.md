There's a ton of functionality in Ansible. If you're migrating from existing automation tools (e.g. shell scripts) a good rule of thumb is to assume it can all be done in Ansible with less headache and greater portability until proven otherwise.

When building roles:

* Aim for maximum compatibility. Don't use apt to install a Python module, if pip will accomplish the same.
* When adding distribution-specific commands, ensure you use conditionals to scope it.
* Make liberal use of inline documentation.
* Store any environment-specific data (local git root, ssh key location, etc.) in your-role/defaults/main.yml.
* Ensure that any dependencies are declared in your-role/meta/main.yml and that your dependency doesn't already exist under roles/common/tasks.
* Submit pull requests to the dev branch.
