from fastapi import  UploadFile
from database.schema import MachineLearningResponse
from service.meta import MachinelearningMeta
from ultralyticsplus import YOLO
from PIL import Image
import tensorflow as tf
import numpy as np
import io
import cv2


class MachineLearningService(MachinelearningMeta):
    def check_dauntomat(self, image) -> bool:
        model = YOLO('foduucom/plant-leaf-detection-and-classification')

        # Set model parameters
        model.overrides['conf'] = 0.25
        model.overrides['iou'] = 0.45
        model.overrides['agnostic_nms'] = False
        model.overrides['max_det'] = 1000

        # Perform inference
        results = model.predict(image)

        # Get class indices and convert to labels
        class_indices = results[0].boxes.cls.cpu().numpy()  # Indeks kelas (tensor -> numpy)
        labels = [model.names[int(idx)] for idx in class_indices]  


        for label in labels:
            if "tomato" in label:
                print(f"Label: {label} - daun tomat")
                return True
            else:
                print(f"Label: {label} - bukan daun tomat")
        return False

    def machine_learning_process(self, content):
        
        # Mengonversi konten gambar menjadi array numpy menggunakan np.frombuffer
        nparr = np.frombuffer(content, np.uint8)

        # Membaca gambar dari array menggunakan OpenCV
        img_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Resize gambar sesuai dengan dimensi yang diinginkan (misalnya 256x256)
        img_resized = cv2.resize(img_cv2, (256, 256))

        check = self.check_dauntomat(img_resized)

 

        if check :
            interpreter = tf.lite.Interpreter(model_path="converted_model.tflite")
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            #cek
            # Convert image to array and normalize
            img_array = np.array(img_resized) / 255.0
            img_array = img_array.astype(np.float32)  # Convert to float32
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
           # Run inference
            interpreter.set_tensor(input_details[0]['index'], img_array)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])[0]
            predicted_index = int(np.argmax(output_data))
            classes = ["Bacterial Spot", "Early Blight", "Late Blight", "Leaf Mold","Septoria Leaf Spot","Spidermites-Two-spottedspider_mite","Target Spot","TomatoYellowLeafCurlVirus", "Tomatomosaicvirus","Healthy"]
            predicted_class = classes[predicted_index]
            confidence_percentage = float(output_data[predicted_index] * 100)
            predicted_index +=1
 
        else:
            return {"predicted_class": "bukan daun tomat","percentage":0, "predicted_index":0} 
        return {"predicted_class": predicted_class, "percentage":confidence_percentage, "predicted_index":predicted_index}

   