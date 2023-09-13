def dataAggregator(data, aggregate_keys, aggregation_name, operation='sum'):
    
    #get original keys
    keys = data[0]
    aggregated_values = data[1:]
    
    #create index list
    index_list = [keys.index(key) for key in aggregate_keys]
    newInsertIndex = index_list[0]
    
    #create new key list
    for index in sorted(index_list, reverse=True):
        del keys[index]    
    keys.insert(newInsertIndex, aggregation_name)

    #init result with keys
    result = [keys]
    
    for values in aggregated_values:
        indexes = [values[index] for index in index_list]

        #remove summed values
        for index in sorted(index_list, reverse=True):
            del values[index]        
        
        aggreageted_value = sum(indexes)

        #insert aggreamted value
        values.insert(newInsertIndex, aggreageted_value)
        result.append(values)
        
    return result