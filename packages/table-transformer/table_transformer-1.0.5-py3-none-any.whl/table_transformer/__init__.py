import sys
from .src.inference import TableExtractionPipeline
from .src.inference import get_structure_class_thresholds, get_detection_class_thresholds
from .src.utils import get_cell_coordinates_by_row, apply_ocr

# encoding utf-8
sys.stdout.encoding = 'utf-8'


