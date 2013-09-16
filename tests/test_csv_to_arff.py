# -*- coding: utf-8 -*-
import unittest

from csv_to_arff import (data_to_dict, init_attributes_list,
        get_selected_columns_map, AttrMissingException, check_selected_attrs)

class TestDataToArff(unittest.TestCase):

    def setUp(self):
        pass

    def test_normal(self):
        data = iter([['a','b','c'],['1','2', '3'],['4', '5', '6']])
        type_list = ['NOMINAL', 'STRING', 'INTEGER']
        relation_name = "testing"
        selected_attrs = ['a', 'b', 'c']
        result = data_to_dict(data, type_list, relation_name, selected_attrs)
        self.assertEqual(result['relation'], 'testing')
        self.assertEqual(result['attributes'], [(u'a', [u'1', u'4']),
            (u'b', 'STRING'), (u'c', 'INTEGER')])
        self.assertEqual(result['data'], [[u'1', u'2', u'3'], [u'4', u'5',
                                             u'6']])

    def test_no_attributes_selected(self):
        data = iter([['a','b','c'],['1','2', '3'],['4', '5', '6']])
        type_list = ['NOMINAL', 'STRING', 'INTEGER']
        relation_name = "testing"
        selected_attrs = []
        result = data_to_dict(data, type_list, relation_name, selected_attrs)
        self.assertEqual(result['relation'], 'testing')
        self.assertEqual(result['attributes'], [(u'a', [u'1', u'4']),
            (u'b', 'STRING'), (u'c', 'INTEGER')])
        self.assertEqual(result['data'], [[u'1', u'2', u'3'], [u'4', u'5',
                                             u'6']])

    def test_select_some_attributes(self):
        data = iter([['a','b','c'],['1','2', '3'],['4', '5', '6']])
        type_list = ['NOMINAL', 'INTEGER']
        relation_name = "testing"
        selected_attrs = ['a', 'c']
        result = data_to_dict(data, type_list, relation_name, selected_attrs)

        self.assertEqual(result['relation'], 'testing')
        self.assertEqual(result['attributes'], [(u'a', [u'1', u'4']),
                                                (u'c', 'INTEGER')])
        self.assertEqual(result['data'], [[u'1', u'3'], [u'4', u'6']])


    def test_missing_value(self):
        data = iter([['a','b','c'],['1','2', ''],['', '5', '6']])
        type_list = ['NOMINAL', 'INTEGER']
        relation_name = "testing"
        selected_attrs = ['a', 'c']
        result = data_to_dict(data, type_list, relation_name, selected_attrs)
        self.assertEqual(result['relation'], 'testing')
        self.assertEqual(result['attributes'], [(u'a', [u'1']),
                                                (u'c', 'INTEGER')])
        self.assertEqual(result['data'], [[u'1', None], [None, u'6']])


    def test_unicode(self):
        data = iter([['a','moño','cám'],['1','2', 'maña'],['', '5', 'cán']])
        type_list = ['NOMINAL', 'INTEGER', 'STRING']
        relation_name = "testing"
        selected_attrs = ['a', 'moño', 'cám']
        result = data_to_dict(data, type_list, relation_name, selected_attrs)

        self.assertEqual(result['relation'], 'testing')
        self.assertEqual(result['attributes'], [(u'a', [u'1']),
            (u'moño', 'INTEGER'), (u'cám', 'STRING')])
        self.assertEqual(result['data'], [[u'1', u'2', u'maña'],
                         [None, u'5', u'cán']])

    def test_init_attr_list(self):
        header = ['a', 'b', 'c']
        selected_columns = ['a', 'c']
        type_list = ['NOMINAL', 'STRING']
        result = init_attributes_list(header, selected_columns, type_list)
        self.assertEqual(result, [(u'a', []), (u'b', 'STRING')])


    def test_get_selected_columns_map(self):
        selected_attrs = ['a', 'c', 'e']
        header = ['a', 'b', 'c', 'd', 'e']
        result = get_selected_columns_map(selected_attrs, header)
        self.assertEqual(result, [True, False, True, False, True])

    def test_check_selected_attrs(self):
        selected_attrs = ['a', 'c', 'mono']
        header = ['a', 'b', 'c', 'd', 'e']
        self.assertRaises(AttrMissingException,
                          check_selected_attrs, selected_attrs, header)



if __name__ == '__main__':
    unittest.main()