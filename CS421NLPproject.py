{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "be307b97",
   "metadata": {},
   "source": [
    "# CS 421 Project"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "3f557e70",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import nltk\n",
    "import spacy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "71e561fe",
   "metadata": {},
   "outputs": [],
   "source": [
    "indexes_df = pd.read_csv('essays_dataset/index.csv', delimiter=';')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "b98c28d9",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>filename</th>\n",
       "      <th>prompt</th>\n",
       "      <th>grade</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1004355.txt</td>\n",
       "      <td>Do you agree or disagree with the following st...</td>\n",
       "      <td>low</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1007363.txt</td>\n",
       "      <td>Do you agree or disagree with the following st...</td>\n",
       "      <td>low</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1079196.txt</td>\n",
       "      <td>Do you agree or disagree with the following st...</td>\n",
       "      <td>high</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1086343.txt</td>\n",
       "      <td>Do you agree or disagree with the following st...</td>\n",
       "      <td>low</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1096747.txt</td>\n",
       "      <td>Do you agree or disagree with the following st...</td>\n",
       "      <td>low</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "      filename                                             prompt grade\n",
       "0  1004355.txt  Do you agree or disagree with the following st...   low\n",
       "1  1007363.txt  Do you agree or disagree with the following st...   low\n",
       "2  1079196.txt  Do you agree or disagree with the following st...  high\n",
       "3  1086343.txt  Do you agree or disagree with the following st...   low\n",
       "4  1096747.txt  Do you agree or disagree with the following st...   low"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "indexes_df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "68e1654c",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "directory = \"essays_dataset\\essays\"\n",
    "essays = {}\n",
    "\n",
    "for filename in os.listdir(directory):\n",
    "    if filename.endswith(\".txt\"):\n",
    "        file_path = os.path.join(directory, filename)\n",
    "        try:\n",
    "            with open(file_path, 'r', encoding='utf-8') as file:\n",
    "                essays[filename] = file.read()\n",
    "        except Exception as e:\n",
    "            print(f\"Error reading file {filename}: {e}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "c5140f22",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'This is an important aspect of today time.\\nThis products rathen are not much better, but today is not important the really character of the product, but only the money and the client not rappresented the important actor in this process.\\nEvery day any people buy same products that is not rappresented the your necessity, but is only important buy any product.\\nTo explain this argoment in my nation, at the television, there is an program that discuss of the problem rappresented by this.\\nMore people go to this program television to talk about your problem, that is very radicate in my nation.\\nThe modern society rappresented the perfect ambient to influenced the minds of all the person.\\nIn my self is present the reasons of this statement, that is one of the problem of the life.\\nBut not all the people and the time is in accord with this problem, because any time the person is too according with the make products.\\nThus I agree with this statement, because this event is present in my life every day, and rappresented the problem with I do fighting.\\nBut to explain all the aspect about this argoment is very inportant to illustre any examples.\\nThe television programs that every day introduce in the minds more argoment, news and other problem, or breaking news, is the first actor in this process.\\nThis opinion rappresented my self in my life, because for me the life of all the people is not possible to influence by the activity of any person.\\nThe society lose the propriety when this problem will rappresent the must argoment of the talk and the life of the people, because as very difficult live at a time with this argoment.\\nThe my request is that the new politics discuss about this problem.\\n'"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "essays['1004355.txt']"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5eae484b",
   "metadata": {},
   "source": [
    "### (a) Number of sentences and length"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5f1faf03",
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "\n",
    "def count_sentences(text):\n",
    "    # Split the text into sentences using regular expressions\n",
    "    sentences = re.split(r'(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?)\\s', text)\n",
    "    return len(sentences)\n",
    "\n",
    "# Example usage:\n",
    "essay_text = \"This is the first sentence. This is the second sentence!\"\n",
    "num_sentences = count_sentences(essay_text)\n",
    "print(\"Number of sentences:\", num_sentences)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "053921da",
   "metadata": {},
   "source": [
    "### (b) Spelling Mistakes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a10713c4",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "id": "372dc999",
   "metadata": {},
   "source": [
    "### c(i) Subject-Verb agreement"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6b0a3738",
   "metadata": {},
   "outputs": [],
   "source": [
   "# Load English language model\n",
   "nlp = spacy.load(\"en_core_web_sm\")\n",
   "\n",
   "def detect_subject_verb_agreement_errors(text):\n",
    "    errors = 0\n",
    "    # Process the text with SpaCy\n",
    "    doc = nlp(text)\n",
    "    for token in doc:\n",
    "        if token.pos_ == \"NOUN\" and token.dep_ == \"nsubj\":  # Check if token is a subject\n",
    "            head_verb = token.head\n",
    "            if head_verb.pos_ == \"VERB\":\n",
    "                # Check if the verb is in the 3rd person singular form\n",
    "                if head_verb.tag_ != \"VBZ\":  \n",
    "                    errors += 1\n",
    "    return errors\n",
    "\n",
    "# Example usage:\n",
    "essay_text = \"Jessica have 8 years old.\"\n",
    "num_sva_errors = detect_subject_verb_agreement_errors(essay_text)\n",
    "print(\"Number of subject-verb agreement errors:\", num_sva_errors)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "45c3bd34",
   "metadata": {},
   "source": [
    "### c(ii) Verb tense / missing verb / extra verb"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2261291a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}