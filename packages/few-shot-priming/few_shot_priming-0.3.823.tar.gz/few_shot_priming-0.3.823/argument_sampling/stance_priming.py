import pandas as pd
from sentence_transformers import SentenceTransformer, losses, SentencesDataset, datasets
from sentence_transformers.evaluation import BinaryClassificationEvaluator
from sentence_transformers.readers import InputExample


def preprocess_dataset(dataset):
    for split in dataset:
        dataset[split]["topic-text"] = dataset[split].apply(lambda record: record["topic"] + "[SEP]" + record["text"], axis=1)

def generate_test_dataset(df, three_classes=False):
    list1 = []
    list2 = []
    labels = []
    for topic, df_topic in df.groupby("topic"):
        df_stances = list(df_topic.groupby("stance"))
        if len(df_stances)<2 or (three_classes and len(df_stances)<3)   :
            continue
        df_stance_1 = df_stances[0][1]
        df_stance_2 = df_stances[1][1]
        if not len(df_stance_1) or not len(df_stance_2):
            continue

        if three_classes:
            df_stance_3 = df_stances[2][1]
            if not len(df_stance_3) and not len(df_stance_2):
                continue

        for i, argument in df_topic.iterrows():
            for j, argument_2 in df_topic.iterrows():
                if j>i:
                    list1.append(argument["topic-text"])
                    list2.append(argument_2["topic-text"])
                    if argument["stance"] == argument_2["stance"]:
                        label = 1
                    else:
                        label = 0
                    labels.append(label)

    return list1, list2, labels

def train(model, params, train_dataloader, evaluator=None, output_model_path=None):


    learning_rate = params["lr"]
    epochs = params["epochs"]
    train_loss = losses.ContrastiveLoss(model=model)
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        optimizer_params = {'lr' : learning_rate},
        output_path=output_model_path,
        epochs=epochs,
        evaluator=evaluator,
        save_best_model=True,
        evaluation_steps=1000
    )
    return model

def create_evaluator(df_test, three_examples=False):
    list1, list2, labels = generate_test_dataset(df_test, three_examples)
    evaluator = BinaryClassificationEvaluator(list1, list2, labels,show_progress_bar=True)
    return evaluator


def generate_training_examples(df_training, three_classes=False):
    contrastive_examples = []
    guid = 0
    for topic, df_topic in df_training.groupby("topic"):
        df_stances = list(df_topic.groupby("stance"))
        if len(df_stances)<2 or (three_classes and len(df_stances)<3):
            continue
        df_stance_1 = df_stances[0][1]
        df_stance_2 = df_stances[1][1]

        if not len(df_stance_1) or not len(df_stance_2):
            continue
        if three_classes:
            df_stance_3 = df_stances[2][1]
            if not len(df_stance_3) or not len(df_stance_2):
                continue
        for i, argument in df_topic.iterrows():
            for j, argument_2 in df_topic.iterrows():
                if j>i:
                    pair = [argument["topic-text"], argument_2["topic-text"]]
                    if argument["stance"] == argument_2["stance"]:
                        label = 1
                    else:
                        label = 0
                    guid = guid + 1
            contrastive_examples.append(InputExample(texts=pair, label=label, guid=guid))

    return contrastive_examples
8