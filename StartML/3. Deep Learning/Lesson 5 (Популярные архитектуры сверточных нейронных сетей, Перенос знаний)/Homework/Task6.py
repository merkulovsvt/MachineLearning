import torch.nn as nn
from torchvision.models import alexnet, vgg11, googlenet, resnet18


def get_pretrained_model(model_name: str, num_classes: int, pretrained: bool = True):
    if model_name == 'alexnet':
        model = alexnet(pretrained=pretrained)
        model.classifier[6] = nn.Linear(in_features=4096, out_features=num_classes)

    elif model_name == 'vgg11':
        model = vgg11(pretrained=pretrained)
        model.classifier[6] = nn.Linear(in_features=4096, out_features=num_classes)

    elif model_name == 'googlenet':
        model = googlenet(pretrained=pretrained)

        model.fc = nn.Linear(in_features=1024, out_features=num_classes)
        model.aux1.fc2 = nn.Linear(1024, num_classes)
        model.aux2.fc2 = nn.Linear(1024, num_classes)

    elif model_name == 'resnet18':
        model = resnet18(pretrained=pretrained)
        model.fc = nn.Linear(in_features=512, out_features=num_classes)

    else:
        return None

    return model
