# Welltech Media Tagging

## Prerequisites

* Google Cloud project with billing enabled.
* [Video Intelligence API](https://console.cloud.google.com/apis/library/videointelligence.googleapis.com) and [Vision API](https://console.cloud.google.com/apis/library/vision.googleapis.com) enabled.
* Python3.8+
* Access to repository configured. In order to clone this repository you need
	to do the following:
	*   Visit https://professional-services.googlesource.com/new-password and
			login with your account.
    * Once authenticated please copy all lines in box
        and paste them in the terminal.


## Run


1. Install `media-tagger`

```
pip install media-tagging
```

2. Perform tagging

```
media-tagger --media-path MEDIA_PATH --tagger TAGGER_TYPE --writer WRITER_TYPE
```
where:
* MEDIA_PATH - comma-separated names of files for tagging (can be urls).
* TAGGER_TYPE - name of tagger, supported options:
  * `vision-api` - tags images based on [Google Cloud Vision API](https://cloud.google.com/vision/),
  * `video-api` for videos based on [Google Cloud Video Intelligence API](https://cloud.google.com/video-intelligence/)
  * `gemini-image` - Uses Gemini to tags images. Add `--tagger.n_tags=<N_TAGS>`
     parameter to control number of tags returned by tagger.
  * `gemini-structured-image`  - Uses Gemini to find certain tags in the images.
    Add `--tagger.tags='tag1, tag2, ..., tagN` parameter to find certain tags
    in the image.
  * `gemini-description-image` - Provides brief description of the image,
* WRITER_TYPE - name of writer, one of `csv`, `json`

By default script will create a single file with tagging results for each media_path.
If you want to combine results into a single file add `--output OUTPUT_NAME` flag (without extension, i.e. `--output tagging_sample`.


## Disclaimer
This is not an officially supported Google product.
