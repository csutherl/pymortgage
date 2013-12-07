class D3_Schedule:

    def comprehend_schedule_for_d3(self, schedule):
            d3_data = []
            bal_data = {}

            bal_data['key'] = "Balance"
            bal_data['values'] = []

            for month in schedule:
                bal_data['values'].append([month['month'], month['balance']])

            d3_data.insert(0, bal_data)
            prin_data = {}

            prin_data['key'] = "Principal"
            prin_data['values'] = []

            for month in schedule:
                prin_data['values'].append([month['month'], month['principal']])

            d3_data.insert(1, prin_data)
    
            int_data = {}
    
            int_data['key'] = "Interest"
            int_data['values'] = []
    
            for month in schedule:
                int_data['values'].append([month['month'], month['interest']])
    
            d3_data.insert(2, int_data)
    
            return d3_data
