window.BENCHMARK_DATA = {
  "lastUpdate": 1771543043464,
  "repoUrl": "https://github.com/Checho3388/graphql-complexity",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "ezequiel.grondona@gmail.com",
            "name": "Cheche",
            "username": "Checho3388"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c58a95420e3cb22d8ed2e494536cc1b0adf8d6b0",
          "message": "Merge pull request #19 from Checho3388/feat/improve-perf-add-benchmark\n\nFeat/improve perf add benchmark",
          "timestamp": "2026-02-19T20:16:43-03:00",
          "tree_id": "5678f59b216e1d30963d5c1fa533238c417d3768",
          "url": "https://github.com/Checho3388/graphql-complexity/commit/c58a95420e3cb22d8ed2e494536cc1b0adf8d6b0"
        },
        "date": 1771543043143,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_simple_query",
            "value": 1062.6514850311244,
            "unit": "iter/sec",
            "range": "stddev: 0.0006061601319412926",
            "extra": "mean: 941.0423022847522 usec\nrounds: 569"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_complex_query",
            "value": 388.21403854268283,
            "unit": "iter/sec",
            "range": "stddev: 0.0009807108615655378",
            "extra": "mean: 2.5758986041666634 msec\nrounds: 384"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_deep_query",
            "value": 171.39575550751732,
            "unit": "iter/sec",
            "range": "stddev: 0.0020615440812377485",
            "extra": "mean: 5.8344502000000835 msec\nrounds: 170"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_simple_query",
            "value": 898.0362982164091,
            "unit": "iter/sec",
            "range": "stddev: 0.0007668444574182909",
            "extra": "mean: 1.1135407354759501 msec\nrounds: 809"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_complex_query",
            "value": 323.55422300306816,
            "unit": "iter/sec",
            "range": "stddev: 0.001466274202679611",
            "extra": "mean: 3.0906720694865335 msec\nrounds: 331"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_deep_query",
            "value": 153.2417448288845,
            "unit": "iter/sec",
            "range": "stddev: 0.0023434485883387164",
            "extra": "mean: 6.525637000000475 msec\nrounds: 146"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_simple_query",
            "value": 900.3930909895865,
            "unit": "iter/sec",
            "range": "stddev: 0.001080165601571073",
            "extra": "mean: 1.1106260254628781 msec\nrounds: 864"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_complex_query",
            "value": 333.23979597646434,
            "unit": "iter/sec",
            "range": "stddev: 0.0003088838867107199",
            "extra": "mean: 3.000842072507531 msec\nrounds: 331"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_deep_query",
            "value": 151.31153019388594,
            "unit": "iter/sec",
            "range": "stddev: 0.0032575943767872736",
            "extra": "mean: 6.608881680851622 msec\nrounds: 141"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_simple_query",
            "value": 893.2469777772152,
            "unit": "iter/sec",
            "range": "stddev: 0.0012583538929140633",
            "extra": "mean: 1.119511204491766 msec\nrounds: 846"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_complex_query",
            "value": 333.65762699809335,
            "unit": "iter/sec",
            "range": "stddev: 0.000247016483219177",
            "extra": "mean: 2.997084193749644 msec\nrounds: 320"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_deep_query",
            "value": 149.80105646841284,
            "unit": "iter/sec",
            "range": "stddev: 0.004169754950876447",
            "extra": "mean: 6.675520343949381 msec\nrounds: 157"
          }
        ]
      }
    ]
  }
}