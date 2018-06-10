
user_file = open("/home/pi/Project/Cofiguration files/record.txt","w")
yes = set(['yes','y', 'ye', ''])
no = set(['no','n'])
        
print('*********************Welcome to Registration Section**********************\n')
print('Kindly Enter the following Details to get registered with us\n')
name = raw_input('Please enter your name: ')
user_file.write('Name : %s'%str(name))
user_file.write('\n\n')
print('\n')
age = raw_input('Enter your age: ')

user_file.write('Age : %s'%str(age))
user_file.write('\n\n')
print('\n')
model = raw_input('Enter your Bike model: ')
user_file.write('Bike Model : %s'%model)
user_file.write('\n\n')
print('\n')
dl = raw_input('Enter your Driving license Number : ')
user_file.write('DL Number : %s'%str(dl))
user_file.write('\n\n')
print('\n')
emerge_no = raw_input('Enter the Emergency number to be contacted: ')

user_file.write('DL Expiry Date : %s'%dl)
user_file.write('\n\n')
print('\n')

Insure_no = raw_input('Enter the insurance no: ')

user_file.write('Insurance Number : %s'%Insure_no)
user_file.write('\n\n')
print('\n')
Insure_date = raw_input('Enter the Bike Insurance expiry date: \n\n')
user_file.write('insurance Date : %s'%Insure_date)
user_file.write('\n\n')

user_file.close()

        

