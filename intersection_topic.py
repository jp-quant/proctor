import os
import pandas as pd
from matplotlib import pyplot as plt

dataset = pd.read_csv(
            os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'intersection_data.csv'
                    ), 
                    index_col = 0, 
                    header = 0
                    )
result = {}
for i in range(1, 100):
    cols = [("f"+str(i)), ("g"+str(i))]
    try:
        df = dataset[cols]
        df.columns = ["f_x", "g_x"]
        result[i] = df
    except:
        break

def get_sample_data():
    return result[1]


#-----| crossing index
def _first_crossed_index(
                    data:pd.DataFrame,
                    f_x:str = "f_x",
                    g_x:str = "g_x",
                    ):
    result = None
    prev_i = None
    for i in data.index:
        if i == data.index[0]:
            prev_i = i
        else:
            d = data.loc[i]
            prev_d = data.loc[prev_i]

            f = d[f_x]
            g = d[g_x]
            prev_f = prev_d[f_x]
            prev_g = prev_d[g_x]

            if (
                ((prev_f > prev_g) and (f < g))
                or
                ((prev_f < prev_g) and (f > g))
                or
                ((prev_f == prev_g) and (f != g))
            ):
                result = i
                break
    return result

def validate_test_function_1(func): # first_crossed_index() problem
    validation_result = []
    for i, df in result.items():
        test_output = func(df)
        correct_output = _first_crossed_index(df)
        validation_result.append(
            {
                'dataset_id': i,
                'test_output':str(test_output),
                'correct_output':str(correct_output)
            }
        )
    validation_result = pd.DataFrame.from_dict(validation_result)

    correct_result = validation_result[validation_result['test_output'] == validation_result['correct_output']]
    score = len(correct_result)/len(validation_result)
    print("Score: %s"%(round(score*100, 3)) + "%")
    print("Passed: %s/%s"%(len(correct_result), len(validation_result)))

    incorrect_result = validation_result[validation_result['test_output'] != validation_result['correct_output']]
    if not incorrect_result.empty:
        print("Failed Scenarios:")
        print(incorrect_result)
#---------------|








#----| Continuous (more advanced)
def _calculate_intersection_point(
                        data:pd.DataFrame,
                        f_x:str = "f_x",
                        g_x:str = "g_x",
                        )->tuple:
    
    assert data.shape[1] >= 2, "DataFrame given needs to have at least 2 columns"
    assert f_x in data.columns
    assert g_x in data.columns
    
    x_intersect = None
    y_intersect = None
    prev_i = None
    prev_d = None
    for i in data.index:
        d = data.loc[i]
        if d[f_x] > d[g_x]:
            if i == data.index[0]:
                x_intersect = i
                y_intersect = d[g_x]
            else:
                # Step 1) Calculate for slopes
                df_dx = (d[f_x] - prev_d[f_x])/(i - prev_i)
                dg_dx = (d[g_x] - prev_d[g_x])/(i - prev_i)

                # Step 2) Calculate for y-intercepts
                f0 = d[f_x] - (df_dx * (i))
                g0 = d[g_x] - (dg_dx * (i))

                # Step 3) Calculate for x-intersect
                x_intersect = (f0 - g0)/(dg_dx - df_dx)

                # Step 4) Calculate for y-intersect
                y_intersect = df_dx*(x_intersect) + f0
            break
        prev_i = i
        prev_d = d.copy()
    
    return (x_intersect,y_intersect)
def plot_result_2(
                data:pd.DataFrame,
                x_intersect,
                y_intersect,
                prefix = None,
                f_x:str = "f_x",
                g_x:str = "g_x",
                ):
    x = data.index.values
    f = data[f_x].values
    g = data[g_x].values

    plt.plot(x, f, "-")
    plt.plot(x, g, "-")

    #x_intersect, y_intersect = calculate_intersection_point(data)
    if x_intersect is not None and y_intersect is not None:
        plt.scatter(x_intersect, y_intersect, s = 150, facecolors = 'none', edgecolors = "r")
        title = "Intersection Point: (%s, %s)"%(round(x_intersect, 3), round(y_intersect, 3))
    else:
        title = "No Intersection Point."
    if prefix is not None:
        title = "[%s] "%str(prefix) + title
    
    plt.title(title)
    plt.show()

def validate_test_function_2(func, precision = 2):
    validation_result = []
    for i, df in result.items():
        x_intersect = None
        y_intersect = None
        try:
            x_intersect, y_intersect = func(df)
            func_output = str((round(x_intersect, precision), round(y_intersect, precision)))
        except Exception as e:
            func_output = "Error: %s"%str(e)
        plot_result_2(df, x_intersect=x_intersect, y_intersect=y_intersect, prefix = "Test Output #%s"%str(i))
        
        correct_x_intersect, correct_y_intersect = _calculate_intersection_point(df)
        correct_ouput = str((round(correct_x_intersect, precision), round(correct_y_intersect, precision)))
        plot_result_2(df, x_intersect=correct_x_intersect, y_intersect=correct_y_intersect, prefix = "Correct Output #%s"%str(i))
        
        validation_result.append(
            {
                'dataset_id': i,
                'test_output':str(func_output),
                'correct_output':str(correct_ouput)
            }
        )
    validation_result = pd.DataFrame.from_dict(validation_result)
    correct_result = validation_result[validation_result['test_output'] == validation_result['correct_output']]
    score = len(correct_result)/len(validation_result)
    print("Score: %s"%(round(score*100, 3)) + "%")
    print("Passed: %s/%s"%(len(correct_result), len(validation_result)))

    incorrect_result = validation_result[validation_result['test_output'] != validation_result['correct_output']]
    if not incorrect_result.empty:
        print("Failed Scenarios:")
        print(incorrect_result)
#--------------|