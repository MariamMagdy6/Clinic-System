#Importing libraries
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *
import datetime

# Create an empty list to store patient information
patients = []

def main():
    # Set the title of the web application
    set_env(title='Clinic System')

    def register_patient():
        # Display the registration form
        put_html('<center><h3>Clinic System</h3></center>').style('background-color:#80AF81; padding:10px; color: #1A5319; font-weight: bold')
        put_html('<center><p>Web application to register patient information</p></center>').style('font-weight: bold')
        put_html('<center><img src="https://cdn.shopify.com/s/files/1/0588/6745/products/medi1_1480x800.jpg?v=1544087948" width="50%"></center>')

        # Get user input for patient information
        data = input_group(
            'Register Form',
            [
                input('Patient name', name='patient'),
                input('Patient Age', name='Age', type=NUMBER),
                input('Patient Address', name='Address'),
                input('Patient phone', name='phone', type=NUMBER),
                input('Date', name='Date', type=DATETIME, value=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                radio('First Visit?', options=['Yes', 'No'], name='visit')
            ],
        )

        # Get the uploaded ID image
        imgs = file_upload(
            'ID Upload',
            accept='image/*',
            multiple=False
        )

        # Store the image data
        pp = None
        if imgs:
            pp = imgs['content']

        # Create a dictionary to store the patient information
        patient_info = {
            'image': pp,
            'name': data['patient'],
            'age': data['Age'],
            'address': data['Address'],
            'phone': data['phone'],
            'date': data['Date'],
            'visit': data['visit']
        }

        # Add the patient information to the list
        patients.append(patient_info)
        clear()
        view_patients()

    def view_patients():
        # Display the patient information in a table format
        put_html('<center><h3>Patient Information</h3></center>').style('background-color:#80AF81; padding:10px; color: #1A5319; font-weight: bold')
        
        table_data = [
            ['ID Image', 'Name', 'Age', 'Address', 'Phone', 'Date', 'Visit', 'Actions']
        ]
        for idx, patient in enumerate(patients):
            row = [
                put_image(patient['image']).style('width:50px;') if patient['image'] else 'No image uploaded',
                patient['name'],
                patient['age'],
                patient['address'],
                patient['phone'],
                patient['date'],
                patient['visit'],
                put_buttons(['Edit', 'Delete'], onclick=[lambda x=idx: edit_patient(x), lambda x=idx: delete_patient(x)])
            ]
            table_data.append(row)
        put_table(table_data)
        put_buttons(['Register New Patient'], [lambda: clear() or register_patient()])

    def edit_patient(index):
        # Display the edit form for the selected patient
        patient = patients[index]
        data = input_group(
            'Edit Form',
            [
                input('Patient name', name='patient', value=patient['name']),
                input('Patient Age', name='Age', type=NUMBER, value=patient['age']),
                input('Patient Address', name='Address', value=patient['address']),
                input('Patient phone', name='phone', type=NUMBER, value=patient['phone']),
                input('Date', name='Date', type=DATETIME, value=patient['date']),
                radio('First Visit?', options=['Yes', 'No'], name='visit', value=patient['visit'])
            ],
        )

        # Get the updated ID image
        imgs = file_upload(
            'ID Upload',
            accept='image/*',
            multiple=False
        )

        # Update the patient information
        pp = patient['image']
        if imgs:
            pp = imgs['content']

        patient['image'] = pp
        patient['name'] = data['patient']
        patient['age'] = data['Age']
        patient['address'] = data['Address']
        patient['phone'] = data['phone']
        patient['date'] = data['Date']
        patient['visit'] = data['visit']
        clear()
        view_patients()

    def delete_patient(index):
        # Remove the selected patient from the list
        global patients
        patients.pop(index)
        clear()
        view_patients()

    # Start the registration process
    register_patient()

# Start the web server and run the main function
start_server(main, port=7200, debug=True)