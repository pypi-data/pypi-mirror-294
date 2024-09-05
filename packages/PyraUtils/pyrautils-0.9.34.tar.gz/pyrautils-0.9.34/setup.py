import os
import site
import sys
from setuptools import setup
from setuptools.command.install import install

# Allow editable install into user site directory.
# See https://github.com/pypa/pip/issues/7953.
site.ENABLE_USER_SITE = '--user' in sys.argv[1:]

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        self._warn_overlay_install()

    def _warn_overlay_install(self):
        overlay_warning = False
        lib_paths = [self.install_lib]
        if lib_paths[0].startswith("/usr/lib/"):
            # We have to try also with an explicit prefix of /usr/local in order to
            # catch Debian's custom user site-packages directory.
            lib_paths.append(self.install_lib.replace("/usr/lib/", "/usr/local/lib/"))
        for lib_path in lib_paths:
            existing_path = os.path.abspath(os.path.join(lib_path, "PyraUtils"))
            if os.path.exists(existing_path):
                overlay_warning = True
                break
        
        if overlay_warning:
            sys.stderr.write(f"""
========
WARNING!
========
You have just installed PyraUtils over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
PyraUtils. This is known to cause a variety of problems. You
should manually remove the
{existing_path}
directory and re-install PyraUtils.
""")

setup(
    cmdclass={
        'install': CustomInstallCommand,
    }
)
