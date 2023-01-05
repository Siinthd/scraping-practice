from pixellib.instance import instance_segmentation
#pixellib == 0.7.1
#tensorflow ==2.2.0
#python == 3.7.9

def find_obj_on_image():
    #https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5
    segment = instance_segmentation()
    segment.load_model("data/mask_rcnn_coco.h5")
    target_class = segment.select_target_classes(car=True)
    result = segment.segmentImage(
                            image_path = "images/city.jpg",
                            show_bboxes = True,
                            segment_target_classes=target_class,
                            output_image_name = "images/output.jpg"
                        )
    print(result)
find_obj_on_image()
