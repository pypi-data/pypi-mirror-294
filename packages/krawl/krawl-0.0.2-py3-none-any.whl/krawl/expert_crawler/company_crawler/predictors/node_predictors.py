from krawl.common.config.globals import Files

from ..schema.dtypes import NodeCategory
from .base_clf import BasePredictor, MockPredictor


class PredictorFactory:

    title_predictor = BasePredictor(
        modelfile=Files.html_node_classifier,
        target=NodeCategory.TITLE)

    logo_predictor = BasePredictor(
        modelfile=Files.html_node_classifier,
        target=NodeCategory.LOGO)

    mock_title_predictor = MockPredictor(
        modelfile=Files.html_node_classifier,
        target=NodeCategory.TITLE)
