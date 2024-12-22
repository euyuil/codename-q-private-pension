from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Union

import xarray as xr
from data_module.data_api import DataManager

from app.models import views

@dataclass
class BenchmarkCon:
    security: str
    weight: float

@dataclass
class BenchmarkSegment:
    constituents: List[BenchmarkCon]
    effective_start_date: date
    effective_end_date: date

def _get_benchmark_segments(fund_id: int) -> List[BenchmarkSegment]:
    fund_benchmarks = views.FundBenchmark.query.filter_by(fund_id=fund_id).all()
    benchmark_dict: Dict[int, List[views.FundBenchmark]] = {}
    for fund_benchmark in fund_benchmarks:
        benchmark_dict.setdefault(fund_benchmark.benchmark_id, list()) \
                      .append(fund_benchmark)

    benchmark_segments: List[BenchmarkSegment] = []
    for _, benchmark_list in benchmark_dict.items():
        benchmark_cons: List[BenchmarkCon] = []
        for benchmark in benchmark_list:
            benchmark_cons.append(BenchmarkCon(
                security=benchmark.constituent_security_code,
                weight=benchmark.constituent_weight
            ))
        benchmark_segments.append(BenchmarkSegment(
            constituents=benchmark_cons,
            effective_start_date=benchmark_list[0].effective_start_date,
            effective_end_date=benchmark_list[0].effective_end_date
        ))

    return benchmark_segments

def get_benchmark_data(fund_id: str, start_date: date, end_date: date) -> List[Dict[str, Union[str, float]]]:
    benchmark_segments = _get_benchmark_segments(fund_id)

    benchmark_securities: List[str] = []
    for benchmark_segment in benchmark_segments:
        benchmark_securities.extend(benchmark_con.security for benchmark_con in benchmark_segment.constituents)
    benchmark_securities = list(dict.fromkeys(benchmark_securities))

    data_manager = DataManager()
    ds = data_manager.get_data(
        start=start_date,
        end=end_date,
        frequency="1d",
        securities=benchmark_securities,
        fields=["AdjClose"]
    )

    da_weight = xr.zeros_like(ds["AdjClose"])
    for benchmark_segment in benchmark_segments:
        for benchmark_con in benchmark_segment.constituents:
            # Set da_weight to benchmark_con.weight, where
            # datetime between benchmark_segment.effective_start_date and benchmark_segment.effective_end_date, and
            # security is benchmark_con.security
            da_weight.loc[{"datetime": slice(benchmark_segment.effective_start_date, benchmark_segment.effective_end_date),
                           "security": benchmark_con.security}] = benchmark_con.weight

    da = ds["AdjClose"] * da_weight
    da = da.sum(dim="security", skipna=False)
    s = da.to_pandas().dropna()
    datetimes = [i.strftime("%Y-%m-%d") for i in s.index]
    values = [i.item() for i in s.values]
    return [{"datetime": datetime, "AdjClose": value} for datetime, value in zip(datetimes, values)]
