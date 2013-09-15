=========
CsvToArff
=========

The csv_to_arff is a script that turn csv filt to arff file.

Attribute Relationship File Format (`ARFF <http://weka.wikispaces.com/ARFF>`_ )
is the text format file used by Weka to store data in a database.

to generate the arff files we need:

- install (`liac-arff https://github.com/renatopp/liac-arff/`_ )


Features
--------

- Script to turn csv to arff file.
- Supports NUMERIC, REAL, INTEGER, STRING and NOMINAL attribute types;
- Supports names with space;
- LGPL license;


Install
-------

pre-requistes::

    $ git clone git@github.com:renatopp/liac-arff.git
    $ cd liac-arff/
    $ python2.7 setup.py install

install csv_to_arff::

	$ git clone git@github.com:flecox/CsvToArff.git
	$ cd CsvToArff/
    $ python2.7 setup.py install


csv to Arff script
-------------------

To be able to convert a csv to Arff file, you must suplly the list of arff types, the name of the relation, and te file input::


	>csv_to_arff.py -t NOMINAL,STRING,INTEGER -f input.csv -r my_relation

If you don't want to use all the attributes in the csv file. we must declare it like this::

	>csv_to_arff.py -t NOMINAL,STRING,INTEGER -f input.csv -r my_relation -a genre,last\ name,age

if you set one of the attributes as nominal, the script will automatically set all the values of that column as the possible values of that attribute.

for help::

	> csv_to_arff.py --help
	Usage: csv_to_arff.py <options>

	Options:
	  -h, --help            show this help message and exit
	  -r RELATION, --relation-name=RELATION
	                        the relation name
	  -t TYPESPEC, --types=TYPESPEC
	                        arff types list. e.g: NOMINAL,REAL,INTEGER,INTEGER
	  -a ATTRS, --attributes=ATTRS
	                        atttributes to be procesed eg: casa,auto,cama\larga
	  -f FILE, --file=FILE  csv input file


Contributors
------------

- `Gonzalo Almeida (flecox) flecox AT gmail.com`_