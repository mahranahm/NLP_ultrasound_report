from schema import Schema


config_schema = Schema(
    {
        "schema": "preproc_and_train",
        "dataset": {
            "path": str,
        },
        "preprocessing": {
            "remove_stopwords": bool,
        },
        "model": {
            "model_type": str,
        },
    }
)
