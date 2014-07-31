class C3Schedule:

    def __init__(self, am_schedule):
        self.monthly_c3_schedule = self.get_c3_schedule(am_schedule.monthly_schedule)
        self.yearly_c3_schedule = self.get_c3_schedule(am_schedule.yearly_schedule, True)

    def get_c3_schedule(self, schedule, by_year=None):
            c3_data = dict()

            keys = ['balance', 'principal', 'interest', 'amount', 'insurance', 'taxes', 'extra payment']

            if by_year:
                term = 'year'
            else:
                term = 'month'

            for i in range(len(keys)):
                key = keys[i]
                c3_data[key.capitalize()] = []

                for item in schedule:
                    c3_data[key.capitalize()].append(item[key])

            return c3_data
