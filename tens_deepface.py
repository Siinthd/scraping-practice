from deepface import DeepFace
import json

def face_verify(img1,img2):
    try:
        result = DeepFace.verify(img1_path=img1,img2_path=img2)
        if result.get('verified'):
            print("ok")
        with open('data_capture/result.json','w') as file:
            json.dump(result,file,indent=4,ensure_ascii=False)
    except Exception as ex:
        return ex

def face_analyze(img):
    try:
        result = DeepFace.analyze(img_path=img,actions=['age','gender','race','emotion'])
        print(result)
        with open('data_capture/analyze.json','w') as file:
            json.dump(result,file,indent=4,ensure_ascii=False)
    except Exception as ex:
        print( ex)

face_analyze('images/face1.jpg')
