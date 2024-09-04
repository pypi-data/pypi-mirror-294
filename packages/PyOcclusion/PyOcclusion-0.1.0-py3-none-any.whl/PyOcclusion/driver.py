import occlusion

# editor = occlusion.VideoEditor(20, 0, 17, 17, 500, height=1080, width=1920)
# editor.showOcclusion("/Users/bohdansynytskyi/Computer-Vision-v2-master/lesson_1/data/picture.jpg")

# editor.edit('/Users/bohdansynytskyi/research/Actor_01/output.mp4', "/Users/bohdansynytskyi/desktop/noisyName.mp4")

editor = occlusion.VideoEditor(20, 0, 17, 17, 500, height=1080, width=192)
editor.showOcclusion("/Users/bohdansynytskyi/Computer-Vision-v2-master/lesson_1/data/picture.jpg")