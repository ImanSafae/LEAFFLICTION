import argparse
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

def load_class_names(model_dir):
    class_names_path = os.path.join(model_dir, 'class_names.txt')
    if not os.path.exists(class_names_path):
        raise FileNotFoundError(f"Class names file not found: {class_names_path}")
    
    with open(class_names_path, 'r') as f:
        class_names = [line.strip() for line in f.readlines()]
    return class_names

def predict_image(image_path, model_path, class_names, img_height=224, img_width=224, show_plot=True):
    model = keras.models.load_model(model_path)
    
    img = image.load_img(image_path, target_size=(img_height, img_width))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array, verbose=0)
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx]
    
    predicted_class = class_names[predicted_class_idx]
    
    print(f"\n{'='*50}")
    print(f"Image: {image_path}")
    print(f"Predicted disease: {predicted_class}")
    print(f"Confidence: {confidence*100:.2f}%")
    print(f"{'='*50}\n")
    
    print("All class probabilities:")
    sorted_indices = np.argsort(predictions[0])[::-1]
    for idx in sorted_indices:
        print(f"  {class_names[idx]}: {predictions[0][idx]*100:.2f}%")
    
    if show_plot:
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        img_display = image.load_img(image_path)
        plt.imshow(img_display)
        plt.title(f"Predicted: {predicted_class}\nConfidence: {confidence*100:.1f}%")
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        y_pos = np.arange(len(class_names))
        plt.barh(y_pos, predictions[0] * 100)
        plt.yticks(y_pos, class_names)
        plt.xlabel('Confidence (%)')
        plt.title('Prediction Probabilities')
        plt.xlim(0, 100)
        
        for i, v in enumerate(predictions[0] * 100):
            plt.text(v + 1, i, f'{v:.1f}%', va='center')
        
        plt.tight_layout()
        plt.show()
    
    return predicted_class, confidence, predictions[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='predict.py',
        description='Predict plant disease from an image using trained model'
    )
    parser.add_argument(
        'image',
        help='Path to the image file to classify'
    )
    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='Disable visualization plot'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        exit(1)
    
    model_path = './model/best_model.keras'
    if not os.path.exists(model_path):
        print(f"Error: Model file not found: {model_path}")
        exit(1)
    
    class_names = load_class_names('./model')
    
    predict_image(
        args.image,
        model_path,
        class_names,
        show_plot=not args.no_plot
    )
