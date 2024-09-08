import pytest
import os
from paper_down.downloader import download_and_merge_pdfs
from paper_down.config.config_loader import config

test_url1 = "https://openaccess.thecvf.com/content/CVPR2024/papers/Gao_GraphDreamer_Compositional_3D_Scene_Synthesis_from_Scene_Graphs_CVPR_2024_paper.pdf"
test_url2 = "https://openaccess.thecvf.com/content/CVPR2024/supplemental/Gao_GraphDreamer_Compositional_3D_CVPR_2024_supplemental.pdf"
test_not_pdf_url = "https://arxiv.org/src/2312.00093"

def test_single_pdf_download():
    result = download_and_merge_pdfs(test_url1)
    assert result == config.temp_filename
    os.remove(config.temp_filename)

def test_invalid_url_raises_exception():
    with pytest.raises(ValueError):
        download_and_merge_pdfs(test_not_pdf_url)

def test_merge_two_pdfs():
    result = download_and_merge_pdfs(test_url1, test_url2)
    assert result == config.temp_filename
    os.remove(config.temp_filename)
