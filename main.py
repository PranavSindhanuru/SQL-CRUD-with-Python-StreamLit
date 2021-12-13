import mysql.connector
import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

db = mysql.connector.connect(
    host="localhost", 
    user="root",
    passwd="root",
    database="dbms_mini_project"
    )

mycursor = db.cursor()

# mycursor.execute("CREATE TABLE guest (Guest_id int, First_name varchar(50), Last_name varchar(50), Address varchar(100), Phone_number varchar(30), Email_address varchar(50))")
# mycursor.execute("CREATE TABLE reservation (Reservation_id int, Guest_id int, Room_type_id int, Check_in varchar(50), Check_out varchar(50), Reservation_status int)")
# mycursor.execute("CREATE TABLE booking (Booking_id int, Room_Type_id int, Guest_id int, Check_in varchar(50), Check_out varchar(50))")
# mycursor.execute("CREATE TABLE room_type (Room_type_id int, Room_type varchar(50))")
# mycursor.execute("CREATE TABLE room (Room_id int, Room_number int, Room_type_Id int, Room_price int, Room_status int)")
# mycursor.execute("CREATE TABLE payment (Payment_id int, Guest_id int, Reservation_id int, Add_On varchar(50), Room_price int, Number_of_nights int, Total int, Payment_status int)")

# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)
mycursor.execute("SELECT * FROM guest")
guest = pd.DataFrame(mycursor.fetchall(), columns=['Guest ID', 'First Name', 'Last Name', 'Address', 'Phone number', 'Email'])

mycursor.execute("SELECT * FROM reservation")
reservation = pd.DataFrame(mycursor.fetchall(), columns=['Reservation ID', 'Guest ID', 'Room Type ID', 'Check IN', 'Check OUT', 'Reservation Status'])

mycursor.execute("SELECT * FROM booking")
booking = pd.DataFrame(mycursor.fetchall(), columns=['Booking Id', 'Room Type ID','Guest_ID', 'Check IN', 'Check OUT'])

mycursor.execute("SELECT * FROM room_type")
room_type = pd.DataFrame(mycursor.fetchall(), columns=['Room Type ID', 'Room Type'])

mycursor.execute("SELECT * FROM room")
room = pd.DataFrame(mycursor.fetchall(), columns=['Room ID', 'Room Number', 'Room Type ID', 'Room Price', 'Room Status'])

mycursor.execute("SELECT * FROM payment")
payment = pd.DataFrame(mycursor.fetchall(), columns=['Payment ID', 'Guest ID', 'Reservation ID', 'Add ON', 'Room Price', 'Number of Nights', 'Total', 'Payment Status'])

header = st.container()

with header:
    st.title('Tourist Inn Reservation System')

with st.form(key='datainput'):
    st.subheader('Add Data')
    guest_id = st.number_input('Guest ID', step=1, min_value=0)
    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    address = st.text_input('Address')
    ph_no = st.text_input('Phone number')
    email = st.text_input('Email Address')
    reservation_id = st.number_input('Reservation ID', step=1, min_value=0)
    room_type_id = st.number_input('Room Type ID', step=1, min_value=0)
    check_in = st.text_input('Check In')
    check_out = st.text_input('Check Out')
    reservation_status = st.number_input('Reservation Status', step=1, min_value=0, max_value=1)
    booking_id = st.number_input('Booking ID', step=1, min_value=0)
    room_id = st.number_input('Room ID', step=1, min_value=0)
    room_type_ = st.text_input('Room Type')
    room_number = st.number_input('Room Number', step=1, min_value=0)
    room_price = st.number_input('Room Price', step=1, min_value=0)
    room_status = st.number_input('Room Status', step=1, min_value=0, max_value=1)
    payment_id = st.number_input('Payment ID', step=1, min_value=0)
    add_on = st.text_input('Add on extra features')
    number_of_nights = st.number_input('Number of Nights', step=1, min_value=0)
    total = st.number_input('Total', step=1, min_value=0)
    payment_status = st.number_input('Payment Status', step=1, min_value=0, max_value=1)
    submit_button = st.form_submit_button()

if submit_button:
    with st.spinner('Running ....'):
        if guest_id != 0 and guest_id not in guest['Guest ID']:
            mycursor.execute("INSERT INTO guest VALUES (%s, %s, %s, %s, %s, %s)", (guest_id, first_name, last_name, address, ph_no, email))
        if reservation_id != 0:
            mycursor.execute("INSERT INTO reservation VALUES (%s, %s, %s, %s, %s, %s);", (reservation_id, guest_id, room_type_id, check_in, check_out, reservation_status))
        if booking_id != 0:
            mycursor.execute("INSERT INTO booking VALUES (%s, %s, %s, %s, %s);", (booking_id, room_type_id, guest_id, check_in, check_out))
        if room_type_id != 0:
            mycursor.execute("INSERT INTO room_type VALUES (%s, %s);", (room_type_id, room_type_))
        if room_id != 0:
            mycursor.execute("INSERT INTO room VALUES (%s, %s, %s, %s, %s);", (room_id, room_number, room_type_id, room_price, room_status))
        if payment_id != 0:
            mycursor.execute("INSERT INTO payment VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (payment_id, guest_id, reservation_id, add_on, room_price, number_of_nights, total, payment_status))
        db.commit()
    st.success('Done!')

st.button('Refresh Page')

st.write('GUEST')
guest

st.write('RESERVATION')
reservation

st.write('BOOKING')
booking

st.write('ROOM TYPE')
room_type

st.write('ROOM')
room

st.write('PAYMENTS')
payment

with st.form('deletedata'):
    st.subheader('Delete Row')
    table = st.selectbox('Table', ['Guest', 'Reservation', 'Booking', 'Room Type', 'Room', 'Payment'])
    str_x = table.lower().replace(' ', '_')
    str_x_id = str_x + '_id'
    id = st.number_input('ID', step=1, min_value=0)
    delete_button = st.form_submit_button('DELETE')

if delete_button:
    try:
        mycursor.execute(f"DELETE FROM {str_x} WHERE {str_x_id} = '{id}'")
        db.commit()
    except:
        print('Item doesn\'t exist')

with st.form(key='cleardata'):
    st.subheader('!! Clear All Data !!')
    st.write('warning! ⚠️ By pressing the clear button, all previous data will be erased ⚠️')
    clear_button = st.form_submit_button('CLEAR')

if clear_button:
    mycursor.execute("TRUNCATE guest")
    mycursor.execute("TRUNCATE reservation")
    mycursor.execute("TRUNCATE booking")
    mycursor.execute("TRUNCATE room_type")
    mycursor.execute("TRUNCATE room")
    mycursor.execute("TRUNCATE payment")
