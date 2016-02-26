PDFMiner
====

Python PDF Analyse System. Powered by Flask and MongoDB.

Get Started
-----------


Install independences:

    sudo apt-get install python-pip mongodb

    cd ~/pdfminer/

    sudo pip install -r requirements.txt

Start the website:

    python runserver.py


Production config:

    Change the code in 'runserver.py' 
        "USED_CONF = 'config.DevelopmentConfig'"
    to
        "USED_CONF = 'config.ProductionConfig'"
    and enter more than 15 different random characters in 'config.py'
        "SECRET_KEY" = 'SomeWordsYouLike12345'


License
-------

This software is free to use under the MIT license.
See the [LICENSE file][] for license text and copyright information.

[LICENSE file]: https://github.com/Dev-Engine/PDFMiner/blob/master/LICENSE


Dependencies
-------

Thanks to all other open-source projects(may not fully included).

[Flask](https://github.com/mitsuhiko/flask)

[Mongoengine](https://github.com/MongoEngine/mongoengine)

