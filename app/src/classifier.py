
class Classifier:
    def classify(logger, message):
        if message.type == 'text':
            logger.debug('this is a text message')
            return [1]
        else:
            logger.debug('this is not a text message')
            return [0]
