## Codal API
#### Overview

Codal API is a Crawler that looks at reports of two stock ```خودرو``` and ‍‍‍‍```خساپا``` and returns stock DPS with the date.


### Built With


* [Scrapy](https://github.com/scrapy/scrapy)
* [Scrapy-Splash](https://hub.docker.com/r/vivekananda/scrapy-splash)
* [Flask](https://github.com/pallets/flask)
* [Docker](https://www.docker.com/)


## Getting Started

To run the application you need to install [Docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) in your system.

### Installation

1. Get a API at [185.239.104.76](http://185.239.104.76/)
2. Clone the repo
   ```sh
   git clone https://github.com/alireza-f/scrapy-api.git
   ```
3. Build Containers
   ```sh
   docker-compose up
   ```

## Usage

There is two way to use of this API service:

* Use in browser: Just enter the stock name and press Enter key to load
* Use in Postman: Send POST request to [185.239.104.76](http://185.239.104.76/) with form-data body: ```key``` should be ```symbol``` and ```value``` is the stock name


If you want to send json raw body data you should change ```index``` function in ```app.py``` to this:
```
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        data = request.json
        symbol = data.get('symbol')

        sql_query = f"SELECT * FROM dps_table WHERE name='{symbol}'"
        conn = db_connection()
        cursor = conn.execute(sql_query)
        dps_list = [dict(name=row[0], dps=row[1], date=row[2])
                    for row in cursor.fetchall()]

        if dps_list:
            return jsonify(dps_list)
        else:
            error_message = {
                'error message': 'نام نماد را درست وارد کنید',
            }
            return jsonify(error_message)
    else:
        return render_template("index.html")
```
