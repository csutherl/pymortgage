class D3Schedule:

    def __init__(self, am_schedule):
        self.monthly_d3_schedule = self.get_d3_schedule(am_schedule.monthly_schedule)
        self.yearly_d3_schedule = self.get_d3_schedule(am_schedule.yearly_schedule, True)

    def get_d3_schedule(self, schedule, by_year=None):
            d3_data = []

            keys = ['balance', 'principal', 'interest', 'amount', 'insurance', 'taxes', 'extra payment']

            if by_year:
                term = 'year'
            else:
                term = 'month'

            for i in range(len(keys)):
                d3_data.insert(i, self.add_key(schedule, keys[i], term))

            return d3_data

    # color would be added to the new set for each key
    def add_key(self, schedule, key, term):
        new_set = dict()
        new_set['key'] = key.capitalize()
        new_set['values'] = []

        for item in schedule:
            new_set['values'].append([item[term], item[key]])

        return new_set