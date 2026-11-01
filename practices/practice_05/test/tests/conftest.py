import os
import sys

# Обеспечиваем, что корень проекта в sys.path для импорта пакета 'app'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
