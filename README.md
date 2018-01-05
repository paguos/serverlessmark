# serverless-mark
A simple benchmark for serverless applications runtimes based on the [faasmark](https://github.com/gobinaris/faasmark) benchmark.

The benchmark currently tests latency under different:
* Load conditions
* FaaS providers

## Architecture

Benchmark code is divided into two parts:

1. **Client** is the code that drives the benchmark process.
2. **Empty** is a FaaS function that retuns immediately after invocation. This function is deployed on the FaaS platform being benchmarked. Empty is implemented is Python or JavaScript across on platforms. 
3. **Sleep** is a FaaS function that is deployed on the platform being benchmarked. Is a more complex version of empty for concurrency test. It can sleep for a specified interval before retuning. This feature is used for *warming up* multiple functions containers before starting the benchmark itself.

## Usage

In order to perform the benchmark you first need to deploy functions to the different FaaS provider platforms. See how to below.

Invoke the benchmark:

    python serverless-mark.py [-command] [-runtime]
    
This are the supported commnads: 

| Name | Arguments | Description |
| ---- | --------- | ----------- |
| `add`            | -                | Adds a runtime into the `settings.json` file |
| `config`         | -, runtime_name  | Configure the settings of the benchmark tool or the information of individual runtimes |
| `clean`          | -                | Remove the logs created by this benchmark |
| `run`            | runtime_name     | Runs the benchmark in an specific runtime |

Benchmark behavior is control by the file *settings.json* which has the following fields:

| Name | Values | Description |
| ---- | ------ | ----------- |
| `concurrencyRepeat`          | Number              | Same as repeat for concurrency (load) tests |
| `maxConcurrency`             | Number              | Maximum concurrent invocations (load level)                     |
| `maxConcurrencyPerInitiator` | Number              | Maximum concurrent invocations from a single initiator function |
| `repeat`                     | Number              | How many times Empty is invoked by Initiator |
| `runtimes`                   | Dictionary          | Information about the registered runtimes |
| `sleep`                      | Number              | Interval of time between concurrency tests (in seconds) |
| `warmUp`                     | Number              | Interval of time for the warm up before the concurrency tests |

## Deployment

The deployment method of the two functions varies between runtimes.

### Apache OpenWhisk
```sh
cd runtimes/openwhisk/
wsk action create empty empty.py  --web true -i
wsk api create /serverlessmark /empty post empty --response-type json -i
wsk action create sleep sleep.py  --web true -i
wsk api create /serverlessmark /sleep post sleep --response-type json -i
```

### Azure Functions Core Tools
```sh
cd runtimes/azure-functions-ct
func host start
```

### Fn Project

```sh
cd runtimes/fn/empty
fn deploy --app serverlessmark --local
cd ../sleep
fn deploy --app serverlessmark --local
```

### Kubeless
```sh
cd runtimes/kubeless/
kubeless function deploy empty --runtime python2.7 --from-file empty.py --handler empty.foobar --trigger-http
kubeless function deploy sleep --runtime python2.7 --from-file sleep.py --handler sleep.foobar --trigger-http
```

### OpenFaaS

```sh
cd runtimes/openfaas/empty
faas-cli build -f ./empty.yml
faas-cli deploy -f ./empty.yml
cd ../sleep
faas-cli build -f ./sleep.yml
faas-cli deploy -f ./sleep.yml
```

### Snafu

```sh
cd runtimes/snafu
snafu-control *
```
