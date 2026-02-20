window.BENCHMARK_DATA = {
  "lastUpdate": 1771605262177,
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
      },
      {
        "commit": {
          "author": {
            "email": "ezequiel.grondona@gmail.com",
            "name": "Checho3388",
            "username": "Checho3388"
          },
          "committer": {
            "email": "ezequiel.grondona@gmail.com",
            "name": "Checho3388",
            "username": "Checho3388"
          },
          "distinct": true,
          "id": "b28675f7466df39c809815e7941f7d76c26f826d",
          "message": "docs: Add comprehensive Sphinx-based documentation\n\n- Introduced Sphinx-based documentation with a modern \"furo\" theme, hosted on Read the Docs.\n- Added guides for installation, getting started, custom estimators, framework integrations, and advanced usage.\n- Created a changelog following \"Keep a Changelog\" format.\n- Included a `docs/requirements.txt` file for building documentation locally.\n- Added `.readthedocs.yml` for Read the Docs configuration.\n- Updated LICENSE year to 2026.",
          "timestamp": "2026-02-19T21:46:12-03:00",
          "tree_id": "7045f7636db43a02cad9fe8f1d194a1d4a3487e5",
          "url": "https://github.com/Checho3388/graphql-complexity/commit/b28675f7466df39c809815e7941f7d76c26f826d"
        },
        "date": 1771548443508,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_simple_query",
            "value": 1192.2631311935393,
            "unit": "iter/sec",
            "range": "stddev: 0.0005116867391828945",
            "extra": "mean: 838.7410243902532 usec\nrounds: 656"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_complex_query",
            "value": 451.9658911004658,
            "unit": "iter/sec",
            "range": "stddev: 0.000791187199733315",
            "extra": "mean: 2.2125563448276093 msec\nrounds: 435"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_deep_query",
            "value": 203.8074945574119,
            "unit": "iter/sec",
            "range": "stddev: 0.0004702120082980255",
            "extra": "mean: 4.906590909090947 msec\nrounds: 44"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_simple_query",
            "value": 1016.7042884585181,
            "unit": "iter/sec",
            "range": "stddev: 0.0006503054674969161",
            "extra": "mean: 983.5701603227774 usec\nrounds: 867"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_complex_query",
            "value": 376.89620983046257,
            "unit": "iter/sec",
            "range": "stddev: 0.0011324948884666192",
            "extra": "mean: 2.653250348285076 msec\nrounds: 379"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_deep_query",
            "value": 174.14319992392308,
            "unit": "iter/sec",
            "range": "stddev: 0.0025899236944209574",
            "extra": "mean: 5.742400509677462 msec\nrounds: 155"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_simple_query",
            "value": 1008.0046614814553,
            "unit": "iter/sec",
            "range": "stddev: 0.0008872833409733987",
            "extra": "mean: 992.0589043014038 usec\nrounds: 930"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_complex_query",
            "value": 374.2071642037811,
            "unit": "iter/sec",
            "range": "stddev: 0.0016402873645285343",
            "extra": "mean: 2.672316555263577 msec\nrounds: 380"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_deep_query",
            "value": 177.69496564842933,
            "unit": "iter/sec",
            "range": "stddev: 0.0022410958591569095",
            "extra": "mean: 5.627621448648729 msec\nrounds: 185"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_simple_query",
            "value": 985.2943209834444,
            "unit": "iter/sec",
            "range": "stddev: 0.0013936665482910556",
            "extra": "mean: 1.0149251636829466 msec\nrounds: 782"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_complex_query",
            "value": 386.52284496747774,
            "unit": "iter/sec",
            "range": "stddev: 0.0002195176778255223",
            "extra": "mean: 2.5871692010446123 msec\nrounds: 383"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_deep_query",
            "value": 175.13338958056323,
            "unit": "iter/sec",
            "range": "stddev: 0.0032831558513623685",
            "extra": "mean: 5.709933453551924 msec\nrounds: 183"
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
          "id": "db4f6353965b1bd808cf2a3fafc3284ff6d614cc",
          "message": "Change package ecosystem from poetry to pip",
          "timestamp": "2026-02-20T13:33:45-03:00",
          "tree_id": "4a2166659f0cd77defc5fb79bfde850f15db75f5",
          "url": "https://github.com/Checho3388/graphql-complexity/commit/db4f6353965b1bd808cf2a3fafc3284ff6d614cc"
        },
        "date": 1771605261524,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_simple_query",
            "value": 1067.670566663205,
            "unit": "iter/sec",
            "range": "stddev: 0.0005914916112690875",
            "extra": "mean: 936.6184956519913 usec\nrounds: 575"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_complex_query",
            "value": 389.0335934603051,
            "unit": "iter/sec",
            "range": "stddev: 0.0008991749821887588",
            "extra": "mean: 2.5704721052631525 msec\nrounds: 380"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_without_extension_deep_query",
            "value": 170.47119257531713,
            "unit": "iter/sec",
            "range": "stddev: 0.0020774444644619406",
            "extra": "mean: 5.866093765714595 msec\nrounds: 175"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_simple_query",
            "value": 906.6632122682074,
            "unit": "iter/sec",
            "range": "stddev: 0.0007632414417491577",
            "extra": "mean: 1.1029453786906067 msec\nrounds: 779"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_complex_query",
            "value": 322.84513210161276,
            "unit": "iter/sec",
            "range": "stddev: 0.0016404462744139085",
            "extra": "mean: 3.097460362776226 msec\nrounds: 317"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_simple_estimator_deep_query",
            "value": 147.31515367929737,
            "unit": "iter/sec",
            "range": "stddev: 0.0027101570530847006",
            "extra": "mean: 6.788167917721372 msec\nrounds: 158"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_simple_query",
            "value": 887.9385796711002,
            "unit": "iter/sec",
            "range": "stddev: 0.001256790133573956",
            "extra": "mean: 1.1262040223214633 msec\nrounds: 672"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_complex_query",
            "value": 331.97466826944,
            "unit": "iter/sec",
            "range": "stddev: 0.0002500015255909203",
            "extra": "mean: 3.0122780307694192 msec\nrounds: 325"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_directives_estimator_deep_query",
            "value": 157.85481025702225,
            "unit": "iter/sec",
            "range": "stddev: 0.0005127910317366445",
            "extra": "mean: 6.334935238094935 msec\nrounds: 21"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_simple_query",
            "value": 929.1345020603543,
            "unit": "iter/sec",
            "range": "stddev: 0.00017636675679232476",
            "extra": "mean: 1.0762704406977694 msec\nrounds: 860"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_complex_query",
            "value": 317.23772913135485,
            "unit": "iter/sec",
            "range": "stddev: 0.002407061194233732",
            "extra": "mean: 3.1522101823706534 msec\nrounds: 329"
          },
          {
            "name": "tests/benchmarks/test_benchmark_strawberry_extension.py::test_arguments_estimator_deep_query",
            "value": 155.781981216068,
            "unit": "iter/sec",
            "range": "stddev: 0.0006621103633569201",
            "extra": "mean: 6.41922764233567 msec\nrounds: 137"
          }
        ]
      }
    ]
  }
}