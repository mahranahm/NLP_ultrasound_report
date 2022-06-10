from schema import Schema, Optional


config_schema = Schema(
    {
        "schema": "preproc_and_train",
        "dataset": {
            "path": str,
        },
        "preprocessing": {
            "patterns_to_remove": list,
            "lowercase": bool,
            "split_measure_text": bool,
            "tokenizer_type": str,
        },
        "training": {
            "vectorizer": {
                "vectorizer_type": str,
                "remove_stopwords": bool,
                "ngram_range": list,
                Optional("binary", default=False): bool,
            },
            "model": {
                "model_type": str,
                # The rest of the paramas are specific to the model
                "model_params": dict,
            }
        },
    }
)
