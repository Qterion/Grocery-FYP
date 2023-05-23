train_iter, test_iter= mu.load_data_fungus_mnist(batch_size)

class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.block1=nn.Sequential(
            nn.Conv2d(in_channels=1,out_channels=16,kernel_size=3,padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2,stride=2)
        )
        self.block2=nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc1=nn.Linear(in_features=32*6*6,out_features=1)
    
    def forward(self, x):
        out=self.block1(x)
        out=self.block2(out)
        out=out.view(out.size(0),-1)
        out=self.fc1(out)
        return out

net=Net()
loss=nn.MSELoss()
optimizer=torch.optim.SGD(net.parameters(),lr=0.01)

epochs=5
net.train()
for e in range(epochs):
    for images,labels, in train_iter:
        predictions=net(images) #predictions.shape [batch_size,1],
        labels=labels.unsqueeze(1).float() #changes labels.shape from [batch_size] to [batch_size, 1] to match dimensions of predictions
        l=loss(predictions,labels)
        l.backward()
        optimizer.step()


