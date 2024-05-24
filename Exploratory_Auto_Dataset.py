import csv
import statistics
import matplotlib.pyplot as plt

def mlist(name, filename):
    d_list = []
    with open(filename, "r") as infile:
        csvreader = csv.reader(infile)
        title = next(csvreader)
        colNum = 0
        while colNum < len(title) and title[colNum] != name:
            colNum += 1
        if colNum == len(title):
            print("Error")
        else:
            for line in csvreader:
                d_list.append(line[colNum])
        return d_list

def all_list(filename):
    d_list = []
    with open(filename, "r") as infile:
        csvreader = csv.reader(infile)
        title = next(csvreader)      
        for row in csvreader:
            d_list.append(row)
        titles.append(title)
        return d_list
    
def f_list(list):
    f_list = []
    for row in list:
        f_row = []
        for i in row:
            if i == '':
                null_col_index.append(row.index(i))
                null_row_index.append(list.index(row))
            else:
                f_row.append(float(i))
        f_list.append(f_row)
    print(null_row_index)
    print(null_col_index)
    return f_list

def mean(list):
    out_list = []
    for i in list:
        if i != '':
            out_list.append(float(i))
    mean = round(statistics.mean(out_list), 2)
    return mean

def all_mean(titles, filename):
    mean_list = []
    for row in titles:
        for i in row:
            l = mlist(i, filename)
            means = mean(l)
            mean_list.append(means)
        break
    print(mean_list)
    return mean_list

def replace_null(mean_list, c_index, r_index, f_list):
    for i in r_index:
        f_list[i].insert(c_index[r_index.index(i)], mean_list[c_index[r_index.index(i)]])
    return f_list

def replace_outlier(f_list, mean_list):
    r_list = []
    for row in f_list:
        rows_list = []
        for i in row:
            imean = mean_list[row.index(i)]
            upper = imean*1.25
            lower = imean*0.75
            if i > upper or i < lower:
                rows_list.append(imean)
            else:
                rows_list.append(i)
        r_list.append(rows_list)
    return r_list

def stats(r_list):
    mins = []
    maxs = []
    means = []
    median = []
    stdev = []
    for col in range(len(r_list[0])):
        col_values = []
        for row in range(len(r_list)):
            col_values.append(r_list[row][col])
        means.append(round(statistics.mean(col_values), 2))
        mins.append(round(min(col_values), 2))
        maxs.append(round(max(col_values), 2))
        median.append(round(statistics.median(col_values), 2))
        stdev.append(round(statistics.stdev(col_values), 2))
    stat_list.append(maxs)
    stat_list.append(mins)
    stat_list.append(means)
    stat_list.append(median)
    stat_list.append(stdev)
    stat_list.insert(0, titles[0])
#     column = ["Stats", "Maximum", "Minimum", "Median", "Mean", "Standard Deviation"]
#     for i in range(len(column)):
#         stat_list[i].insert(0, column[i])
    print(stat_list)
#     for row in range(0, len(stat_list)): 
#         for column in range(0, len(stat_list[row])): 
#             print(stat_list[row][column], "   \t", end = " ")
#         print()
#     print()
    
def correlation_plots(r_list):
    n_cols = len(r_list[0])
    for i in range(n_cols):
        for j in range(i, n_cols):
            x = [row[i] for row in r_list]
            y = [row[j] for row in r_list]
            plt.scatter(x, y)
            plt.xlabel(str(i))
            plt.ylabel(str(j))
#             plt.show()

def correlation_plot(xlist,ylist):
    plt.scatter(xlist,ylist)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Pairwise Correlation')
    plt.show()

def pearson_correlation(r_list, name1, name2, titles):
    sum_x = 0
    sum_y = 0
    sum_sq_x = 0
    sum_sq_y = 0
    psum = 0
    n = len(r_list)
    x = titles[0].index(name1)
    y = titles[0].index(name2)
    for row in r_list:
        sum_x += row[x]
        sum_y += row[y]
        sum_sq_x += row[x] ** 2
        sum_sq_y += row[y] ** 2
        psum += row[x] * row[y]
    num = psum - (sum_x * sum_y / n)
    den = ((sum_sq_x - (sum_x ** 2) / n) * (sum_sq_y - (sum_y ** 2) / n)) ** 0.5
    corr = num / den
    print(corr)
    xlist = []
    ylist = []
    for row in r_list:
        xlist.append(row[x])
    for row in r_list:
        ylist.append(row[y])
    correlation_plot(xlist,ylist)

def fuel_efficiency(mean_list, r_list):
    for row in r_list:
        if row[0] >= mean_list[0]:
            row.append("High Efficiency")
        elif row[0] <= mean_list[0]:
            row.append("Low Efficiency")
    return r_list    


filename = "autompg.csv"
null_col_index = []
null_row_index = []
titles = []
f_list = f_list(all_list(filename))
mean_list = all_mean(titles, filename)
f_list = replace_null(mean_list, null_col_index, null_row_index, f_list)
r_list = replace_outlier(f_list, mean_list)
stat_list = []
stats(r_list)
correlation_plots(r_list)
pearson_correlation(r_list, "MPG", "Cylinders", titles)
pearson_correlation(r_list, "Displacement", "Horsepower", titles)
pearson_correlation(r_list, "Weight", "Cylinders", titles)
pearson_correlation(r_list, "Acceleration", "Horsepower", titles)
pearson_correlation(r_list, "Acceleration", "Cylinders", titles)
fuel_efficiency(mean_list, r_list)