GENDER = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'),)
PAYMENT_MODE = (
    ('Cash on Delivery','Cash on Delivery'), 
    ('Credit/Debit Card', 'Credit/Debit Card'), 
    ('Mobile Wallet', 'Mobile Wallet'),
)
ORDER_STATUS = (
    ('Pending','Pending'),
    ('On Process', 'On Process'), 
    ('Hand over to courier', 'Hand over to courier'),
    ('Delivered', 'Delivered'), 
    ('Cancelled', 'Cancelled'), 
    ('Returned', 'Returned'), 
)
PAYMENT_STATUS = (
    ('Pending','Pending'),
    ('Partial Received', 'Partial Received'), 
    ('Received', 'Received'),
)

TYPE = (
    ('product','product'),
    ('gift-box', 'gift-box'), 
    ('general-box', 'general-box'),
    ('combo', 'combo'),
    ('external', 'external'),
)
BLOOD_GROUP = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('Golden Blood(Rh Null)', 'Golden Blood(Rh Null)'),
)
MARITAL_STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
    ('Separated ', 'Separated'),
)

USER_TYPE = (('Admin', 'Admin'), ('Customer', 'Customer'))
