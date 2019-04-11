
# read kaggle facial expression recognition challenge dataset (fer2013.csv)
# https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics
import pickle
import warnings
warnings.filterwarnings("ignore")

def sigmoid(x):
    return 1/(1+np.exp(-x))

def get_data():
    # angry, disgust, fear, happy, sad, surprise, neutral
    with open("fer2013.csv") as f:
        content = f.readlines()

    lines = np.array(content)
    num_of_instances = lines.size
    print("number of instances: ",num_of_instances)
    print("instance length: ",len(lines[1].split(",")[1].split(" ")))

    x_train, y_train, x_test, y_test = [], [], [], []

    for i in range(1,num_of_instances):
        emotion, img, usage = lines[i].split(",")
        pixels = np.array(img.split(" "), 'float32')
        emotion = 1 if int(emotion)==3 else 0 # Only for happiness
        if 'Training' in usage:
            y_train.append(emotion)
            x_train.append(pixels)
        elif 'PublicTest' in usage:
            y_test.append(emotion)
            x_test.append(pixels)

    #------------------------------
    #data transformation for train and test sets
    x_train = np.array(x_train, 'float64')
    y_train = np.array(y_train, 'float64')
    x_test = np.array(x_test, 'float64')
    y_test = np.array(y_test, 'float64')

    x_train /= 255 #normalize inputs between [0, 1]
    x_test /= 255

    x_train = x_train.reshape(x_train.shape[0], 48, 48)
    x_test = x_test.reshape(x_test.shape[0], 48, 48)
    y_train = y_train.reshape(y_train.shape[0], 1)
    y_test = y_test.reshape(y_test.shape[0], 1)
    
    x_val = x_train[20000:]
    x_train = x_train[0:20000]
    y_val = y_train[20000:]
    y_train = y_train[0:20000]

    print(x_train.shape[0], 'train samples')
    print(x_val.shape[0], 'validation samples')
    print(x_test.shape[0], 'test samples')

    # plt.hist(y_train, max(y_train)+1); plt.show()

    return x_train, y_train, x_val, y_val, x_test, y_test

class Model():
    def __init__(self):
        params = 48*48 # image reshape
        out = 1 # smile label
        self.lr = 0.00001 # Change if you want
        self.W = np.random.randn(params, out)
        self.b = np.random.randn(out)

    def forward(self, image):
        image = image.reshape(image.shape[0], -1)
        out = np.dot(image, self.W) + self.b
        return out

    def compute_loss(self, pred, gt):
        J = (-1/pred.shape[0]) * np.sum(np.multiply(gt, np.log(sigmoid(pred))) + np.multiply((1-gt), np.log(1 - sigmoid(pred))))
        return J

    def compute_gradient(self, image, pred, gt):
        image = image.reshape(image.shape[0], -1)
        W_grad = np.dot(image.T, pred-gt)/image.shape[0]
        self.W -= W_grad*self.lr

        b_grad = np.sum(pred-gt)/image.shape[0]
        self.b -= b_grad*self.lr

def train(model):
    x_train, y_train, x_val, y_val, x_test, y_test = get_data()
    batch_size = 100 # Change if you want
    epochs = 40000 # Change if you want
    loss_Train = []
    loss_Test = []    
    epoch = []
    
    for i in range(epochs):
        loss = []
        for j in range(0,x_train.shape[0], batch_size):
            _x_train = x_train[j:j+batch_size]
            _y_train = y_train[j:j+batch_size]
            out = model.forward(_x_train)
            loss.append(model.compute_loss(out, _y_train))
            model.compute_gradient(_x_train, out, _y_train)
            
        out = model.forward(x_test)                
        loss_test = model.compute_loss(out, y_test)
        
        epoch.append(i)
        loss_Train.append(np.array(loss).mean())
        loss_Test.append(np.array(loss_test).mean())
        
        print('Epoch {:6d}: {:.5f} | test: {:.5f}'.format(i, np.array(loss).mean(), loss_test))
	#return epoch, loss_Train, loss_Test
    model_par = {'W':model.W,'b':model.b}
    with open('40kModel.pickle','wb') as f:
        pickle.dump(model_par,f)
 
    # plot()
    plot(epoch,loss_Train, loss_Test)
	

def plot(epoch,loss_Train, loss_Test): # Add arguments
    # CODE HERE
    # Save a pdf figure with train and test losses
    
    figu = plt.figure()
    plt.plot(epoch, loss_Train, label='Train')
    plt.plot(epoch, loss_Test, label='Test')
    plt.legend()
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
     
    figu.savefig('Loss.jpg')
    figu.savefig('Loss.pdf')
    
    pass

def test(model):
    _, _, _, _, x_test, y_test = get_data()
    # YOU CODE HERE
    # Show some qualitative results and the total accuracy for the whole test set
    

    thres = 0.5
    labels = model.forward(x_test)
    labels = sigmoid(labels)
    labels[labels >= thres] = 1
    labels[labels < thres] = 0
    
    #tn, fp, fn, tp = sklearn.metrics.confusion_matrix(y_test,labels).ravel();
    #aca = (tp/(tp+fn))+(tn/(fp+tn))
    #aca = aca/2


    conf = sklearn.metrics.confusion_matrix(y_test, labels)
    aca=sklearn.metrics.accuracy_score(y_test,labels)
    print(aca)
    print(conf)
    #pass

if __name__ == '__main__':
    model = Model()
    train(model)
    test(model)

