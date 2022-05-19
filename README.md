# NLP ultrasound report
Project using NLP on ultrasound reports.

## Installation instructions
Create a new conda environment with
```
conda create -n env_name python=3.8
```

Activate your environment with
```
conda activate env_name
```

Install dependencies with

```
make setup
```

To visualize the expirements used in this repository, we use the `wandb` package/interface. Make an account here: [https://wandb.ai/site](https://wandb.ai/site). Once this is done, login with

```
wandb login
```

The first time you run a script with the `wandb` package dependency present, it will prompt you for your API key which you can find by following the instructions [here](https://docs.wandb.ai/quickstart). For the first time, it will also be necessary for the *project administrator* to add you to the dashboard. Email them at <cesare.spinoso-dipiano@mcgill.ca>. ***Skipping these steps may prevent you from running some of the experiments in the repository.***
