# sheatless - A python library for extracting parts from sheetmusic pdfs

Sheatless, a tool for The Beatless to become sheetless. Written and managed by the web-committee in the student orchestra The Beatless. Soon to be integrated in [taktlaus.no](https://taktlaus.no/).

# Requirements

Sheatless requires tesseract and poppler installed on the system to work,

```shell
sudo apt install tesseract poppler
```

and it is recommended to use the following tessdata: [https://github.com/tesseract-ocr/tessdata_best/archive/refs/tags/4.1.0.zip](https://github.com/tesseract-ocr/tessdata_best/archive/refs/tags/4.1.0.zip). These requirements are already set up properly in the docker image described by [`Dockerfile`](Dockerfile).

# API

## PdfPredictor

```py
class PdfPredictor():
    def __init__(
        self,
        pdf : BytesIO | bytes,
        instruments=None,
        instruments_file=None,
        instruments_file_format="yaml",
        use_lstm=False,
        tessdata_dir=None,
        tesseract_languages=["eng"],
        log_stream=sys.stdout,
        crop_to_top=False,
        crop_to_left=True,
        full_score_threshold=3,
        full_score_label="Full score",
        ):
        ...
    
    def parts(self):
        for ...:
            yield  {
                "name": "<part name>",
                "partNumber": "<part number>",
                "instruments": ["<instrument name", ...],
                "fromPage": "<from page>",
                "toPage": "<to page>",
            }
```

### Arguments for `__init__`:
- `pdf`                                - PDF file object
- `instruments`             (optional) - Dictionary of instruments. Will override any provided instruments file.
- `instruments_file`        (optional) - Full path to instruments file or instruments file object. Accepted extensions: .yaml, .yml, .json
- `instruments_file_format` (optional) - Format of instruments_file if it is a file object. Accepted formats: yaml, json
  - If neither instruments_file nor instruments is provided a default instruments file will be used.
- `use_lstm`                (optional) - Use LSTM instead of legacy engine mode.
- `tessdata_dir`            (optional) - Full path to tessdata directory. If not provided, whatever the environment variable TESSDATA_DIR will be used.
- `tesseract_languages`     (optional) - List of which languages tesseract should use.
- `log_stream`              (optional) - File stream log output will be sent to. Can be set to `None` to disable logging.
- `crop_to_top`             (optional) - If set to `True` (not default), PDF pages will be cropped to top half.
- `crop_to_left`            (optional) - If set to `True` (default), PDF pages will be cropped to left half.
- `full_score_threshold`    (optional) - If the number of parts predicted in one pages is greater than this number, `full_score_label` will be considered as the predicted part instead.
- `full_score_label`        (optional) - The label to use for identifying a full score.

## processUploadedPdf

```python
def processUploadedPdf(pdfPath, imagesDirPath, instruments_file=None, instruments=None, use_lstm=False, tessdata_dir=None):
    ...
    return parts, instrumentsDefaultParts
```

which will be available with

```python
from sheatless import processUploadedPdf
```

Arguments description here:

| Argument         | Optional   | Description                                                                                                      |
| ---------------- | ---------- | ---------------------------------------------------------------------------------------------------------------- |
| pdfPath          |            | Full path to PDF file.                                                                                           |
| imagesDirPath    |            | Full path to output images.                                                                                      |
| instruments_file | (optional) | Full path to instruments file. Accepted formats: YAML (.yaml, .yml), JSON (.json).                               |
| instruments      | (optional) | Dictionary of instruments. Will override any provided instruments file.                                          |
|                  |            | If neither instruments_file nor instruments is provided a default instruments file will be used.                 |
| use_lstm         | (optional) | Use LSTM instead of legacy engine mode.                                                                          |
| tessdata_dir     | (optional) | Full path to tessdata directory. If not provided, whatever the environment variable `TESSDATA_DIR` will be used. |

Returns description here:

| Return                  | Description                                                                                                                                     |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| parts                   | A list of dictionaries `{ "name": "name", "instruments": ["instrument 1", "instrument 2"...] "fromPage": i, "toPage": j }` describing each part |
| instrumentsDefaultParts | A dictionary `{ ..., "instrument_i": j, ... }`, where `j` is the index in the parts list for the default part for `instrument_i`.               |

## predict_parts_in_pdf

```py
def predict_parts_in_pdf(
    pdf : BytesIO | bytes,
    instruments=None,
    instruments_file=None,
    instruments_file_format="yaml",
    use_lstm=False,
    tessdata_dir=None,
    ):
    ...
    return parts, instrumentsDefaultParts
```

### Arguments:
- pdf                                - PDF file object
- instruments             (optional) - Dictionary of instruments. Will override any provided instruments file.
- instruments_file        (optional) - Full path to instruments file or instruments file object. Accepted extensions: .yaml, .yml, .json
- instruments_file_format (optional) - Format of instruments_file if it is a file object. Accepted formats: yaml, json
  - If neither instruments_file nor instruments is provided a default instruments file will be used.
- use_lstm                (optional) - Use LSTM instead of legacy engine mode.
- tessdata_dir            (optional) - Full path to tessdata directory. If not provided, whatever the environment variable TESSDATA_DIR will be used.

### Returns:
- parts                              - A list of dictionaries `{ "name": "name", "instruments": ["instrument 1", "instrument 2"...] "fromPage": i, "toPage": j }` describing each part
- instrumentsDefaultParts            - A dictionary `{ ..., "instrument_i": j, ... }`, where j is the index in the parts list for the default part for instrument_i.

## predict_parts_in_img

```py
def predict_parts_in_img(img : io.BytesIO | bytes | PIL.Image.Image, instruments, use_lstm=False, tessdata_dir=None) -> typing.Tuple[list, list]:
    ...
    return partNames, instrumentses
```

### Arguments:
- img                     - image object
- instruments             - dictionary of instruments
- use_lstm     (optional) - Use LSTM instead of legacy engine mode.
- tessdata_dir (optional) - Full path to tessdata directory. If not provided, whatever the environment variable TESSDATA_DIR will be used.

### Returns:
- partNames               - a list of part names
- instrumentses           - a list of lists of instruments for each part

# Development

## Build docker container

```
docker-compose build
```

## Enter docker container

```
docker-compose run develop
```

## Usage

The entry point is `main.py`, which uses argparse to generate a flexible CLI. The full synopsis for this interface is

```
python main.py [-h] [--clear-output] [--engine ENGINE] [--tessdata-dir TESSDATA_DIR] operation {img,pdf} [input] [pages ...]
```

where the second positional argument is `input_type`. `input` is relative path from `input_pdfs` or `input_images` to the file or directory you want to analyze. `input` can be skipped, then the script will take all the files it finds. If `input` is a directory, the script will take all files recursively in that directory. If `input_type` is `pdf`, you can also specify which pages you want to analyze. If no pages are provided all pages will be analyzed. `operation` is the name of the python function you want to perform on each pdf page or image. That function should have the following interface:

```py
import io
def operation(img: io.BytesIO, engine_kwargs: dict):
    ...
    return ["identifier_1", io.BytesIO(output_img_1)], ...
```

As we can see the function must accept one input image and a dictionary of engine kwargs, and can return any number of output images. Image format is same as input image when `input_type=img`, and png when `input_type=pdf`. All output images will then be stored in `output_images/`. The operation function must also accept arguments from argparse as keywordarguments.

You can get a more detailed description of the arguments by running the help command

```
python main.py -h
```

There is also a way to clear the output directories:

```
python main.py --clear-output
```

## Example usage

Given you have a function called `blur` like this:

```py
import io
from PIL import Image
import numpy as np

def blur(img, engine_kwargs):
    pixel_array = np.asarray(Image.open(img))
    np.blur(pixel_array) # Not sure if blur is a numpy function though...
    ret = io.BytesIO()
    Image.fromarrray(pixel_array).save(ret, format="png")
    return ["blurred", ret]
```

and the following file structure:

```
+- input_pdfs
|  +- a.pdf
|  +- b.pdf
|  +- c
|  |  +- e.pdf
|  |  +- f.pdf
+- input_images
|  +- g.png
|  +- h.png
```

, here is some commands you might want to run:

Execute `blur` on all pages in `a.pdf`:

```
python main.py blur pdf a.pdf
```

Execute `blur` on all pages in all pdfs:

```
python main.py blur pdf
```

Execute `blur` on all pages in all pdfs the `c` directory:

```
python main.py blur pdf c
```

Execute `blur` on page 2 and 3 in `a.pdf`:

```
python main.py blur pdf a.pdf 2 3
```
Execute `blur` on all pdfs, but clear old output data first:

```
python main.py --clear-output blur pdf
```

Execute `blur` on all images:

```
python main.py blur img
```

The format for specifying an image file or directory is the same as for pdfs. The `--clear-output` flag of course works for images as well.

It is not possible to operate on images in the `input_pdfs` folder or pdfs in the `input_images` folder.

# Sheatless build and deployment

## Build sheatless package

```
docker-compose run build_package
```

## Deploy shealess package

This requires you to configure an API token in your `~/.pypirc`. To do that log in as thebeatless [here](https://pypi.org/manage/account/) and add a token for sheatless and add it to `~/.pypirc`.

It also requires you to install twine, and I do not encourage doing this in docker as I think it will be a mess, and not really that useful.

```
pip install --upgrade twine
```

And then the actual deployment command is

```
python3 -m twine upload sheatless_full_repo/dist/*
```
