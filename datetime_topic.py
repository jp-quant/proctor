import datetime
import os
import numpy as np
import pandas as pd


#---| correct function
def _last_day_of_month(any_date:str)->str:
    m,d,y = any_date.split("/")
    date = datetime.date(year=int(y),month=int(m),day=int(d))
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month_date = date.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    result = next_month_date - datetime.timedelta(days=next_month_date.day)
    return result.strftime("%m/%d/%Y")

def get_test_data(start_year = 2000, end_year = 2050, **kwargs)->dict:
    test_data = {}
    for year in range(start_year, end_year+1):
        months = [np.random.choice(range(1,13)) for _ in range(4)] # pick 4 random months
        if 2 not in months: months.append(2) # add february as well
        for month in months:
            input_date= datetime.date(
                            year = year,
                            month = month,
                            day = np.random.choice(range(1,24)) # random pick for day
                            ).strftime("%m/%d/%Y")
            output_date = _last_day_of_month(input_date)
            test_data[input_date] = output_date
    return test_data

def validate_test_function(func, **kwargs):
    test_data = get_test_data(**kwargs)
    result = []
    for input_date, correct_output in test_data.items():
        try:
            output_date = func(input_date)
        except Exception as e:
            output_date = "Error: %s"%str(e)
        
        result.append(
            {
                'input_date': input_date,
                'output_date': output_date if isinstance(output_date, str) else "Failed. Output needs to be a string.",
                'correct_output_date': correct_output
            }
        )
    result = pd.DataFrame.from_dict(result)

    correct_result = result[result['output_date'] == result['correct_output_date']]
    score = len(correct_result)/len(result)
    print("Score: %s"%(round(score*100, 3)) + "%")
    print("Passed: %s/%s"%(len(correct_result), len(result)))

    incorrect_result = result[result['output_date'] != result['correct_output_date']]
    if not incorrect_result.empty:
        print("Failed Scenarios:")
        print(incorrect_result)
