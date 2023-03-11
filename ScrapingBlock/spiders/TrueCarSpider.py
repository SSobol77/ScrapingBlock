import scrapy


class TrueCarSpider(scrapy.Spider):
    name = "truecar"
    allowed_domains = ["https://www.truecar.com/"]
    start_urls = ["https://www.truecar.com/used-cars-for-sale/listings/tesla/model-3/"]

    # W tej funkcji realizujmy ściągnięcie zawartości strony:
    def start_requests(self):
        urls = ["https://www.truecar.com/used-cars-for-sale/listings/tesla/model-3/"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # W tej funkcji będziemy przetwarzać stronę i przygotowywać wynik:
    def parse(self, response):
        # Xpath=//tagname[@attribute='value']
        # data-test="vehicleCardYearMakeModel"
        # Z tega div wyciągamy: <div class="card-content order-3 vehicle-card-body" data-test="cardContent">:
        all_listings = response.xpath('//div[@data-test="allVehicleListings"]')

        # Będziemy oznaczać informację dla każdego z samochodów, które chcemy przetworzyć:
        for tesla in all_listings:
            make_model = tesla.css('div[data-test="vehicleCardYearMakeModel"] > div') # znajdujemy nazwę modelu (make_model)
            year = make_model.css('span.vehicle-card-year text-xs::text').get()  # rok produkcji (year)

            # W ramach obiektu make_model znajdujemy konkretny model, wykonując działania na zmiennych tekstowych:
            model_raw = make_model.css('span.truncate::text').get()
            model_raw = str(model_raw)
            model = model_raw[model_raw.find('>') + 1:-7].replace('<!-- -->', '')

            # Budujemy słownik, w którym zapisujemy dane dla pierwszego znalezionego modelu oraz zapętlamy proces:
            tesla_data = {
                'url': 'https://truecar.com' + tesla.css('a::attr(href)').get(),
                'model': str(year) + ' ' + str(model),
                'mileage': tesla.css('div[data-test="cardContent"] > div > div.truncate::text').get(),
                'price': tesla.css('div.vehicleCardPricingBlockPrice::text').get(),
            }
            yield tesla_data

            # Etap „idź szukaj danych”:
            # Robimy to wykonując prostą komendę w zakładce „terminal” w której podajemy nazwę naszego Spidera, w tym
            # wypadku truecar, która od razu zapisuje nam wszystkie dane w pliku.CSV, który podajemy na końcu
            # scrapy crawl truecar -o truecar.csv
