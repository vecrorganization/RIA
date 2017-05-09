# Django
from django.test import TestCase
from django.contrib.auth.models import User
# Project
from ourAdmin.models import Table
from ourAdmin.forms import TableForm
from datetime import datetime

class TableSetUp(TestCase):
    """
    Set necessary data for Table
    """

    def setUp(self):
        self.modifier = User.objects.create_user(
                        'temporary', 'temporary@gmail.com', 'temporary'
                    )
        
    
class TableModelTestCase(TableSetUp):
    """
    Test case for Table model object creation
    """

    def test_Prod_model(self):
        self.assertTrue(Table.objects.create(
                            desc = 'descripcion',
                            type = 'CA',
                            refer = 0,
                            value1 = 1,
                            value2 = 2,
                            modifier = self.modifier,
                            createDate = datetime.now(),
                            modifyDate = datetime.now()
                        ))

class TableFormTestCase(TableSetUp):
    """
    Test cases for TableForm
    """
    
    def test_all_fields_filled(self):
        form_data = { 
                'desc':'descripcion',
                'type':'T',
                'refer':0,
                'value1':1,
                'value2':2
            }

        form = TableForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test cases for Mandatory Fields

    def test_mandatory_fields_filled(self):
        """
        Mandatory fields filled
        Form should be valid 
        """
        form_data = { 
                'desc':'descripcion',
                'type':'T'
            }

        form = TableForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_desc_empty(self):
        """
        Desc is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'type':'T',
                'refer':0,
                'value1':1,
                'value2':2
            }

        form = TableForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_type_empty(self):
        """
        Type is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'desc':'descripcion',
                'refer':0,
                'value1':1,
                'value2':2
            }

        form = TableForm(data=form_data)
        self.assertFalse(form.is_valid())







    # Test cases for Numeric Fields

    def test_refer_no_numeric(self):
        """
        Refer should be numeric. Otherwise, form is not valid.
        """
        form_data = { 
                'desc':'descripcion',
                'type':'T',
                'refer':'test',
                'value1':1,
                'value2':2
            }

        form = TableForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_value1_no_numeric(self):
        """
        Value1 should be numeric. Otherwise, form is not valid.
        """
        form_data = { 
                'desc':'descripcion',
                'type':'T',
                'refer':0,
                'value1':'test',
                'value2':2
            }

        form = TableForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_value2_no_numeric(self):
        """
        Value2 should be numeric. Otherwise, form is not valid.
        """
        form_data = { 
                'desc':'descripcion',
                'type':'T',
                'refer':0,
                'value1':1,
                'value2':'test'
            }

        form = TableForm(data=form_data)
        self.assertFalse(form.is_valid())




    # Test cases for non-blank Fields

    def test_desc_blank(self):
        """
        Desc should not be blank. Otherwise, form is not valid.
        """
        form_data = { 
                'desc':'',
                'type':'T',
                'refer':0,
                'value1':1,
                'value2':2
            }

        form = TableForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_type_blank(self):
        """
        Type should not be blank. Otherwise, form is not valid.
        """
        form_data = { 
                'desc':'descripcion',
                'type':'',
                'refer':0,
                'value1':1,
                'value2':2
            }

        form = TableForm(data=form_data)
        self.assertFalse(form.is_valid())