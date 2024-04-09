import os
import csv
from tabulate import tabulate


class PriceManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.prices = []
        self.last_search_results = []
        self.load_prices()

    def load_prices(self):
        for filename in os.listdir(self.folder_path):
            if "price" in filename.lower():
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=',')
                    for row in reader:
                        product_name = self.get_column_value(row, ['название', 'продукт', 'товар', 'наименование'])
                        price = self.get_float_column_value(row, ['цена', 'розница'])
                        weight = self.get_float_column_value(row, ['фасовка', 'масса', 'вес'])
                        if product_name and price and weight is not None:
                            self.prices.append((product_name, price, weight, filename))

    def get_column_value(self, row, column_names):
        for column_name in column_names:
            if column_name in row:
                return row[column_name]
        return None

    def get_float_column_value(self, row, column_names):
        for column_name in column_names:
            if column_name in row and row[column_name]:
                try:
                    return float(row[column_name].replace(',', '.'))
                except ValueError:
                    pass
        return None

    def find_text(self, text):
        result = []
        for product_name, price, weight, filename in self.prices:
            if text.lower() in product_name.lower():
                result.append((product_name, price, weight, filename))
        self.last_search_results = result
        return result

    def format_data(self, data):
        headers = ["№", "Наименование", "цена", "вес", "файл", "цена за кг."]
        table = []
        sorted_data = sorted(data, key=lambda x: x[1] / x[2])
        for i, (product_name, price, weight, filename) in enumerate(sorted_data, 1):
            price_per_kg = round(price / weight, 2)
            table.append([i, product_name, price, weight, filename, price_per_kg])
        return table, headers

    def search_and_display(self):
        while True:
            search_text = input("Введите текст для поиска (для выхода введите 'exit'): ")
            if search_text.lower() == 'exit':
                print("Работа завершена.")
                break
            search_results = self.find_text(search_text)
            table, headers = self.format_data(search_results)
            print(tabulate(table, headers=headers, tablefmt='simple_grid'))

    def export_to_html(self, output_file):
        if self.last_search_results:
            with open(output_file, 'w', encoding='utf-8') as file:
                table, headers = self.format_data(self.last_search_results)
                file.write(tabulate(table, headers=headers, tablefmt="html"))
        else:
            print("Нет результатов поиска для экспорта.")


if __name__ == "__main__":
    current_directory = os.getcwd()
    manager = PriceManager(current_directory)
    manager.search_and_display()
    manager.export_to_html("output.html")
