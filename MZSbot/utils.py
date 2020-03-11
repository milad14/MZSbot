from datetime import timedelta, date



def daterange(start_date, end_date):
    for n in range(int (( end_date - start_date ).days)):
        yield start_date + timedelta(n)



def url_array_generator(url, start_date, end_date):
    url_array = []
    for single_date in daterange(start_date, end_date):
        date = single_date.strftime("%Y/%m/%d")
        result = url + date
        url_array.append(result)
    return url_array