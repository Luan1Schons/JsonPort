# Benchmarking

Learn how to measure and optimize JsonPort performance.

## How to Run Benchmarks

### Running benchmarks with pytest-benchmark

```bash
pytest --benchmark-only -v
```

### Running specific benchmarks

```bash
pytest --benchmark-only tests/test_jsonport.py::test_serialization_benchmark -v
```

## Benchmark Examples

### Serialization Benchmark

```python
import pytest
from dataclasses import dataclass
from jsonport import dump

@dataclass
class BenchmarkData:
    id: int
    name: str
    values: list[float]
    metadata: dict[str, str]

@pytest.mark.slow
def test_serialization_benchmark(benchmark):
    test_data = BenchmarkData(
        id=1,
        name="test",
        values=[1.1, 2.2, 3.3] * 1000,
        metadata={"key1": "value1", "key2": "value2"}
    )
    result = benchmark(dump, test_data)
    assert isinstance(result, dict)
```

### Deserialization Benchmark

```python
@pytest.mark.slow
def test_deserialization_benchmark(benchmark):
    test_data = BenchmarkData(
        id=1,
        name="test",
        values=[1.1, 2.2, 3.3] * 1000,
        metadata={"key1": "value1", "key2": "value2"}
    )
    data = dump(test_data)
    result = benchmark(load, data, BenchmarkData)
    assert isinstance(result, BenchmarkData)
```

### File Operations Benchmark

```python
import tempfile
import os

@pytest.mark.slow
def test_file_operations_benchmark(benchmark):
    test_data = BenchmarkData(
        id=1,
        name="test",
        values=[1.1, 2.2, 3.3] * 100,
        metadata={"key1": "value1", "key2": "value2"}
    )
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    try:
        benchmark(dump_file, test_data, temp_file)
        benchmark(load_file, temp_file, BenchmarkData)
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
```

## Interpreting Results

```
--------------------------------------------------------------------------------------------- benchmark: 2 tests -----------------------------------------------------------------------------
Name (time in us)                       Min                 Max                Mean             StdDev              Median                IQR            Outliers  OPS (Kops/s)            Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_deserialization_benchmark     110.3460 (1.0)      263.2940 (1.0)      120.8443 (1.0)      12.3452 (1.0)      118.4470 (1.0)       6.0770 (1.0)       386;464        8.2751 (1.0)        6829           1
test_serialization_benchmark       251.4210 (2.28)     522.7470 (1.99)     270.2584 (2.24)     16.9108 (1.37)     266.3670 (2.25)     12.2920 (2.02)      218;161        3.7002 (0.45)       2499           1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

- **OPS**: operations per second (higher is better)
- **Mean**: average time per operation
- **StdDev**: variation in times
- **Outliers**: runs outside the normal range

## Benchmarking Tips

- Always run benchmarks on the same hardware for fair comparison
- Use multiple runs for more reliable results
- Compare with other methods (e.g., `json`, `pickle`) to evaluate gains

## Next Steps

- [Testing](testing.md) - How to run and write tests
- [Contributing](contributing.md) - How to contribute to the project
- [Performance](../user-guide/performance.md) - Performance optimization techniques 