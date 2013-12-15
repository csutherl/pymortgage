class Amortization_Schedule:

    def __init__(self, rate, P, n):
        self.rate = rate
        self.P = P
        self.n = n
        self.schedule = None

        self.create_schedule()

    def calc_amortization(self, rate, P, n):
        from math import pow
        # calc monthly interest rate
        # doing this funky conversion stuff to drop off the remaining digits instead of round up.
        i = float(str(rate / 12)[:10])
        # calc amortization for a single month
        amort = round(((i * P * pow((1 + i), n)) / (pow((1 + i), n) - 1)), 2)
        # calc monthly interest
        mi = round((P * i), 2)
        # calc monthly principal portion
        mp = round((amort - mi), 2)
      
        return {"amount": amort, "interest": mi, "principal": mp, "monthly_rate": i}

    def create_schedule(self):
        temp_schedule = []
        new_prin = self.P
        year = False

        count_n = self.n
        start_n = count_n

        while count_n > 0:
            curr_month = self.calc_amortization(self.rate, new_prin, count_n)
            current_month = (start_n - count_n)
            curr_month['month'] = current_month + 1  # to make it one based
            curr_month['balance'] = round(new_prin - curr_month['principal'], 2)
            new_prin = curr_month['balance']

            count_n -= 1

            temp_schedule.append(curr_month)
            self.schedule = temp_schedule

    def get_yearly_schedule(self):
        temp_schedule = []
        year_end_balance = dict()

        for month in self.schedule:
            year = (month['month'] / 12) + 1

            if month['month'] % 12 == 0:
                year = month['month'] / 12
                year_end_balance[year] = month['balance']

            month['year'] = year
            temp_schedule.append(month)

        # grouping
        yearly_schedule = []
        from itertools import groupby
        for key, group in groupby(temp_schedule, lambda x: x['year']):
            group_schedule = dict()
            group_schedule['year'] = key
            group_schedule['interest'] = 0
            group_schedule['principal'] = 0
            group_schedule['amount'] = 0
            group_schedule['balance'] = year_end_balance[key]

            for year in group:
                group_schedule['interest'] += year['interest']
                group_schedule['principal'] += year['principal']
                group_schedule['amount'] += year['amount']

            yearly_schedule.append(group_schedule)

        return yearly_schedule

    def get_first_x(self, num_of_items):
        subset = []

        for x in range(num_of_items):
            subset.insert(x, self.schedule[x])

        return subset

if __name__ == "__main__":
    am_sched = Amortization_Schedule(.0575, 245000, 240)

    from d3_schedule import D3_Schedule
    d3_sched = D3_Schedule(am_sched.schedule)

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(am_sched.schedule)

    pp.pprint(d3_sched.get_d3_schedule())
    # pp.pprint(am_sched.get_first_x(5))

    # pp.pprint(am_sched.get_yearly_schedule())
