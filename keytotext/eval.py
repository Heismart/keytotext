            The model that will be used by the pipeline to make predictions.

            If not provided, the default for the :obj:`task` will be loaded.
    :param tokenizer:
    (:obj:`str` or `optional`):
            The tokenizer that will be used by the pipeline to encode data for the model. This can be a model
            identifier or an actual pretrained tokenizer inheriting from :class:`~transformers.PreTrainedTokenizer`.

            If not provided, the default tokenizer for the given :obj:`model` will be loaded (if it is a string).
    :param use_cuda:
    (:obj:`bool`, `optional`, defaults to :obj:`True`):
            Whether or not to use a GPU or not Default: True
    :return:
    (:class:):
            `K2TEval`: A Keytotext eval pipeline for the task.

    """

    if task not in SUPPORTED_TASKS:
        raise KeyError(
            "Unknown task {}, available tasks are {}".format(
                task, list(SUPPORTED_TASKS.keys())
            )
        )

    targeted_task = SUPPORTED_TASKS[task]
    task_class = targeted_task["impl"]

    if model is None:
        model = targeted_task["default"]["model"]

    if tokenizer is None:
        if isinstance(model, str):
            tokenizer = model
        else:
            # Impossible to guest what is the right tokenizer here
            raise Exception(
                "Please provided a PretrainedTokenizer "
                "class or a path/identifier to a pretrained tokenizer."
            )
    if isinstance(tokenizer, (str, tuple)):
        tokenizer = AutoTokenizer.from_pretrained(tokenizer)

    # Instantiate model if needed
    if isinstance(model, str):
        model = AutoModelForSeq2SeqLM.from_pretrained(model)

    if task == "k2t":
        return task_class(model=model, tokenizer=tokenizer, use_cuda=use_cuda)
    if task == "k2t-base":
        return task_class(model=model, tokenizer=tokenizer, use_cuda=use_cuda)


def eval():
    test = pd.read_csv("data/TestNLG.csv")
    keywords_test = test["input_text"]

    nlp = eval_pipeline("k2t")
    prediction = []
    for key in keywords_test:
        prediction.append(nlp(keywords=key))

    test["predctions"] = prediction

    return test
