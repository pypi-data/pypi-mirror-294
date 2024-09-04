# PyOcclusion
![PyPI](https://img.shields.io/pypi/v/PyOcclusion)
![License](https://img.shields.io/github/license/BohdanSynytskyi/PyOcclusion)

PyOcclusion is a Python package for adding noise of occlusionary type to video files. There is a broad range of parameters for altering in order to achieve the desirded occlusion density, coverage percent, etc. The process is automated and requires no additional prescribing.

Here is an example of what can be done with PyOcclusion:

![Description of the image](grid_image.png)

# Installation

PyOcclusion can be installed from PyPI:

```pip install PyOcclusion```

Once installed, package can be loaded as:

```import PyOcclusion```

# Example

``` 
import PyOcclusion

editor = PyOcclusion.VideoEditor(20, 0, 17, 17, 500, height=1080, width=1920)

editor.edit('video.mp4', "newVideo.mp4")
```

