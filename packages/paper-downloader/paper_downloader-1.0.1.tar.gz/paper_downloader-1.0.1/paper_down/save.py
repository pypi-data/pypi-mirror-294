import os
from paper_down.config.config_loader import config


def fetch_paper_types():
  root = config.save_root
  return [(os.path.join(root, name), name) for name in os.listdir(root) if os.path.isdir(os.path.join(root, name))]
