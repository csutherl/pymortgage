#!/usr/bin/python


class Amortization_Schedule:

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

    def create_schedule(self, rate, P, n, num_of_months=None):
        schedule = []
        new_prin = P
        start_n = n
    
        while n > 0:
            curr_month = self.calc_amortization(rate, new_prin, n)
            current_month = (start_n - n)
            curr_month['month'] = current_month + 1  # to make it one based
            curr_month['balance'] = round(new_prin - curr_month['principal'], 2)
            new_prin = curr_month['balance']

            if current_month == num_of_months:
                break
            n -= 1
        
            schedule.append(curr_month)
        return schedule

if __name__ == "__main__":
    am_sched = Amortization_Schedule()
    from d3_schedule import D3_Schedule
    d3_sched = D3_Schedule()

    #schedule = create_schedule(.045, 250000, 360)#, 10) 
    #schedule = create_schedule(.05, 250000, 360, 5) 
    schedule = am_sched.create_schedule(.0575, 245000, 240, 5) 
    
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(schedule)

    pp.pprint(d3_sched.comprehend_schedule_for_d3(schedule))


