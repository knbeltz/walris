'''
Pseudocode: 


endpoint = FMP base URL + "/stable/batch-index-quotes" 

query_parameters = {
    "apikey": FMP API key from settings 
}



def fetch_market_snapshot(symbols: list[str]) -> list[IndexQuote]: 
    RETURNS list of Index Quote 

    IF symbols is empty 
        RETURN empty list 
    
    normalize_symbols = empty set 

    FOR each symbol in symbols 
        trim white space from symbol
        convert symbol to uppercase 
        add symbol to normalized_symbols 

    TRY 
        send GET request to endpoint 
            using query_parameters 
            with a timeout 
        
        raise an error if HTTP response is unsuccessful 

        raw_quotes = parse response body as JSON 

    CATCH network error, timeoutm or unsucessful HTTP response 
        raise MarketSnapshotFetchError 
    
    index_quotes = empty list 

    FOR each raw_quote in raw_quotes 
        raw_symbol = raw_quote["symbol"]

        IF raw_symbol is not in normalized_symbols 
            CONTINUE 

        TRY
            quote = IndexQuote(
                symbol = raw_symbol,
                name = raw_quote["name"],
                price = raw_quote["price"],
                change = raw_quote["change"],
                change_percentage = raw_qyote["changesPercentage"],
                day_low = raw_quote["dayLow"],
                day_high = raw_quote["dayHigh"],
                previous_close = raw_quote["previousClose"],
                timestamp = raw_quote["timestamp"]
            )
            add quote to index_quotes 
        
        CATCH missing or invalid quote data 
            log that this quote could not be normalized 
            CONTINUE 
        
        RETURN index_quotes

def fetch_sector_performance(as_of: date) -> list[SectorPerformance]
    RETURNS list of Sector Performance 

    as_of — the date to query (today's date, same local-vs-fixed-timezone question from before applies here too).
    Calls /stable/sector-performance-snapshot, normalizes into a list of SectorPerformance (one per sector).

    TRY 
        send GET request to endpoint 
            using query_parameters 
            with a timeout 
        
        raise an error if HTTP response is unsuccessful 

        raw_quotes = parse response body as JSON 

    CATCH network error, timeoutm or unsucessful HTTP response 
        raise MarketSnapshotFetchError 


    sector_performance = empty list 

    TRY
        sector = SectorPerformance(
            basic_materials = raw basic_materials,
            communication_services = raw communication_services,
            consumer_cyclical = raw consumer_cyclical, 
            consumer_defensive = raw consumer_defensive, 
            energy = raw energy,
            financial_services = raw financial_services,
            healthcare = raw healthcare,
            industrials = raw industrials, 
            real_estate = raw real_estate,
            technology = raw technology, 
            utilities = raw utilies, 
        )
        add sector to sector_performance 
    
    CATCH missing or invalid quote data 
        log that this quote could not be normalized 
        CONTINUE 

    def pick_best_and_worst(sectors: list[SectorPerformance]) -> tuple[SectorPerformance, SectorPerformance]: 
        


'''