from transformers import pipeline


class EmotionClassifier:
    """Class with only class methods"""

    # Class variable for the model pipeline
    classifier = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.classifier is None:
            cls.classifier = pipeline("text-classification",
                                      model="j-hartmann/emotion-english-distilroberta-base",
                                      return_all_scores=True)


    @classmethod
    def get_classifier(cls):
        # load the emotion classifier if not loaded yet
        cls.load()

        # get the emotion classifier
        return cls.classifier
