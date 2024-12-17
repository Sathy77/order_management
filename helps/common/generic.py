from helps.common.mini import Minihelps
from datetime import datetime, date, timedelta
from helps.choice import common as CHOICE
import calendar

class Generichelps(Minihelps):

    # ORDER
    # def checkUser(self, User, Userserializer, data, contact_no):
    #     response = {'message': [], 'combo_name': '', 'given_combo_quantity': '' }
    #     if not user.exists():
    #         allowed_fields = ['name', 'address', 'contact_no', 'email']
    #         extra_fields = {'username': contact_no, 'password': make_password(f'PASS{contact_no}'), 'user_type': CHOICE.USER_TYPE[1][1], 'created_by': userid, 'updated_by': userid}
    #         required_fields = ['name', 'address', 'contact_no']
    #         fields_regex = [{'field': 'contact_no', 'type': 'phonenumber'}]
    #         unique_fields=['contact_no']
    #         responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
    #             classOBJ=User,
    #             Serializer=Userserializer,
    #             data=data,
    #             allowed_fields=allowed_fields,
    #             required_fields=required_fields,
    #             unique_fields=unique_fields,
    #             extra_fields=extra_fields,
    #             fields_regex=fields_regex
    #         )
    #         if responsesuccessflag == 'success': user = responsedata.instance
    #         elif responsesuccessflag == 'error': response.extend(responsemessage)
    #     elif user.exists(): 
    #         user = user.first()
    #         data['contact_no'] = contact_no
    #         extra_fields = {}
    #         if userid: extra_fields.update({'updated_by': userid})
    #         allowed_fields=['name', 'address', 'contact_no', 'email']
    #         # freez_update = [{'user_type': 'Admin'}]  //user type admin paile purai r update korte dibe na
    #         responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
    #             classOBJ=User, 
    #             Serializer=Userserializer, 
    #             id=user.id,
    #             data=data,
    #             allowed_fields = allowed_fields,
    #             unique_fields=['contact_no'],
    #             # freez_update=freez_update,
    #             extra_fields=extra_fields
    #         )
    #         if responsesuccessflag == 'success': user = responsedata.instance
    #         elif responsesuccessflag == 'error': response.extend(responsemessage)


    def purifyCombos(self, Product, data):
        response = {'message': [], 'combo_name': '', 'given_combo_quantity': '' }
        combo_boxid = data.get('combo_box')
        given_combo_quantity = data.get('combo_quantity')
        if combo_boxid:
            combo_box = Product.objects.filter(id=combo_boxid) 
            if combo_box.exists():
                combo_names = combo_box.first().name
                combo_capacity = combo_box.first().capacity
                combo_quntity = combo_box.first().quntity
                given_combo_capacity = data.get('combo_capacity')
                if given_combo_capacity:
                    if combo_capacity >= given_combo_capacity:
                        products = data.get('products')
                        if products:
                            given_combo_quantity = data.get('combo_quantity')
                            if given_combo_quantity:
                                if combo_quntity >= given_combo_quantity:
                                    totalproduct = 0
                                    for product in products:
                                        order_quantity = product.get('order_quantity')
                                        product['order_quantity'] = order_quantity * given_combo_quantity
                                        if order_quantity:
                                            totalproduct += order_quantity
                                    if totalproduct <= given_combo_capacity:
                                        response['combo_name'] = combo_names
                                        response['given_combo_quantity'] = given_combo_quantity
                                    else: response['message'].append('totalproductquantity and  combo_capacity not same!')
                                else:  response['message'].append('combo_box_quantity is less than  quantity!')
                            else: response['message'].append('is_combo is true then combo_quantity is required!') 
                        else: response['message'].append('products list is required!')    
                    else: response['message'].append('combo_capacity is less then given combo_capacity!')       
                else: response['message'].append('is_combo is true then combo_capacity is required!')   
            else: response['message'].append('combo_boxid is not valid!')
        else: response['message'].append('combo_box is required!')
        return response
    
    def purifyProducts(self, Product, data):
        response = {'message': [], 'products': {}}
        products = data.get('products')
        if products:
            if isinstance(products, list):
                for product in products:
                    order_quantity = product.get('order_quantity')
                    if isinstance(order_quantity, str):
                        if order_quantity.isnumeric(): order_quantity = int(order_quantity)
                        else:
                            response['message'].append(f'order_quantity should be type of int!')
                            break
                    else:
                        if not isinstance(order_quantity, int):
                            response['message'].append(f'order_quantity should be type of int!')
                            break
                    productid = product.get('id')
                    if productid:
                        product = Product.objects.filter(id=productid)
                        if product.exists():
                            if product.first().costprice:
                                if product.first().mrpprice:
                                    if product.first().quntity:
                                        if product.first().quntity>=order_quantity:
                                            response['products'].update({str(product.first().id): {'product': product, 'quantity': order_quantity}})
                                        else:
                                            response['message'].append(f'less products are available({product.first().quntity}) then required({order_quantity})!')
                                            break
                                    else:
                                        response['message'].append(f'quntity doesn\'t exist, product id({productid})!')
                                        break
                                else:
                                    response['message'].append(f'mrpprice doesn\'t exist, product id({productid})!')
                                    break
                            else:
                                response['message'].append(f'costprice doesn\'t exist, product id({productid})!')
                                break
                        else:
                            response['message'].append(f'product doesn\'t exist with this id({productid})!')
                            break
                    else:
                        response['message'].append('please provide productid!')
                        break
            else: response['message'].append('products type should be list!')
        else: response['message'].append('products list is required!')
        return response

    def calculateComboBoxCalculationauth(self,combobox, combo_quantity, products, discount, is_fiexd_amounts, deliverycost):
        product_cost = 0
        trade_cost = 0

        combobox_unit_mrp = combobox.first().mrpprice
        total_combobox_mrp = combobox_unit_mrp*combo_quantity
        combobox_unit_cost = combobox.first().costprice
        total_combobox_cost = combobox_unit_cost*combo_quantity
        
        for productkey in products.keys():
            product = products[productkey]['product']
            order_quantity = products[productkey]['quantity']

            unit_trade_price = product.first().costprice
            unit_mrp = product.first().mrpprice

            product_cost +=  unit_mrp*order_quantity
            trade_cost += unit_trade_price*order_quantity
        # product_cost -= discount
        if is_fiexd_amounts:
            discount_total = discount
            # product_cost -= discount_total
                   
        else:
            discount_total = product_cost * discount/100
        
        grand_total = product_cost + deliverycost + total_combobox_mrp
        grand_total -= discount_total
        product_cost += total_combobox_mrp
        trade_cost += total_combobox_cost
        total_profit = (product_cost - discount_total ) - trade_cost
        return product_cost, grand_total, total_profit, discount_total    

    # ORDER
    def calculateProductCalculation(self, products, discount, deliverycost):
        product_cost = 0
        trade_cost = 0

        for productkey in products.keys():
            product = products[productkey]['product']
            order_quantity = products[productkey]['quantity']

            unit_trade_price = product.first().costprice
            unit_mrp = product.first().mrpprice

            product_cost +=  unit_mrp*order_quantity
            trade_cost += unit_trade_price*order_quantity
        # product_cost -= discount
        
        grand_total = product_cost + deliverycost
        grand_total -= discount
        total_profit = (product_cost - discount) - trade_cost
        return product_cost, grand_total, total_profit
    
    def calculateProductCalculationauth(self, products, discount, is_fiexd_amounts, deliverycost):
        product_cost = 0
        trade_cost = 0

        for productkey in products.keys():
            product = products[productkey]['product']
            order_quantity = products[productkey]['quantity']

            unit_trade_price = product.first().costprice
            unit_mrp = product.first().mrpprice

            product_cost +=  unit_mrp*order_quantity
            trade_cost += unit_trade_price*order_quantity
        
        if is_fiexd_amounts:
            discount_total = discount
            # product_cost -= discount_total
                   
        else:
            discount_total = product_cost * discount/100
            # product_cost -= discount_total

        grand_total = product_cost + deliverycost
        grand_total -= discount_total
        total_profit = (product_cost -discount_total) - trade_cost
        return product_cost, grand_total, total_profit, discount_total

    def getPermissionsList(self, User, username, permissions, all=False, active=False, inactive=False):
        if all + active + inactive == 1:
            user = User.objects.filter(username=username)
            if user.exists():
                user = user.first()
                if user.is_active:
                    if all: self.getPermissionsListIfAll(permissions, user)
                    elif active: self.getPermissionsListIfActiveOrInactive(permissions, user, True)
                    else: self.getPermissionsListIfActiveOrInactive(permissions, user, False)

    def filterClass(self, Object, request, extra_conditions={}):
        kwargs={}
        for key in request.GET.keys():
            if request.GET[key]:
                if key in extra_conditions: kwargs.update({'{0}__{1}'.format(key, extra_conditions[key]): request.GET[key]})
                else: kwargs.update({'{0}'.format(key): request.GET[key]})
        objects = Object.objects.filter(**kwargs)
        return objects
    
    def prepareData(self, objects, fieldsname): # New
        preparedData = []

        if fieldsname == 'product': fields = self.getProductData()
        if fieldsname == 'setting': fields = self.getSettingData()
        

        if isinstance(objects, dict):
            preparedData.append(self.getOBJDetails(objects, fields))

        if isinstance(objects, list):
            carrierList = []
            for object in objects:
                preparedObj = self.getOBJDetails(object, fields)
                if preparedObj: carrierList.append(preparedObj)
            if carrierList: preparedData.append(carrierList)

        return preparedData[0] if preparedData else None
    





















































































    def createuser(self, classOBJpackage, serializerOBJpackage, createdInstance, personalDetails, officialDetails, salaryAndLeaves, photo, created_by): # New
        response = {'flag': True, 'message': []}
        
        details = self.getuserdetails(classOBJpackage, serializerOBJpackage, createdInstance, personalDetails, officialDetails, salaryAndLeaves, photo, created_by)
        if not details['flag']: response['flag'] = False
        response['message'].extend(details['message'])

        if response['flag']:
            required_fields = ['username', 'password', 'first_name', 'official_id']
            unique_fields = ['personal_email', 'personal_phone', 'nid_passport_no', 'tin_no', 'official_id', 'official_email', 'official_phone', 'rfid']
            choice_fields = [
                {'name': 'blood_group', 'type': 'single-string', 'values': [item[1] for item in CHOICE.BLOOD_GROUP]},
                {'name': 'marital_status', 'type': 'single-string', 'values': [item[1] for item in CHOICE.MARITAL_STATUS]},
                {'name': 'gender', 'type': 'single-string', 'values': [item[1] for item in CHOICE.GENDER]},
                {'name': 'employee_type', 'type': 'single-string', 'values': [item[1] for item in CHOICE.EMPLOYEE_TYPE]},
                {'name': 'payment_in', 'type': 'single-string', 'values': [item[1] for item in CHOICE.PAYMENT_IN]},
                {'name': 'job_status', 'type': 'single-string', 'values': [item[1] for item in CHOICE.JOB_STATUS]}
            ]
            fields_regex = [
                {'field': 'dob', 'type': 'date'},
                {'field': 'personal_email', 'type': 'email'},
                {'field': 'personal_phone', 'type': 'phonenumber'},
                {'field': 'official_id', 'type': 'employeeid'},
                {'field': 'official_email', 'type': 'email'},
                {'field': 'official_phone', 'type': 'phonenumber'},
                {'field': 'joining_date', 'type': 'date'}
            ]
            responsedata, responsemessage, responsesuccessflag, responsestatus = self.addtocolass(
                classOBJ=classOBJpackage['User'],
                Serializer=serializerOBJpackage['User'],
                data=details['data'],
                required_fields=required_fields,
                unique_fields=unique_fields,
                choice_fields=choice_fields,
                fields_regex=fields_regex
            )
            if responsesuccessflag == 'error':
                response['flag'] = False
                response['message'].extend(responsemessage)
                response['message'].append('couldn\'t create user instance, something went wrong!')
            if responsesuccessflag == 'success':
                response['message'].extend(responsemessage)
                response.update({'userinstance': responsedata.instance})
        return response
    

    