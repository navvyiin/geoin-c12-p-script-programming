# Performance Evaluation

The benchmark measures three complete end-to-end runs of the automated spatial analysis workflow using the supplied synthetic data.

## Measurement method

- Timing uses Python `time.perf_counter()` for wall-clock elapsed time.
- The same input datasets and parameters are used for each run.
- Three runs are recorded to show run-to-run variability.

## Demonstration benchmark

The supplied environment produced:

| Run | Time (s) |
|---:|---:|
| 1 | 0.137778 |
| 2 | 0.297139 |
| 3 | 0.251559 |
| **Mean** | **0.228826** |
| **Sample standard deviation** | **0.082077** |

These numbers are illustrative for the development environment used to validate the project. Results on a student's computer will vary with processor, Python environment, storage, dataset size and library versions.

## Interpretation

Automation does not make every individual GIS operation faster than a highly skilled manual operator. Its main value is removing repeated interaction and enforcing the same sequence of operations and parameters across datasets. That advantage becomes more important as the number of inputs increases. The batch-processing module demonstrates this repeatability by applying the same operation to multiple layers without manually reopening and configuring each one.
