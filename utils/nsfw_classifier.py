from transformers import pipeline


class NSFWClassifier:
    """Class with only class methods"""

    # Class variable for the model pipeline
    classifier = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.classifier is None:
            cls.classifier = pipeline("sentiment-analysis",
                                      model="michellejieli/NSFW_text_classifier")


    @classmethod
    def get_classifier(cls):
        # load the emotion classifier if not loaded yet
        cls.load()

        # get the emotion classifier
        return cls.classifier
