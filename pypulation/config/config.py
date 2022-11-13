import duckdb

from numpy import array, append
from pandas import DataFrame

class Logging:
    logging_enabled = True
    logging_results = {
        'populations': {
            "agent_alias": array([], str),
            "population": array([], float),
        }
    }

    def logger_append(self, key, value):
        self.logging_results["populations"][key] = append(self.logging_results["populations"][key], value)

    def cache_logger(self):
        con = duckdb.connect(database = "pypulation_logs.duckdb")
        log_results_df = DataFrame(self.logging_results["populations"])
        con.execute("create or replace table populations as (select * from log_results_df)")

logging = Logging()
