from sql_connection import get_sql_connection
from datetime import datetime

def insert_order(connection,order):
    cursor=connection.cursor()
    query=("Insert into orders(Customer_name,Total,Datetime) VALUES (%s,%s,%s)")
    order_data=(order['Customer_name'],order['Total'],datetime.now())
    cursor.execute(query,order_data)
    
    order_id=cursor.lastrowid
    
    order_details_query=("insert into order_details(order_id,product_id,quantity,total_price) values (%s,%s,%s,%s)")
    order_details_data=[]
    
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
            float(order_detail_record['total_price'])
            
        ])
        
    cursor.executemany(order_details_query,order_details_data)
    connection.commit()
    
    return order_id

def get_all_orders(connection):
    cursor=connection.cursor()
    query=("Select * from orders")
    cursor.execute(query)
    response=[]
    for (order_id,Customer_name,Total,Datetime) in cursor:
       response.append({
           'order_id':order_id,
           'Customer_name': Customer_name,
           'Total':Total,
           'Datetime':Datetime
       })
    return response

if __name__=='__main__':
    connection=get_sql_connection()
    print(insert_order(connection,{
        'Customer_name': 'Mann',
        'Total': '3000',
        'Datetime': datetime.now(),
        'order_details': 
        [
            {
                'product_id':2,
                'quantity':3,
                'total_price':40
            },
            {
                'product_id':12,
                'quantity':3,
                'total_price':150
            }
        ]
    }))