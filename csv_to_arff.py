#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

from optparse import OptionParser
from collections import defaultdict

import arff


ARFF_TYPES = ('NUMERIC', 'STRING', 'NOMINAL', 'REAL', 'INTEGER')


#Exceptions
class NotEnoughTypesException(Exception):
    pass


class AttrMissingException(Exception):
    pass


class NotEnoughAttributesException(Exception):
    pass


def types_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


def check_selected_attrs(selected_attrs, header):
    """Check if the selected attrs are in the csv header."""
    for attr in selected_attrs:
            if attr not in header:
                raise AttrMissingException(attr)


def get_selected_colmumns_map(selected_attrs, header):
    selected_columns = []
    for attr in header:
        #list the selected columns
        if selected_attrs and attr not in selected_attrs:
            selected_columns.append(False)
        else:
            selected_columns.append(True)
    return selected_columns


def init_attributes_list(header, selected_column, type_list):
    #set the attributes
    attributes = []
    index = 0
    for selected, attr in zip(selected_columns, header):
        #list the selected columns
        if selected:
            attr = unicode(attr, 'utf-8')
            if index >= len(type_list):
                raise NotEnoughTypesException
            arff_type = type_list[index]
            if arff_type.upper() == "NOMINAL":
                tmp = (attr, [])
            else:
                tmp = (attr, arff_type)
            index += 1
            attributes.append(tmp)
    return attributes


def data_to_arff(data, type_list, relation_name, selected_attrs=None):
    """Reads a data matrix with first row as header, a list of arff types and
    returns a string with the arff format."""

    #this will be dictionria sent to to_arff module
    arff_content = defaultdict(list)

    #set relation
    arff_content['relation'] = relation_name

    is_nominal_column = [t.upper() == 'NOMINAL' for t in type_list]

    #get header
    header = data.next()
    attributes = []

    check_selected_attrs(selected_attrs, header)

    selected_columns = get_selected_colmumns_map(selected_attrs, header)

    attributes = init_attributes_list(header, selected_columns, type_list)

    assert len(attributes) > len(type_list)

    #create data rows
    arff_data = []
    index = 0
    for line in data:
        #only use the selected columns
        new_line = []
        for i, item in enumerate(line):
            if selected_columns[i]:
                if item != '':
                    new_line.append(unicode(item, 'utf-8'))
                else: #missing value, must be none not ''
                    new_line.append(None)

                assert i < len(is_nominal_column)
                #add to attributes if its nominal column
                if is_nominal_column[index] and item:
                    attributes[i][1].append(unicode(item, 'utf-8'))
                index += 1

        if len(type_list) != len(new_line):
            raise NotEnoughAttributesException
        #append new row to the data list
        arff_data.append(new_line)

    arff_content['attributes'] = attributes
    arff_content['data'] = arff_data
    return arff.dumps(arff_content)


def main():
    usage = "Usage: %prog <options>'"
    parser = OptionParser(usage=usage)

    parser.add_option('-r', '--relation-name',
                  type='string',
                  dest="relation",
                  help="the relation name")

    parser.add_option('-t', '--types',
                  type='string',
                  dest="typespec",
                  action='callback',
                  help="arff types list. e.g: NOMINAL,REAL,INTEGER,INTEGER",
                  callback=types_callback)

    parser.add_option('-a', '--attributes',
                  type='string',
                  dest="attrs",
                  action='callback',
                  help="atttributes to be procesed eg: casa,auto,cama\\larga",
                  callback=types_callback)


    parser.add_option("-f", "--file", dest="fileinput",
                  help="csv input file", metavar="FILE")

    #get args and option from commandline
    (options, args) = parser.parse_args()
    type_list = options.typespec
    fileinput = options.fileinput
    selected_attrs = options.attrs or []
    relation_name = options.relation

    #check relation name
    if not relation_name:
        parser.error(
            "Please specify a relation name e.g. -r test"
        )
    #the list of types and file input are mandatory
    if type_list and len(type_list) < 1:
        parser.error(
            "Please specify the list of arff types e.g. -t NOMINAL,STRING"
        )
    if not options.fileinput:
        parser.error("Please specify file input: -f example.csv")

    for arff_type in type_list:
        if arff_type.upper() not in ARFF_TYPES:
            #check is the types are legal
            parser.error("%s is not a legal type use %s" % (arff_type,
                                                            str(ARFF_TYPES)))
    try:
        with open(fileinput, 'r') as inputfile:
            data = csv.reader(inputfile, delimiter=',')
            print data_to_arff(data, type_list, relation_name, selected_attrs)

    except IOError:
        parser.error("the file %s does not exists" % options.fileinput)
    except NotEnoughTypesException:
        parser.error("there are more columns than types specified")
    except NotEnoughAttributesException:
        parser.error("there are more types than attributes specified")
    except AttrMissingException, e:
        parser.error("attribute '%s' not in csv header" % e)
    except arff.WrongTypeException, e:
        parser.error("Type Error, '%s' can't be a %s type.\n\nrow: %s" % (e[0], e[1], e[2]))

#main program
if __name__ == "__main__":
    main()
