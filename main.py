import streamlit as st
import pandas as pd
from PIL import Image
#from drug_db import *
import random

## SQL DATABASE CODE
import sqlite3




conn = sqlite3.connect("drug_data.db",check_same_thread=False)
c = conn.cursor()

def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table create Successfully')

def customer_add_data(Cname,Cpass, Cemail, Cstate,Cnumber):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_State, C_Number) VALUES(?,?,?,?,?)''', (Cname,Cpass,  Cemail, Cstate,Cnumber))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data
def customer_update(Cemail,Cnumber):
    c.execute(''' UPDATE Customers SET C_Number = ? WHERE C_Email = ?''', (Cnumber,Cemail,))
    conn.commit()
    print("Updating")
def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
    conn.commit()

def drug_update(Duse, Did):
    c.execute(''' UPDATE Drugs SET D_Use = ? WHERE D_id = ?''', (Duse,Did))
    conn.commit()
def drug_delete(Did):
    c.execute(''' DELETE FROM Drugs WHERE D_id = ?''', (Did,))
    conn.commit()

def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL, 
                D_id INT PRIMARY KEY NOT NULL)
                ''')
    print('DRUG Table create Successfully')

def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did):
    c.execute('''INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_id) VALUES(?,?,?,?,?)''', (Dname, Dexpdate, Duse, Dqty, Did))
    conn.commit()

def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data

def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL)
    ''')

def order_delete(Oid):
    c.execute(''' DELETE FROM Orders WHERE O_id = ?''', (Oid,))

def order_add_data(O_Name,O_Items,O_Qty,O_id):
    c.execute('''INSERT INTO Orders (O_Name, O_Items,O_Qty, O_id) VALUES(?,?,?,?)''',
               (O_Name,O_Items,O_Qty,O_id))
    conn.commit()


def order_view_data(customername):
    c.execute('SELECT * FROM ORDERS Where O_Name == ?',(customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM ORDERS')
    order_all_data = c.fetchall()
    return order_all_data






#__________________________________________________________________________________



def admin():


    st.title("Pharmacy Database Dashboard")
    st.subheader("Select an option from the menu to manage different aspects of the pharmacy database.")
    menu = ["Drugs", "Customers", "Orders", "About"]
    choice = st.sidebar.selectbox("Menu", menu)



    ## DRUGS
    if choice == "Drugs":

        st.subheader("Manage Drugs")
        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_area("When to Use")
            with col2:
                drug_quantity = st.text_area("Enter the quantity")
                drug_id = st.text_area("Enter the Drug id (example:#D1)")

            if st.button("Add Drug"):
                drug_add_data(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            #st.write(drug_result)
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(drug_clean_df)
            with st.expander("View Drug Quantity"):
                drug_name_quantity_df = drug_clean_df[['Name','Quantity']]
                #drug_name_quantity_df = drug_name_quantity_df.reset_index()
                st.dataframe(drug_name_quantity_df)
        if choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_area("Drug ID")
            d_use = st.text_area("Drug Use")
            if st.button(label='Update'):
                drug_update(d_use,d_id)

        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_area("Drug ID")
            if st.button(label="Delete"):
                drug_delete(did)



    ## CUSTOMERS
    elif choice == "Customers":

        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password","Email-ID" ,"Area", "Number"])
                st.dataframe(cust_clean_df)

        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email,cust_number)

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)

    elif choice == "Orders":
        menu = ["View"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()

            with st.expander("View All Order Data", expanded=True):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
                st.dataframe(order_clean_df.style.set_properties(**{'font-size': '16px'}))  # Larger font size inside the expander

        # Display order details outside the expander as well
        st.subheader("Order Details (Expanded)")
        st.dataframe(order_clean_df.style.set_properties(**{'font-size': '16px'}))  # Larger font size

    elif choice == "About":
        st.subheader("DBMS Mini Project")
        st.subheader("By Laxman and Arun")


def getauthenicate(username, password):
    #print("Auth")
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?', (username,))
    cust_password = c.fetchall()
    #print(cust_password[0][0], "Outside password")
    #print(password, "Parameter password")
    if cust_password[0][0] == password:
        #print("Inside password")
        return True
    else:
        return False


###################################################################

import csv  

def customer(username, password):
    if getauthenicate(username, password):
        
        print("In Customer")
        st.title("Welcome to Pharmacy Store")

        st.subheader("Your Order Details")
        order_result = order_view_data(username)
        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
            st.dataframe(order_clean_df)

        # Read drugs from CSV file
        drug_result = []
        with open('drugs.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                drug_result.append(row)

        for drug in drug_result:
            st.subheader(drug['D_Name'])
            img_path = 'images/' + drug['Image_Path']
            img = Image.open(img_path)
            st.image(img, width=400, caption="Rs. " + drug['D_Price'])
            
            quantity_slider = st.slider(label="Quantity", min_value=0, max_value=5, key=str(drug['D_id']))
            st.info("When to USE: " + drug['D_Use'])

        if st.button(label="Buy now"):
            O_items = ""
            O_Qty = ""
            for drug in drug_result:
                # Access session state using string conversion for D_id
                quantity = st.session_state[str(drug['D_id'])]
                if int(quantity) > 0:
                    O_items += drug['D_Name'] + ","
                    O_Qty += str(quantity) + ","
            O_id = username + "#O" + str(random.randint(0,1000000))
            order_add_data(username, O_items, O_Qty, O_id)

# def customer(username, password):
#     if getauthenicate(username, password):
        
#         print("In Customer")
#         st.title("Welcome to Pharmacy Store")

#         st.subheader("Your Order Details")
#         order_result = order_view_data(username)
#         # st.write(cust_result)
#         with st.expander("View All Order Data"):
#             order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
#             st.dataframe(order_clean_df)

#         drug_result = drug_view_all_data()
#         print(drug_result)


#         st.subheader("Drug: "+drug_result[0][0])
#         img = Image.open('images/dolo650.jpg')
#         st.image(img, width=400, caption="Rs. 15/-")
#         dolo650 = st.slider(label="Quantity",min_value=0, max_value=5, key= 1)
#         st.info("When to USE: " + str(drug_result[0][2]))


#         st.subheader("Drug: " + drug_result[1][0])
#         img = Image.open('images/strepsils.JPG')
#         st.image(img, width=400 , caption="Rs. 10/-")
#         strepsils = st.slider(label="Quantity",min_value=0, max_value=5, key= 2)
#         st.info("When to USE: " + str(drug_result[1][2]))

#         st.subheader("Drug: " + drug_result[2][0])
#         img = Image.open('images/vicks.JPG')
#         st.image(img, width=400, caption="Rs. 65/-")
#         vicks = st.slider(label="Quantity",min_value=0, max_value=5, key=3)
#         st.info("When to USE: " + str(drug_result[2][2]))



#         if st.button(label="Buy now"):
#             O_items = ""

#             if int(dolo650) > 0:
#                 O_items += "Dolo-650,"
#             if int(strepsils) > 0:
#                 O_items += "Strepsils,"
#             if int(vicks) > 0:
#                 O_items += "Vicks"
#             O_Qty = str(dolo650)+str(',') + str(strepsils) + str(",") + str(vicks)

#             O_id = username + "#O" + str(random.randint(0,1000000))
#             #order_add_data(O_Name, O_Items,O_Qty, O_id):
#             order_add_data(username, O_items, O_Qty, O_id)








if __name__ == '__main__':
    drug_create_table()
    cust_create_table()
    order_create_table()

    menu = ["Login", "SignUp","Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            customer(username, password)
    
    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_area("Email ID", placeholder="Enter your email")
        with col2:
            cust_area = st.text_area("State", placeholder="Enter your state")
        with col3:
            cust_number = st.text_area("Phone Number", placeholder="Enter your phone number")

        if st.button("Signup"):
            if (cust_password == cust_password1):
                customer_add_data(cust_name,cust_password,cust_email, cust_area, cust_number,)
                st.success("Account Created Successfully!")
                st.info("Go to the Login Menu to log in")
            else:
                st.warning('Passwords do not match. Please try again.')
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        # if st.sidebar.button("Login"):
        if username == 'admin' and password == 'admin':
            admin()
