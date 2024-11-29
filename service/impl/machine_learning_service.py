from fastapi import  UploadFile
from database.schema import MachineLearningResponse
from service.meta import MachinelearningMeta
from PIL import Image
import tensorflow as tf
import numpy as np
import io
import cv2


class MachineLearningService(MachinelearningMeta):
    def machine_learning_process(self, content):
        
        # Mengonversi konten gambar menjadi array numpy menggunakan np.frombuffer
        nparr = np.frombuffer(content, np.uint8)

        # Membaca gambar dari array menggunakan OpenCV
        img_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Resize gambar sesuai dengan dimensi yang diinginkan (misalnya 256x256)
        img_resized = cv2.resize(img_cv2, (256, 256))

        hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)
        lower_green = np.array([35, 40, 40])  # Rentang hijau daun
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        green_percentage = (np.sum(mask) / (mask.size * 255)) * 100

          # Jika > 30% dari gambar adalah hijau, mungkin dau

        if green_percentage > 19:
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
