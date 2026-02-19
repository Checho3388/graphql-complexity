window.BENCHMARK_DATA = {
  "lastUpdate": 1771544259789,
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
      },
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
          "id": "a33ceb4da3ba14889403461181c0fc8c4339ed3f",
          "message": "Merge pull request #20 from Checho3388/v1.0.0\n\nv1.0.0 Release PR",
          "timestamp": "2026-02-19T20:37:00-03:00",
          "tree_id": "5eaac36e10688c31f6678948ae7478938821b443",
          "url": "https://github.com/Checho3388/graphql-complexity/commit/a33ceb4da3ba14889403461181c0fc8c4339ed3f"
        },
        "date": 1771544258787,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_simple_query",
            "value": 1076.6571515874018,
            "unit": "iter/sec",
            "range": "stddev: 0.0005633382041572929",
            "extra": "mean: 928.8007779687526 usec\nrounds: 581"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_complex_query",
            "value": 386.7439531815795,
            "unit": "iter/sec",
            "range": "stddev: 0.0009318244133513752",
            "extra": "mean: 2.585690071618241 msec\nrounds: 377"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_deep_query",
            "value": 169.8703976339479,
            "unit": "iter/sec",
            "range": "stddev: 0.001972186038384035",
            "extra": "mean: 5.886840873563448 msec\nrounds: 174"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_simple_query",
            "value": 903.8201221658579,
            "unit": "iter/sec",
            "range": "stddev: 0.0008037055072720953",
            "extra": "mean: 1.1064148445861801 msec\nrounds: 785"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_complex_query",
            "value": 328.8789589346515,
            "unit": "iter/sec",
            "range": "stddev: 0.0002556979733075905",
            "extra": "mean: 3.0406323446149703 msec\nrounds: 325"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_deep_query",
            "value": 150.205913242468,
            "unit": "iter/sec",
            "range": "stddev: 0.0024202344800707356",
            "extra": "mean: 6.657527512820102 msec\nrounds: 156"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_simple_query",
            "value": 926.8886153407409,
            "unit": "iter/sec",
            "range": "stddev: 0.0001812661821829641",
            "extra": "mean: 1.0788782853184382 msec\nrounds: 722"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_complex_query",
            "value": 317.4982605669389,
            "unit": "iter/sec",
            "range": "stddev: 0.00224115652304345",
            "extra": "mean: 3.1496235545176092 msec\nrounds: 321"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_deep_query",
            "value": 155.89440606991346,
            "unit": "iter/sec",
            "range": "stddev: 0.0005315558584792041",
            "extra": "mean: 6.414598350318825 msec\nrounds: 157"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_simple_query",
            "value": 932.6695916055461,
            "unit": "iter/sec",
            "range": "stddev: 0.0001717809076396612",
            "extra": "mean: 1.0721910620872155 msec\nrounds: 757"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_complex_query",
            "value": 330.36103474903194,
            "unit": "iter/sec",
            "range": "stddev: 0.00024944804819781465",
            "extra": "mean: 3.026991366459662 msec\nrounds: 322"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_deep_query",
            "value": 147.20068181518985,
            "unit": "iter/sec",
            "range": "stddev: 0.004266230190215269",
            "extra": "mean: 6.7934467943259795 msec\nrounds: 141"
          }
        ]
      }
    ]
  }
}