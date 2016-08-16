## How to use

Go into the project directory.
Run the following command:

```sh
scrapy crawl weightxreps
  -a user=[username]
  -a start=[start date]
  -a end=[end date]
  -o [where to save the output]
  -t [format of the result]
```

Date format is YYYY-MM-DD

By defaults:
```
start=[date when user joined (user registration date)]
end='today' by default
```


Example:
```sh
# Data by date 2015-09-30
scrapy crawl weightxreps -a user='danharp' -a start='2015-09-30' -a end='2015-09-30' -o /tmp/data.csv -t csv

# Today's data
scrapy crawl weightxreps -a user='danharp' -a start='today' -o /tmp/data.csv -t csv

# Download all users data
scrapy crawl weightxreps -a user='danharp' -o /tmp/data.csv -t csv
```

## Requirements

Python 2.7 and Scrapy
