import torch
import torch.nn as nn
from torchvision import models, transforms
from torchvision.datasets import ImageFolder
from PIL import Image
import io
from collections import Counter

device = torch.device("cpu")

# Define transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Class names
dataroot = "dataset"
dataset = ImageFolder(root=dataroot)
class_names = dataset.classes 


# Load EfficientNet
efficientnet = models.efficientnet_b0(weights=None)
efficientnet.classifier[1] = nn.Linear(efficientnet.classifier[1].in_features, len(class_names))
efficientnet.load_state_dict(torch.load("model_pth/efficientnet.pth", map_location=device, weights_only=True))
efficientnet.to(device)
efficientnet.eval()

# Load ResNet
resnet = models.resnet18(weights=None)
resnet.fc = nn.Linear(resnet.fc.in_features, len(class_names))
resnet.load_state_dict(torch.load("model_pth/resnet.pth", map_location=device, weights_only=True))
resnet.to(device)
resnet.eval()

# Load DenseNet
densenet = models.densenet121(weights=None)
densenet.classifier = nn.Linear(densenet.classifier.in_features, len(class_names))
densenet.load_state_dict(torch.load("model_pth/densenet.pth", map_location=device, weights_only=True))
densenet.to(device)
densenet.eval()

# Model Dictionary
models_dict = {
    "efficientnet": efficientnet,
    "resnet": resnet,
    "densenet": densenet
}

# Load and preprocess image
def load_image(file):
    image = Image.open(io.BytesIO(file.read())).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)
    return image.to(device)

# Get prediction from a model
def get_prediction(model_name, image):
    model = models_dict[model_name]
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
        return predicted.item(), confidence.item()

# Majority voting
def majority_vote(predictions):
    counter = Counter(predictions)
    return counter.most_common(1)[0][0]
