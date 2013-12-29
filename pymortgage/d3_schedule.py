import json


class D3_Schedule:

    def __init__(self, schedule):
        self.schedule = schedule

    def get_d3_schedule(self, by_year=None):
            d3_data = []

            if by_year:
                d3_data.insert(0, self.add_year_key("balance"))
                d3_data.insert(1, self.add_year_key("principal"))
                d3_data.insert(2, self.add_year_key("interest"))
                d3_data.insert(3, self.add_year_key("amount"))
            else:
                d3_data.insert(0, self.add_month_key("balance"))
                d3_data.insert(1, self.add_month_key("principal"))
                d3_data.insert(2, self.add_month_key("interest"))
                d3_data.insert(3, self.add_month_key("amount"))

            return json.dumps(d3_data)

    def add_month_key(self, key):
        return self.add_key(key, 'month')

    def add_year_key(self, key):
        return self.add_key(key, 'year')

    # color would be added to the new set for each key
    def add_key(self, key, term):
        new_set = dict()
        new_set['key'] = key.capitalize()
        new_set['values'] = []

        for item in self.schedule:
            new_set['values'].append([item[term], item[key]])

        return new_set