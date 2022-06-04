
class Classifier:
    def classify(message, logger):
        if message.type == 'text':
            logger.debug('this is a text message')
            return [1]
        else:
            logger.debug('this is not a text message')
            return [0]
