# flake8: noqa
# pylint: skip-file
DEFAULT_PRE_CONFIG = {
    "characteristics": [
        {
            "key": "reliability",
            "weight": 25,
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "weight": 50,
                    "measures": [
                        {
                            "key": "passed_tests",
                            "weight": 33,
                            "min_threshold": 0,
                            "max_threshold": 1,
                        },
                        {
                            "key": "test_builds",
                            "weight": 33,
                            "min_threshold": 0,
                            "max_threshold": 300000,
                        },
                        {
                            "key": "test_coverage",
                            "weight": 34,
                            "min_threshold": 60,
                            "max_threshold": 100,
                        },
                    ],
                },
                {
                    "key": "maturity",
                    "weight": 50,
                    "measures": [
                        {
                            "key": "ci_feedback_time",
                            "weight": 100,
                            "min_threshold": 1,
                            "max_threshold": 900,
                        }
                    ],
                },
            ],
        },
        {
            "key": "maintainability",
            "weight": 25,
            "subcharacteristics": [
                {
                    "key": "modifiability",
                    "weight": 100,
                    "measures": [
                        {
                            "key": "non_complex_file_density",
                            "weight": 33,
                            "min_threshold": 0,
                            "max_threshold": 10,
                        },
                        {
                            "key": "commented_file_density",
                            "weight": 33,
                            "min_threshold": 10,
                            "max_threshold": 30,
                        },
                        {
                            "key": "duplication_absense",
                            "weight": 34,
                            "min_threshold": 0,
                            "max_threshold": 5,
                        },
                    ],
                }
            ],
        },
        {
            "key": "functional_suitability",
            "weight": 25,
            "subcharacteristics": [
                {
                    "key": "functional_completeness",
                    "weight": 100,
                    "measures": [
                        {
                            "key": "team_throughput",
                            "weight": 100,
                            "min_threshold": 45,
                            "max_threshold": 100,
                        },
                    ],
                }
            ],
        },
        {
            "key": "performance_efficiency",
            "weight": 25,
            "subcharacteristics": [
                {
                    "key": "resource_utilization",
                    "weight": 50,
                    "measures": [
                        {
                            "key": "cpu_utilization",
                            "weight": 50,
                            "min_threshold": 0.0,
                            "max_threshold": 0.33,
                        },
                        {
                            "key": "memory_utilization",
                            "weight": 50,
                            "min_threshold": 0.0,
                            "max_threshold": 0.33,
                        },
                    ],
                },
                {
                    "key": "time_behaviour",
                    "weight": 50,
                    "measures": [
                        {
                            "key": "response_time",
                            "weight": 100,
                            "min_threshold": 0.0,
                            "max_threshold": 0.66,
                        },
                    ],
                },
            ],
        },
    ]
}
