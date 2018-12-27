import logging
import traceback

from app.crawlers.assessment import fill_assessment, get_assessments

from .models import Log


logger = logging.getLogger(__name__)


def get_assessment(cookies, class_no):
    assessments = list(filter(
        lambda x: x['class_no'] == class_no,
        get_assessments(cookies)
    ))

    if not assessments:
        return None

    return assessments[0]


def fill(cookies, assessment, score, suggestions):
    try:
        fill_assessment(cookies, assessment['params'], score, suggestions)
    except Exception:
        error_message = traceback.format_exc()
        Log.objects.create(error_message=error_message)
        logger.error(error_message)
        return False

    return True


def fill_all(cookies, assessments, score, suggestions):
    for assessment in assessments:
        if assessment['params'] is None:
            continue

        result = fill(cookies, assessment, score, suggestions)
        if not result:
            return False

    return True
