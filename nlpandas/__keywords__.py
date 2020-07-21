key_words =  {
                "aggregation" : {
                    "avarage": {
                        "keywords": [
                            "average",
                            "avg",
                            "mean",
                            "avrg"
                        ],
                        "pd_func": "mean",
                        "sql_func": "avg"
                    },
                    "sum": {
                        "keywords": [
                            "total sum",
                            "total",
                            "sum",
                            "how much"
                        ],
                        "pd_func": "sum",
                        "sql_func": "sum"
                    },
                    "min": {
                        "keywords": [
                            "minimum",
                            "lowest",
                            "min",
                            "smallest"
                        ],
                        "pd_func": "min",
                        "sql_func": "min"
                    },
                    "max": {
                        "keywords": [
                            "maximun",
                            "max",
                            "highest",
                            "greatest"
                        ],
                        "pd_func": "max",
                        "sql_func": "max"
                    },
                    "count": {
                        "keywords": [
                            "total count",
                            "count",
                            "many",
                            "how many"
                        ],
                        "pd_func": "count",
                        "sql_func": "count"
                    }
                },
                "filter":{
                    "where" : {
                        "keywords":[
                            "of",
                            "in",
                            "where"
                        ],
                        "pd_func": "filter",
                        "sql_func": "count"
                    },
                    "and" :{
                        "keywords":[
                            "and"
                        ],
                        "pd_func" : "&",
                        "sql_func" : "and"
                    },
                    "or" :{
                        "keywords":[
                            "or",
                            "either"
                        ],
                        "pd_func" : "||",
                        "sql_func" : "and"
                    },
                    "greater" : {
                        "keywords":[
                            "greater",
                            "over",
                            "greater than",
                            "over than"
                        ],
                        "pd_func" : ">",
                        "sql_func" : ">"
                    },
                    "lower" : {
                        "keywords":[
                            "lower",
                            "less",
                            "lower than",
                            "less than"
                        ],
                        "pd_func" : ">",
                        "sql_func" : ">"
                    },
                    "equal":{
                        "keywords":[
                            "equal",
                            "equal to",
                            "is equal to",
                            "are equal to"               
                        ],
                        "pd_func" : "sort_values",
                        "sql_func" : "order by"
                    },
                    "order":{
                        "keywords":[
                            "order",
                            "seq",
                            "sequence",
                            "sequence by",
                            "ordered",
                            "ordered by"
                        ],
                        "pd_func" : "sort_values",
                        "sql_func" : "order by"
                    },
                    "asc" :{
                        "keywords":[
                        "ascending",
                        "ascending by",
                        "increasing",
                        "increasing by"
                        ],
                        "pd_func" : "asc",
                        "sql_func" : ""
                    },
                    "dsc" :{
                        "keywords":[
                        "descending",
                        "descending by",
                        "decreasing",
                        "decreasing by"
                        ],
                        "pd_func" : "sort_values",
                        "sql_func" : "ascending=False"
                    }
                }
                
            }