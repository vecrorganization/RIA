# Django
from django.test import TestCase
from django.contrib.auth.models import User
# Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
# Project
from ourAdmin.models import Prod,Table,Seller
from ourAdmin.forms import ProdForm

class ProdSetUp(TestCase):
    """
    Set necessary data for Prod
    """

    def setUp(self):
        self.user = User.objects.create_user(
                        'temporary', 'temporary@gmail.com', 'temporary'
                    )
        self.category = Table.objects.create(desc='Frutas y verduras',type='CA',modifier=self.user)
        self.prod_class = Table.objects.create(desc='Todo',type='CL',modifier=self.user)
        self.tax = Table.objects.create(desc='Estandar',type='T',modifier=self.user)
        country = Table.objects.create(desc='Venezuela',type='CO',modifier=self.user)
        self.seller = Seller.objects.create(
                          eMail='seller@seller.com',
                          contactName='Contact',
                          contactPhone='02123698758',
                          contactMail='contact@seller.com',
                          country=country,
                          city='Caracas',
                          address='Las Bonitas',
                          modifier=self.user
                    )

        # create a new image using PIL
        im = Image.new(mode='RGB',size=(200,200),color=(255,0,0,0)) 
        # a BytesIO object for saving image
        im_io = BytesIO() 
        # save the image to im_io
        im.save(im_io, 'JPEG') 
        # seek to the beginning
        im_io.seek(0) 

        self.image = InMemoryUploadedFile(
            im_io, None, 'random-name.jpg', 'image/jpeg', im_io.__sizeof__(), None
        )
    
class ProdModelTestCase(ProdSetUp):
    """
    Test case for Prod model object creation
    """

    def test_Prod_model(self):
        self.assertTrue(Prod.objects.create(
                            id='123',
                            name='Prod1',
                            desc='Prod1',
                            price='1234',
                            category= self.category,
                            clase= self.prod_class,
                            width='100',
                            length='100',
                            height='100',
                            tax1=self.tax,
                            tax2=self.tax,
                            seller=self.seller,
                            modifier=self.user,
                            createDate='2016-09-22',
                            modifyDate='2016-09-30',
                            image_1 = self.image,
                            image_2 = self.image,
                            image_3 = self.image,
                            image_4 = self.image,
                            image_5 = self.image
                        ))


class ProdFormTestCase(ProdSetUp):
    """
    Test cases for ProdForm
    """
    
    def test_all_fields(self):
        """
        All fields filled
        Form should be valid 
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertTrue(form.is_valid())

    # Test cases for Mandatory Fields

    def test_mandatory_fields(self):
        """
        Mandatory fields filled
        Form should be valid 
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        form = ProdForm(data=form_data,files={ 'image_1': self.image })
        self.assertTrue(form.is_valid())

    def test_id_empty(self):
        """
        Id is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_name_empty(self):
        """
        Name is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    def test_desc_empty(self):
        """
        Desc is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    def test_price_empty(self):
        """
        Price is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_category_empty(self):
        """
        Category is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_clase_empty(self):
        """
        Class is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_tax1_empty(self):
        """
        Tax1 is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_tax2_empty(self):
        """
        Tax2 is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_seller_empty(self):
        """
        Seller is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_modifier_empty(self):
        """
        Modifier is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_image_1_empty(self):
        """
        Image_1 is a mandatory field. If it is empty, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'1234',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    # Test cases for Numeric Fields

    def test_price_no_numeric(self):
        """
        Price should be numeric. Otherwise, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'hola1',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    def test_width_no_numeric(self):
        """
        Width should be numeric. Otherwise, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'hola1',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_length_no_numeric(self):
        """
        Length should be numeric. Otherwise, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'hola1',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    def test_height_no_numeric(self):
        """
        height should be numeric. Otherwise, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'hola1',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    # Test cases for non-blank Fields

    def test_id_blank(self):
        """
        Price should not be blank. Otherwise, form is not valid.
        """
        form_data = { 
                'id':'',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_name_blank(self):
        """
        Name should not be blank. Otherwise, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    def test_desc_blank(self):
        """
        Desc should not be blank. Otherwise, form is not valid.
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    # Test cases for table type

    def test_category_type_tax(self):
        """
        Category field should be a Table object with CATEGORY type. 
        Otherwise, form is not valid.
        Test case with TAX instead
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.tax.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_category_type_class(self):
        """
        Category field should be a Table object with CATEGORY type. 
        Otherwise, form is not valid.
        Test case with CLASS instead
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.prod_class.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    def test_class_type_tax(self):
        """
        Class field should be a Table object with CLASS type. 
        Otherwise, form is not valid.
        Test case with TAX instead
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.tax.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_class_type_category(self):
        """
        Class field should be a Table object with CLASS type. 
        Otherwise, form is not valid.
        Test case with CATEGORY instead
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.category.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    def test_tax1_type_class(self):
        """
        Tax1 field should be a Table object with TAX type. 
        Otherwise, form is not valid.
        Test case with CLASS instead
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.prod_class.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_tax1_type_category(self):
        """
        Tax1 field should be a Table object with TAX type. 
        Otherwise, form is not valid.
        Test case with CATEGORY instead
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.category.id),
                'tax2':str(self.tax.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())


    def test_tax2_type_class(self):
        """
        Tax2 field should be a Table object with TAX type. 
        Otherwise, form is not valid.
        Test case with CLASS instead
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.prod_class.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())

    def test_tax2_type_category(self):
        """
        Tax1 field should be a Table object with TAX type. 
        Otherwise, form is not valid.
        Test case with CATEGORY instead
        """
        form_data = { 
                'id':'123',
                'name':'Prod1',
                'desc':'Prod1',
                'price':'123',
                'category': str(self.category.id),
                'clase': str(self.prod_class.id),
                'width':'100',
                'length':'100',
                'height':'100',
                'tax1':str(self.tax.id),
                'tax2':str(self.category.id),
                'seller':self.seller.eMail,
                'modifier': str(self.user.id)
            }

        images = {  'image_1': self.image,
                    'image_2': self.image,
                    'image_3': self.image,
                    'image_4': self.image,
                    'image_5': self.image
            }

        form = ProdForm(data=form_data,files=images)
        self.assertFalse(form.is_valid())