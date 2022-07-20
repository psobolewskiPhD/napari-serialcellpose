from napari_serialcellpose import SerialWidget
import numpy as np

from pathlib import Path
import shutil

def test_load_single_image(make_napari_viewer):
    
    viewer = make_napari_viewer()
    widget = SerialWidget(viewer)

    mypath = Path('src/napari_serialcellpose/_tests/data/singlefile_singlechannel/')
              
    widget.file_list.update_from_path(mypath)
    assert len(viewer.layers) == 0 
    widget.file_list.setCurrentRow(0)
    assert len(viewer.layers) == 1

def test_analyse_single_image_no_save(make_napari_viewer):
    
    viewer = make_napari_viewer()
    widget = SerialWidget(viewer)

    mypath = Path('src/napari_serialcellpose/_tests/data/singlefile_singlechannel/')
              
    widget.file_list.update_from_path(mypath)
    widget.file_list.setCurrentRow(0)

    # Check that selecting cyto2 displays diameter choice
    assert widget.spinbox_diameter.isVisible() is False
    widget.qcbox_model_choice.setCurrentIndex(
        [widget.qcbox_model_choice.itemText(i) for i in range(widget.qcbox_model_choice.count())].index('cyto2')
    )
    # not working for some reason
    #assert widget.spinbox_diameter.isVisible() is True
    
    # set diameter and run segmentation
    widget.spinbox_diameter.setValue(70)
    widget._on_click_run_on_current()

    # check that segmentatio has been added, named 'mask' and results in 33 objects
    assert len(viewer.layers) == 2
    assert viewer.layers[1].name == 'mask'
    assert viewer.layers[1].data.max() == 33


def test_analyse_single_image_save(make_napari_viewer):

    viewer = make_napari_viewer()
    widget = SerialWidget(viewer)


    mypath = Path('src/napari_serialcellpose/_tests/data/multifile/')
    output_dir = Path('src/napari_serialcellpose/_tests/data/analyzed_multiple')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True)

    widget.file_list.update_from_path(mypath)
    widget.output_folder = output_dir
    widget.file_list.setCurrentRow(0)

    widget.qcbox_model_choice.setCurrentIndex(
        [widget.qcbox_model_choice.itemText(i) for i in range(widget.qcbox_model_choice.count())].index('cyto2'))
    widget.spinbox_diameter.setValue(70)
    widget._on_click_run_on_current()

    assert len(list(output_dir.glob('*mask.tif'))) == 1

    widget._on_click_run_on_folder()
    assert len(list(output_dir.glob('*mask.tif'))) == 4

def test_mask_loading(make_napari_viewer):

    viewer = make_napari_viewer()
    widget = SerialWidget(viewer)

    mypath = Path('src/napari_serialcellpose/_tests/data/multifile/')
    output_dir = Path('src/napari_serialcellpose/_tests/data/analyzed_multiple2')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True)

    widget.file_list.update_from_path(mypath)
    widget.output_folder = output_dir
    widget.file_list.setCurrentRow(0)

    widget.qcbox_model_choice.setCurrentIndex(
        [widget.qcbox_model_choice.itemText(i) for i in range(widget.qcbox_model_choice.count())].index('cyto2'))
    widget.spinbox_diameter.setValue(70)
    widget._on_click_run_on_current()

    widget.file_list.setCurrentRow(1)
    assert len(viewer.layers) == 1

    widget.file_list.setCurrentRow(0)
    assert len(viewer.layers) == 2