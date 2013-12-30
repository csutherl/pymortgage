import json


class D3_Schedule:

    def __init__(self, schedule):
        self.schedule = schedule

    def get_d3_schedule(self, by_year=None):
            d3_data = []

            keys = ['balance', 'principal', 'interest', 'amount', 'insurance', 'taxes']

            if by_year:
                term = 'year'
            else:
                term = 'month'

            for i in range(len(keys)):
                d3_data.insert(i, self.add_key(keys[i], term))

            return json.dumps(d3_data)

    # color would be added to the new set for each key
    def add_key(self, key, term):
        new_set = dict()
        new_set['key'] = key.capitalize()
        new_set['values'] = []

        for item in self.schedule:
            new_set['values'].append([item[term], item[key]])

        return new_set