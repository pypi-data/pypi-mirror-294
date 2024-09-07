import os
import torch
import torchvision
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from mlplay.going_modular.helper_functions import set_seeds, plot_loss_curves
from mlplay.going_modular import engine

def load_pretrained_vit(num_classes, device):
    """Load and return a pretrained ViT model with a modified classification head."""
    pretrained_vit_weights = torchvision.models.ViT_B_16_Weights.DEFAULT
    model = torchvision.models.vit_b_16(weights=pretrained_vit_weights).to(device)

    # Freeze the base parameters
    for param in model.parameters():
        param.requires_grad = False

    # Change the classifier head
    set_seeds()
    model.heads = nn.Linear(in_features=768, out_features=num_classes).to(device)

    return model, pretrained_vit_weights.transforms()

def create_dataloaders(train_dir=None, test_dir=None, transform=None, batch_size=32):
    """Create and return DataLoader objects for training and testing datasets."""
    NUM_WORKERS = os.cpu_count()

    train_dataloader, test_dataloader = None, None

    if train_dir:
        train_data = datasets.ImageFolder(train_dir, transform=transform)
        if len(train_data) > 0:  # Ensure there are images in the train_data
            train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=NUM_WORKERS)
        else:
            raise ValueError(f"No images found in the training directory: {train_dir}")

    if test_dir:
        test_data = datasets.ImageFolder(test_dir, transform=transform)
        if len(test_data) > 0:  # Ensure there are images in the test_data
            test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=False, num_workers=NUM_WORKERS)
        else:
            raise ValueError(f"No images found in the testing directory: {test_dir}")

    return train_dataloader, test_dataloader

def train_model(train_dir, class_names, batch_size=32, lr=1e-3, epochs=10):
    """Train the ViT model and return the training accuracy."""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load the pretrained ViT model and transforms
    model, transforms = load_pretrained_vit(num_classes=len(class_names), device=device)

    # Create dataloaders
    train_dataloader, _ = create_dataloaders(train_dir=train_dir, transform=transforms, batch_size=batch_size)

    if train_dataloader is None:
        raise ValueError("train_dataloader is None. Please check the training directory and its contents.")

    # Setup optimizer and loss function
    optimizer = torch.optim.Adam(params=model.parameters(), lr=lr)
    loss_fn = torch.nn.CrossEntropyLoss()

    # Train the model
    set_seeds()
    results = engine.train(
        model=model,
        train_dataloader=train_dataloader,
        test_dataloader=None,  # No testing during training
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=epochs,
        device=device
    )

    # Optionally, plot loss curves
    plot_loss_curves(results)

    # Return the final training accuracy
    return results['train_acc'][-1]

def test_model(test_dir, class_names, model):
    """Test the ViT model on a test dataset and return the test accuracy."""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load the pretrained ViT model and transforms
    _, transforms = load_pretrained_vit(num_classes=len(class_names), device=device)

    # Create dataloaders
    _, test_dataloader = create_dataloaders(test_dir=test_dir, transform=transforms, batch_size=32)

    if test_dataloader is None:
        raise ValueError("test_dataloader is None. Please check the testing directory and its contents.")

    # Evaluate the model
    test_acc = engine.evaluate(model, test_dataloader, loss_fn=None, device=device)

    return test_acc

#nothing