Create a egg installation package at ./dist
name just like app_name-version-python_version.egg

    $python setup.py bdist-egg

Create a tar.gz installation package at ./dist, postfix with .tar.gz
name just like app_name-version.tar.gz

    $python setup.py sdist --formats=gztar

Install package from source code.
This mode will copy whole package to distination.
    $python setup.py install

Install package from source code with development mode.
This mode will create link to distination, not copy.

    $python setup.py develop

Install a egg package 

    $easy_install xxx.egg

Install a tar.gz package

    $easy_install xxx.tar.gz

Normally, package will install lib/pythonx.x/site-packages.
There is no uninstall option for this type of installation, so you need to remove associated files manually.

You could record installation path to a files.txt.
You can remove files and directories according to files.txt, when you want to uninstall.

    #Install and record
    $python setup.py install --record files.txt
    #uninstallation
    cat files.txt | xargs rm -rf 