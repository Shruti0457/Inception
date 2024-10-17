# Hate Speech Detection - Project Report
## Overview 
The goal of this project was to build a basic text classification model that classifies text as either "hate" or "noHate" using the provided dataset. The project involved model training, evaluation, and deployment via a REST API using FastAPI.
## Process
### 1. Data Understanding & Preprocessing
* The dataset consists of text from online forums labeled as either "hate" or "noHate".
* Data preprocessing included loading the texts from the directory and mapping the labels from the CSV file. The dataset was split into training and testing sets (`sampled_train` and `sampled_test`).
* Texts were tokenized and converted into a format suitable for input into the BERT model.
### 2. Model Selection
* BERT (Bidirectional Encoder Representations from Transformers) was chosen for its state-of-the-art performance in Natural Language Processing (NLP) tasks.
* Hugging Face's `transformers` library was used to load the pre-trained BERT model.
* The model was fine-tuned on the given dataset with appropriate learning rate, batch size, and training epochs.
* The classification report indicated a balanced performance across both classes with an overall accuracy of 81%:
    * Precision (noHate): 0.83
    * Recall (noHate): 0.79
    * F1-score (noHate): 0.81
    * Precision (hate): 0.80
    * Recall (hate): 0.84
    * F1-score (hate): 0.82
### 3. Overfitting Mitigation
* To prevent overfitting, I introduced early stopping based on validation loss, and applied weight decay in the BERT model.
* After tuning these hyperparameters, the model showed stable validation performance with no significant overfitting issues.
### 4. Model Saving and API Development
* The fine-tuned model and tokenizer were saved in the `/models` directory.
* FastAPI was chosen for deploying the model as a REST API. The model is served on localhost:8080 and accepts text input for prediction.
## API Details
The API accepts POST requests at the `/predict` endpoint. The input is a text string, and the output is a prediction of either hate or noHate.
### Sample CURL command
```
curl -X POST "http://<ngrok_url>/predict" \
-H "Content-Type: application/json" \
-d '{"text": "This is a hateful comment."}'
```
This command will return the prediction (`hate` or `noHate`) for the input text.

## Conclusion
The BERT-based model performed reasonably well with an accuracy of **81%**. While further tuning could improve the performance, the main focus of this project was on the approach and implementation of the API. The model is deployed using FastAPI and can be easily tested using the provided `curl` command.
