# Floor Plan Coloring
Made By: Daniel Ivanovich

This program colors the various rooms of Andover High School (AHS) based off of their temperature. The program is being written in a way that, when complete, it *should*  work on **most** floor plans, as long as they meet the following requirements:

1. It is ans SVG file, with "selectable" text (you are able to highlight the text with your mouse)
2. The walls are black
3. The room numbers are not black
4. The room numbers are contained inside the walls

Here is an example of a properly formatted floor plan:

![Floor Plan](https://i.imgur.com/Mt1kolY.png)

If this functionality is implemented, temperature data should be inputted from a CSV file.

### Dependencies
If you want to run this script on your server (or something along those lines), it requires the following:
* [Colour](https://pypi.org/project/colour/)
* [Flask](http://flask.pocoo.org/)
* [Inkscape](https://inkscape.org/en/) (installed and added to the PATH)
* [Pandas](http://pandas.pydata.org/)
* [Pdfminer.six](https://pypi.org/project/pdfminer.six/) (A Python 3+ port of [pdfminer](https://pypi.org/project/pdfminer/))
* [PIL](https://pypi.org/project/PIL/) (Python Imaging Library)
* [PyPDF2](https://pypi.org/project/PyPDF2/)
* [Python 3+](https://www.python.org/downloads/)
* [Requests](http://docs.python-requests.org/en/master/)