## pymortgage

The pymortgage application is an application that provides the ability to dynamically compare multiple different types of mortgages. There are lots of different mortgage calculators out there, but I've found none that allow you to do comparisons as granularly as this.

The project source is hosted here <http://github.com/csutherl/pymortgage> and I deploy a development build as I make major changes to on Openshift here <pymortgage-csutherl.rhcloud.com>. Feel free to visit and test it out!

For the latest version, to contribute, and for more information, please visit the project pages on GitHub, or the Openshift node.

### Technologies used

I used this project to learn HTML/CSS/JS with the Bootstrap and D3 charting libraries. In addition to that, I have also increased my understanding of python through this project and learned a bit about Openshift and how it works. The backend API is python which produces the data for the front end UI to chart and display.

### Reporting bugs

Please report any bugs or requested enhancements by opening an issue in the [GitHub Issue Tracker](https://github.com/csutherl/pymortgage/issues).

### Testing locally

If you'd like to run this locally, clone the current master (development):
~~~
git clone git://github.com/csutherl/pymortgage.git
~~~
and execute the following commands:
~~~
python setup.py install
python pymortgage/server/cherrypy_server.py
~~~
This will start the CherryPy server which you can hit by http://localhost:4001 (by default).
