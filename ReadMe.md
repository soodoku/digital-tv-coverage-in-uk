### UK Digital TV Coverage Data and Scripts

[UK Digital TV Coverage](http://www.digitaluk.co.uk/coveragechecker/) data, and scripts for getting that data. 

#### Getting the Data

1. Download the Data: 
	
	* Start with a file containing [all the postcodes](http://dx.doi.org/10.7910/DVN/NRY5OP) (Harvard DVN Link). The data are from UK's [Office of National Statistics](http://www.ons.gov.uk/ons/guide-method/geography/products/postcode-directories/-nspp-/index.html).

    * Write a script that pings the [coverage checker website](http://www.digitaluk.co.uk/coveragechecker/) for each 7 character postcode (column name: `pcd`). Download the html if there is data (Sample data pages: [AB101AA](data/sample_src_data/AB101AA.html), [AB101AB](data/sample_src_data/AB101AB.html)). Write postcode to `error` file if there is no data. ([Sample error page](data/sample_src_data/Error.html).)

    ```{r sample_scraper_code}
    # sample code

    library(httr)
    library(rvest)

    for (i in 1:nrow(postcodes_ons)) {

    request <- httr::GET(paste0("http://www.digitaluk.co.uk/coveragechecker/main/display/detailed/",paste(strsplit(postcodes_ons$pcd[i], " ")[[1]], collapse="+"),"/NA/0"))

    webpage <- html(request)
    if(length(webpage %>% html_nodes("#error-frame"))!=0)
    ...

    }

    ```
    
    * Given there are 2.5 million postcodes, run multiple instances. For instance, if a page takes 1 second to return, we need approximately 700 hours or nearly 29 days to download the data using a single instance. ([See here](https://gist.github.com/soodoku/3e3eb8d842a73400d9a8) for basic installs for initializing a R based scraper on Ubuntu.)

    ```{r sample_run_code}

    nohup RScript downloader.R & 

    ```

2. Concatenate all the `error` files and put all the html files in a single folder.
    ```
    cat *error > errors
    
    ```

3. Parse the Data: 
    * Run [converter.py](converter.py) with the folder containing html files as the source folder ([sample html files folder](data/sample_src_data/). The python script will produce `output.csv` (you can change the name of the ouput file.)

#### Data

1. [errors](data/errors): All the postcodes for which no data are returned.
2. [output.csv](http://dx.doi.org/10.7910/DVN/NRY5OP)  (Harvard DVN Link): Data on the postcodes for which data are returned:
    * Postal code of the address: postal.code
    * Quality of TV Signal: quality.terrestrial.tv.signal
    * Transmitter name: transmitter.name
    * Transmitter region: transmitter.region
    * Digital services available through aerial: service.* (e.g. service.bt_vision, service.freeview) Data take values 0 and 1, indicating whether or not a service is available.
    * Channels available: channel.* (entertainment, hd, childrens, news, adult, text stream, radio.. etc.).
    
#### License
Scripts are released under the [MIT License](License.md).