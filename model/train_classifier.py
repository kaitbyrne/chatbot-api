import os
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


def train_skills():
    """
    Loads the training phrases and converts the data into a
    matrix of TF-IDF features
    A random forest classifier from sklearn is then trained
    Creates two pickle files containing the TF-IDF features
    and random forest classifier to load when classifying text
    into a skill
    """

    # Read the data
    train_data_dict = {}
    train_data = []
    train_labels = []

    phrases_path = "../training_phrases"
    for filename in os.listdir(phrases_path):
        if filename.endswith('.txt'):
            train_data_dict[filename] = []
            phrase_file = "{}/{}".format(phrases_path, filename)
            with open(phrase_file) as f:
                for line in f:
                    train_data_dict[filename].append(line.rstrip('\n'))

    for key, value in train_data_dict.iteritems():
        for i in range(len(value)):
            train_labels.append([key.rsplit(".", 1)[0]])

    for k, v in train_data_dict.iteritems():
        for i in v:
            train_data.append(i)

    # Create feature vectors
    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True)
    train_vectors = vectorizer.fit_transform(train_data)

    # Perform classification with SVM, kernel=linear
    classifier = RandomForestClassifier(n_estimators=10)
    classifier.fit(train_vectors, train_labels)

    classification_model_path = "classification_models"
    tfidf_rf_path = "{}/tfidf_rf_model.pkl".format(classification_model_path)
    rf_path = "{}/rf_model.pkl".format(classification_model_path)

    pickle.dump(vectorizer, open(tfidf_rf_path, 'wb'))
    pickle.dump(classifier, open(rf_path, 'wb'))


def find_skill(cmd):
    """
    Loads the pickle models and predicts the command from the models
    :param cmd: command input
    :return: skill found or 'no skill found' string
    """

    classification_model_path = "model/classification_models"
    tfidf_rf_path = "{}/tfidf_rf_model.pkl".format(classification_model_path)
    rf_path = "{}/rf_model.pkl".format(classification_model_path)

    vectorizer = pickle.load(open(tfidf_rf_path, 'rb'))
    classifier = pickle.load(open(rf_path, 'rb'))

    test_vectors = vectorizer.transform([cmd])
    prediction_linear = classifier.predict(test_vectors)

    get_predict_prob(classifier, cmd, prediction_linear, test_vectors)

    return prediction_linear[0]


def get_predict_prob(classifier, cmd, prediction_linear, test_vectors):
    """
    Stores the probability of the found skill into skill_probabilities.txt
    :param classifier: input classifier
    :param cmd: command input
    :param prediction_linear: skill found
    :param test_vectors: list of probabilities for each skill
    """
    results = classifier.predict_proba(test_vectors)[0]
    prob_per_class_dictionary = dict(zip(classifier.classes_, results))
    with open('model/skill_probabilities.txt', 'a') as f:
        found_skill = prob_per_class_dictionary.get(prediction_linear[0])
        line = ("Input Command: %s | Skill Found: %s | Confidence: %f\n" % (cmd, prediction_linear[0], found_skill))
        f.write(line)


def get_skill_list():

    skill_lst = []

    phrases_path = "training_phrases"
    for filename in os.listdir(phrases_path):
        if filename.endswith('.txt'):
            if not filename.endswith('answer.txt'):
                skill_lst.append(filename.rsplit(".", 1)[0])

    return skill_lst


if __name__ == '__main__':
    # os.chdir('../')

    train_skills()

    # skills_lst = get_skill_list()
    # print(skills_lst)

    # Test command with find_skill()
    # cmd = 'connect gitlab'
    # skill = find_skill(cmd.lower())
    # print("Found: " + skill)

