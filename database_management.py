import sqlite3


class DatabaseManager:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()

    def save(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_product_name_list(self):
        name_list = []
        for row in self.cursor.execute('''SELECT product_name
                            FROM product'''):
            name_list.append(row[0])
        return name_list

    def get_store_list(self):
        store_list = []
        for row in self.cursor.execute('''SELECT store_name, store_city
                            FROM store'''):
            store_list.append(" - ".join(row[0:2]))
        return store_list

    def get_user_list(self):
        user_list = []
        for row in self.cursor.execute('''SELECT username_name
                            FROM username'''):
            user_list.append(row[0])
        return user_list

    def update_product(self, product_detail_list):
        product_name = product_detail_list[0]
        product_price = product_detail_list[1]
        self.cursor.execute('''UPDATE product
         SET product_times_purchased = product_times_purchased + 1,
             product_highest_price = CASE WHEN product_highest_price < ? THEN (?) ELSE product_highest_price END,
             product_lowest_price = CASE WHEN product_lowest_price > ? THEN (?) ELSE product_lowest_price END,
             product_average_price = (product_average_price + ?) / 2
         WHERE product_name = ?''', (product_price, product_price, product_price, product_price, product_price, product_name))

    def push_product(self, product_detail_list):
        product_name = product_detail_list[0]
        product_price = product_detail_list[1]
        product_category = product_detail_list[3]
        product_weight = product_detail_list[4]
        self.cursor.execute('''INSERT INTO product
         (product_name, product_lowest_price, product_highest_price, product_average_price, product_times_purchased, product_category, product_weight_based_price)
          VALUES (?,?,?,?,?,?,?)''', (product_name, product_price, product_price, product_price, 1, product_category, product_weight))

    def push_transaction(self, product_detail_list, username, store, date):
        store = store.split(" - ")
        store_name = store[0]
        store_city = store[1]
        product_name = product_detail_list[0]
        product_price = product_detail_list[1]
        product_quantity = product_detail_list[2]
        self.cursor.execute('''INSERT INTO store_transaction
                 (username_id, store_id, product_id, transaction_price, transaction_quantity, transaction_date) VALUES ((SELECT username_id FROM username WHERE username_name = ?),
                  (SELECT store_id FROM store WHERE store_name = ? AND store_city = ?), (SELECT product_id FROM product WHERE product_name = ?),?,?,?)''',
                            (username, store_name, store_city, product_name, product_price, product_quantity, date))

    def push_transaction_summary(self, username, store, date, total):
        store = store.split(" - ")
        store_name = store[0]
        store_city = store[1]
        self.cursor.execute('''INSERT INTO transaction_summary
                        (username_id, store_id, summary_date, summary_total) VALUES ((SELECT username_id FROM username WHERE username_name = ?),
                         (SELECT store_id FROM store WHERE store_name = ? AND store_city = ?),?,?)''',
                            (username, store_name, store_city, date, total))

    def push_new_user(self, new_username):
        self.cursor.execute('''INSERT INTO username (username_name) VALUES (?)''', (new_username,))

    def push_new_store(self, name, address, address2, city, state, store_zip):
        self.cursor.execute('''INSERT INTO store (store_name, store_address, store_address, store_city, store_state, store_zip) VALUES (?,?,?,?,?,?)''', (name, address, address2, city, state, store_zip))

    def retrieve_report_query(self, user, store, item, category, date1, date2):
        result_list = []
        where_count = 0
        query_text = ["""SELECT * 
        FROM store_transaction INNER JOIN username on username.username_id = store_transaction.username_id
        INNER JOIN store on store.store_id = store_transaction.store_id
        INNER JOIN product on product.product_id = store_transaction.product_id"""]
        query_values = ()
        if user != "All Users":
            query_text.append("WHERE username_name = ?")
            query_values += (user,)
            where_count += 1
        if store != "All Stores":
            store = store.split(" - ")
            store_name = store[0]
            store_city = store[1]
            query_text.append("WHERE store_name = ?") if not where_count else query_text.append("AND store_name = ?")
            query_text.append("AND store_city = ?")
            query_values += (store_name, store_city)
            where_count += 1
        if item != "":
            query_text.append("WHERE product_name = ?") if not where_count else query_text.append("AND product_name = ?")
            query_values += (item,)
            where_count += 1
        if category != "All Categories":
            query_text.append("WHERE product_category = ?") if not where_count else query_text.append("AND product_category = ?")
            query_values += (category,)
            where_count += 1
        if date1:
            if date2:
                query_text.append("WHERE transaction_date >= ? AND transaction_date <= ?") if not where_count else query_text.append("AND transaction_date >= ? AND transaction_date <= ?")
                query_values += (date1, date2)
            else:
                query_text.append("WHERE transaction_date >= ?") if not where_count else query_text.append("AND transaction_date >= ?")
                query_values += (date1,)
            where_count += 1
        elif date2:
            query_text.append("WHERE transaction_date <= ?") if not where_count else query_text.append("AND transaction_date <= ?")
            query_values += (date2,)
            where_count += 1
        query_text = " ".join(query_text)
        print(query_text)
        print(query_values)
        for row in self.cursor.execute(query_text, query_values):
            result_list.append(row)
        return result_list
