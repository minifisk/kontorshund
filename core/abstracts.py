import logging

def prevent_request_warnings(original_function):
    """
    If we need to test for 404s or 405s this decorator can prevent the
    request class from throwing warnings.
    """
    def new_function(*args, **kwargs):
        # raise logging level to ERROR
        logger = logging.getLogger('django.request')
        #previous_logging_level = logger.getEffectiveLevel()
        logging.disable(logging.CRITICAL)


        # trigger original function that would throw warning
        original_function(*args, **kwargs)

        # lower logging level back to previous
        logging.disable(logging.NOTSET)

    return new_function