from pymortgage.server.amortization_calculator import calc_amortization


class AmortizationSchedule:

    # assuming adj_frequency is always expressed in years, and adj_cap and lifetime_cap are expressed as decimals
    def __init__(self, rate, P, n, annual_tax=0, annual_ins=0, adj_frequency=None, adj_cap=None, lifetime_cap=None,
                 extra_pmt=None, yearly=False):
        self.rate = rate
        self.P = P

        if yearly:
            self.n = n * 12
        else:
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

        self.monthly_schedule = dict()
        self.yearly_schedule = dict()

        # create schedules in instance
        self.create_monthly_schedule()
        self.create_yearly_schedule()

    def create_monthly_schedule(self):
        temp_schedule = []

        new_prin = self.P

        count_n = self.n
        start_n = count_n

        # set payment to 0 so that we can capture the first payment or adjustments with ARMs
        constant_amt = 0
        # add a boolean to allow adjustments after the rate adjustment
        last_adj = False
        while count_n > 0:
            current_month = (start_n - count_n)

            curr_month = calc_amortization(self.rate, new_prin, count_n)
            curr_month['month'] = current_month + 1  # to make it one based
            curr_month['balance'] = round(new_prin - curr_month['principal'] - self.extra_pmt, 2)

            if self.adj_frequency is not None and current_month > 0:
                if current_month % (self.adj_frequency * 12) == 0 and (self.rate + self.adj_cap) <= self.lifetime_cap:
                    self.rate += self.adj_cap  # assumes worst case scenario
                elif current_month % (self.adj_frequency * 12) == 1 and not last_adj:
                    # mod 1 because we need to update the constant_amt after the rate change
                    constant_amt = curr_month['amount']
                    if (self.rate + self.adj_cap) > self.lifetime_cap:
                        last_adj = True

            # set payment amount to first amount
            if constant_amt == 0:
                constant_amt = curr_month['amount']
            elif constant_amt != curr_month['amount']:
                # set delta amount from payments
                delta = constant_amt - curr_month['amount']
                curr_month['amount'] = constant_amt
                # if delta is positive then update the balance and principal amount
                if delta > 0:
                    curr_month['balance'] -= delta
                    curr_month['principal'] += delta

            # balance cant be < 0...it makes other things less...
            if curr_month['balance'] < 0:
                curr_month['balance'] = 0

            new_prin = curr_month['balance']
            curr_month['extra payment'] = self.extra_pmt
            curr_month['taxes'] = self.monthly_tax
            curr_month['insurance'] = self.monthly_insurance

            # add taxes and insurance to the amount and extra payment
            curr_month['amount'] += self.monthly_tax + self.monthly_insurance + self.extra_pmt

            count_n -= 1

            temp_schedule.append(curr_month)

        self.monthly_schedule['table'] = temp_schedule
        self.monthly_schedule['summary'] = self.calc_stats(self.monthly_schedule)

    def create_yearly_schedule(self):
        # multiply the original term by 12 so that we can create years
        temp_n = self.n / 12
        self.n = temp_n

        if len(self.monthly_schedule) == 0:
            self.create_monthly_schedule()

        temp_schedule = []
        year_end_balance = dict()

        counter = 1
        year = 1
        for month in self.monthly_schedule['table']:
            # overwrite each year end balance with the last month's
            year_end_balance[year] = month['balance']

            month['year'] = year
            temp_schedule.append(month)

            # python rounding wasn't working out, so I employed my own strategy to get the year count right
            counter += 1
            if counter % 12 == 1:
                year += 1

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

        self.yearly_schedule['table'] = yearly_schedule
        self.yearly_schedule['summary'] = self.calc_stats(self.yearly_schedule)

    def calc_stats(self, schedule):
        summary = dict()

        summary['90% ltv'] = self.P * .90
        summary['80% ltv'] = self.P * .80

        summary['total amount'] = 0
        summary['total extra payment'] = 0
        summary['total principal'] = 0
        summary['total interest'] = 0

        for row in schedule['table']:
            summary['total amount'] += row['amount']
            summary['total extra payment'] += row['extra payment']
            summary['total principal'] += row['principal']
            summary['total interest'] += row['interest']

        return summary
