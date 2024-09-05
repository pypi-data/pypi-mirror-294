# Nomadic

Nomadic enables ML engineering teams to deploy and maintain LLM systems in production confidently. Teams use Nomadic to eliminate guesswork and ensure quality. Nomadic is a partner toolkit throughout an LLM app development lifecycle, offering features from prompt tuning, to systematic fine-tuning, to testing and evaluations, all in one centralized experimentation platform.


# Installation

You can install `nomadic` with pip (Python 3.8+ required):

```bash
pip install nomadic
```

# Expected Use Case of Nomadic

## With Experiment

```python
from nomadic.experiment import Experiment
from nomadic.model import SagemakerModel, OpenAIModel
from nomadic.tuner import tune

from llama_index.core.evaluation import BatchEvalRunner

experiment = Experiment(
    name = "Sample_Nomadic_Experiment",
    model = SagemakerModel(...), # or OpenAIModel
    evaluator = BatchEvalRunner(...),
    params = {'temperature','top_k'}
    current_hp_values = { # Optional
        'temperature'=0.5,
        'top_k'=5,
        'top_p'=8
    },
    evaluation_dataset = {
        {
            'Context': "You are a helpful assistant writing a transcript for ...",
            'Instruction': "Absolutely do not hallucinate. Capture all relevant ...",
            'Answer': "The generated summary is shown below: ..."
        }
    }
)
results = experiment.run(
    param_dict={
        'temperature': tune.choice([0.1, 0.3, 0.5, 0.7, 0.9])
        'top_k': tune.choice([3,5])
    })
```

## With ParamTuner

```python
import os

from openai import OpenAI
from ray import tune

from nomadic.tuner import ParamTuner, tune

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

def objective_function(param_dict):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Knock knock."},
            {"role": "assistant", "content": "Who's there?"},
            {"role": "user", "content": "Orange."},
        ],
        temperature=param_dict['temperature'],
        top_k=param_dict['top_k'],
        top_p=param_dict['top_p']
    )
    return response == "Orange who?"

param_tuner = ParamTuner(
    param_fn=objective_function,
    param_dict={
        'temperature': tune.choice([0.1, 0.3, 0.5, 0.7, 0.9]),
        'top_k':tune.choice([3, 5])
    },
    fixed_param_dict={
        'top_p':5
    },
)
results = param_tuner.fit()

print(f"Score: {results.best_run_result.score}")
print(f"Top-k: {results.best_run_result.params["top_k"]}")
print(f"Temperature: {results.best_run_result.params["temperature"]}")
```
