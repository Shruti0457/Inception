# NLP Challenge for Core42 AI Modelling team

## Goal
Build a basic text classification model using any framework(PyTorch, Keras, etc..) and any technique as you wish.Deploy the final model via a REST API. We are not looking high performance numbers but the approach and thought process.

## Format Requirements
- Fork or clone this repo
- Maintain the directory structure given for the project
- Use Python 3.7+
- If you need additional imports specify them in `requirements.txt`

## Model Requirements
- Model should be trained on the given dataset.
- Create a model artifact and save it under `/models`.
- Report results on `sampled_test` and place it under `/results`.


## API Requirements
- Serve the model as a REST API using FastAPI on localhost 8080.
- Be able to use CURL to send in text input and return the prediction. 

### Documentation
- Create short walkthrough of your approach and thought process in `./project.md`.
- Include a sample curl command that can be used to call your API.

## Data
The dataset you will be using contains hate speech from an online forum. You need to train basic text classification model which will classify given text into `hate` `noHate` categories. You can find the dataset and details data format and labels can be found [here](https://github.com/Vicomtech/hate-speech-dataset/tree/master)

Dataset contains two splits `sampled_train` and `sampled_test`.

Note: The text in this dataset might contain offensive language.

## Submission
Timebox this challenge to 4-6 hours. After completing the assignment, please compress whole repo in `zip` format and send it as an attachment via email.
