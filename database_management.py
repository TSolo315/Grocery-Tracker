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
        print(name_list)
        return name_list

    def update_product(self, product_detail_list):
        product_name = product_detail_list[0]
        product_price = product_detail_list[1]
        product_category = product_detail_list[3]
        product_weight = product_detail_list[4]
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

    def push_transaction(self, product_detail_list, store, date):
        pass
