from pymortgage.server.amortization_calculator import calc_amortization


class AmortizationSchedule:

    # assuming adj_frequency is always expressed in years, and adj_cap and lifetime_cap are expressed as decimals
    def __init__(self, rate, P, n, annual_tax, annual_ins, adj_frequency=None, adj_cap=None, lifetime_cap=None,
                 extra_pmt=None):
        self.rate = rate
        self.P = P
        self.n = n

        # static taxes and insurance
        self.annual_tax = annual_tax
        self.annual_ins = annual_ins
        self.monthly_tax = round(self.annual_tax/12, 2)
        self.monthly_insurance = round(self.annual_ins/12, 2)

        # init ARM vars
        self.adj_frequency = adj_frequency
        self.adj_cap = adj_cap
        self.lifetime_cap = lifetime_cap

        # correct lifetime_cap by adding it to initial rate
        # added .000001 b/c the 5 year ARM wasn't adjusting the last time.
        if self.lifetime_cap is not None:
            self.lifetime_cap += self.rate + .000001

        # adding new var for recording and calculating amort after making extra payments
        if extra_pmt is None:
            self.extra_pmt = 0
        else:
            self.extra_pmt = extra_pmt

        # create schedules in instance
        self.monthly_schedule = self.create_monthly_schedule()
        self.yearly_schedule = self.create_yearly_schedule()

    def create_monthly_schedule(self):
        temp_schedule = []

        new_prin = self.P

        count_n = self.n
        start_n = count_n

        while count_n > 0:
            current_month = (start_n - count_n)

            if self.adj_frequency is not None \
                and current_month > 0 \
                and current_month % (self.adj_frequency * 12) == 0 \
                and (self.rate + self.adj_cap) <= self.lifetime_cap:
                self.rate += self.adj_cap  # assumes worst case scenario

            curr_month = calc_amortization(self.rate, new_prin, count_n)
            curr_month['month'] = current_month + 1  # to make it one based
            curr_month['balance'] = round(new_prin - curr_month['principal'] - self.extra_pmt, 2)

            # balance cant be < 0...it makes other things less...
            if curr_month['balance'] < 0:
                curr_month['balance'] = 0

            new_prin = curr_month['balance']
            curr_month['taxes'] = self.monthly_tax
            curr_month['insurance'] = self.monthly_insurance
            curr_month['extra payment'] = self.extra_pmt

            # add taxes and insurance to the amount and extra payment
            curr_month['amount'] += self.monthly_tax + self.monthly_insurance + self.extra_pmt
            # add extra payment amount to principal for the month
            curr_month['principal'] += self.extra_pmt

            count_n -= 1

            temp_schedule.append(curr_month)

        return temp_schedule

    def create_yearly_schedule(self):
        # multiply the original term by 12 so that we can create years
        temp_n = self.n * 12
        self.n = temp_n
        monthly_schedule = self.create_monthly_schedule()

        temp_schedule = []
        year_end_balance = dict()

        for month in monthly_schedule:
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
            group_schedule['extra payment'] = 0

            # insert taxes and insurance
            group_schedule['insurance'] = self.annual_ins
            group_schedule['taxes'] = self.annual_tax

            for year in group:
                group_schedule['interest'] += year['interest']
                group_schedule['principal'] += year['principal']
                group_schedule['amount'] += year['amount']
                group_schedule['extra payment'] += year['extra payment']

            yearly_schedule.append(group_schedule)

        return yearly_schedule
