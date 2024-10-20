# -*- coding: utf-8 -*-
"""train_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QLYEggMhS0_fMXzvhpDK-dWNxewQGFnK
"""

! git clone https://github.com/Shruti0457/Inception.git

import pandas as pd
import os
import numpy as np
from collections import Counter

!python --version

"""## Loading the files"""

def load_labels_from_csv(csv_file):
    """Load labels from the given CSV file."""
    df = pd.read_csv(csv_file)
    return df[['file_id', 'label']]

def load_data_from_directory(directory, labels_df):
    """Load text data from the directory and map labels."""
    texts = []
    labels = []

    # Create a mapping of file_id to label
    label_map = {row['file_id']: row['label'] for index, row in labels_df.iterrows()}

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  # Check if the file is a .txt file
            file_id = filename.split('.')[0]
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read().strip()  # Read the text from the file
                texts.append(text)

                # Assign label based on file_id
                if file_id in label_map:
                    labels.append(label_map[file_id])
                else:
                    continue  # Skip files that don't have a corresponding label

    return texts, labels

# Load labels from the CSV file
labels_csv_path = '/content/Inception/data/annotations_metadata.csv'
labels_df = load_labels_from_csv(labels_csv_path)
labels_df['label'] = labels_df['label'].map({'hate': 1, 'noHate': 0})

# Load training data
train_directory = '/content/Inception/data/sampled_train'
train_texts, train_labels = load_data_from_directory(train_directory, labels_df)

# Load testing data
test_directory = '/content/Inception/data/sampled_test'
test_texts, test_labels = load_data_from_directory(test_directory, labels_df)

train_labels = np.array(train_labels).astype(int)
test_labels = np.array(test_labels).astype(int)

len(train_texts)

Counter(train_labels)

"""The dataset is balanced so wouldn't have to take any extra steps for a balanced data."""

len(test_texts)

#Checking for GPUs
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"GPUs available: {gpus}")
else:
    print("No GPU available")

"""## Building the classification model using BERT"""

import pandas as pd
import tensorflow as tf
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.metrics import classification_report
from transformers import Trainer, TrainingArguments
from transformers import EarlyStoppingCallback
import torch

# Initialize BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize the input texts
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=128)

# Create a Dataset class
class HateSpeechDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Create datasets
train_dataset = HateSpeechDataset(train_encodings, train_labels)
test_dataset = HateSpeechDataset(test_encodings, test_labels)

# Load the BERT model for sequence classification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

# Move model to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

training_args = TrainingArguments(
    output_dir='/content/Inception/results',         # Output directory
    num_train_epochs=3,
    per_device_train_batch_size=16,   # Batch size for training
    per_device_eval_batch_size=64,    # Batch size for evaluation
    warmup_steps=500,                  # Number of warmup steps for learning rate scheduler
    weight_decay=0.02,
    logging_dir='./logs',              # Directory for storing logs
    logging_steps=10,
    evaluation_strategy="epoch",       # Evaluation strategy
    save_strategy="epoch",             # Save strategy
    load_best_model_at_end=True,      # Load the best model when finished training
    metric_for_best_model="loss",      # Metric to use to compare models
    greater_is_better=False,            # Lower loss is better
    learning_rate=5e-5,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=1)],  # Early stopping because the model is starting to overfit
)

# Train the model
trainer.train()

# Evaluate the model
predictions, labels, _ = trainer.predict(test_dataset)
preds = np.argmax(predictions, axis=1)

# Print classification report
print(classification_report(test_labels, preds, target_names=['noHate', 'hate']))

# Saving the classification report to results directory
report = classification_report(test_labels, preds, target_names=['noHate', 'hate'])

with open('/content/Inception/results/classification_report.txt', 'w') as f:
    f.write(report)

model.save_pretrained('/content/Inception/models')
tokenizer.save_pretrained('/content/Inception/models')

