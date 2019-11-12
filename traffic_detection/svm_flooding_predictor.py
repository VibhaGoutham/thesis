from __future__ import division
import time
import threading
import requests
import cvxopt
import cvxopt.solvers
import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing, cross_validation, neighbors
from sklearn.preprocessing import MinMaxScaler
#from sklearn.metrics import precision_score
#from sklearn.metrics import accuracy_score

rx_packets = 0
rx_bytes = 0
t_observation = 5.0

#/stats/port/<dpid>[/<port>]
PortStatsURL = "http://10.20.5.39:8080/stats/port/1/1"

#---------------------------------------------------------------------#
#Support Vector Machine Engine
global_w = np.array([])
global_a = np.array([])
global_sv = np.array([])
global_sv_y = np.array([])
global_b = 0.0

def linear_kernel(x1, x2):
    return np.dot(x1, x2)

class SVM(threading.Thread):
    global global_w, global_a, global_sv, global_sv_y, global_b, global_L, global_m
    def __init__(self, kernel=linear_kernel, C=None):
        self.kernel = kernel
        self.C = C
        if self.C is not None: self.C = float(self.C)
        threading.Thread.__init__(self)
        #print self.C

    def run(self):
        X1, y1, X2, y2 = self.gen_lin_separable_overlap_data()
        X, y = self.split_train(X1, y1, X2, y2)
        print("X_train/X is", X)
        global_L, global_m = self.split_test(X1, y1, X2, y2)
        print("X_test/L is", global_L)

        n_samples, n_features = X.shape

        # Gram matrix
        K = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            for j in range(n_samples):
                K[i,j] = self.kernel(X[i], X[j])

        P = cvxopt.matrix(np.outer(y,y) * K)
        q = cvxopt.matrix(np.ones(n_samples) * -1)
        A = cvxopt.matrix(y, (1,n_samples))
        b = cvxopt.matrix(0.0)

        if self.C is None:
            G = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))
            h = cvxopt.matrix(np.zeros(n_samples))
        else:
            tmp1 = np.diag(np.ones(n_samples) * -1)
            #print "tmp1 is", tmp1
            tmp2 = np.identity(n_samples)
            #print "tmp2 is", tmp2
            G = cvxopt.matrix(np.vstack((tmp1, tmp2)))
            tmp1 = np.zeros(n_samples)
            tmp2 = np.ones(n_samples) * self.C
            h = cvxopt.matrix(np.hstack((tmp1, tmp2)))

        # solve QP problem
        solution = cvxopt.solvers.qp(P, q, G, h, A, b)

        # Lagrange multipliers
        a = np.ravel(solution['x'])

        # Support vectors have non zero lagrange multipliers
        sv = a > 1e-4
        ind = np.arange(len(a))[sv]
        self.a = a[sv]
        self.sv = X[sv]
        self.sv_y = y[sv]
        print "%d support vectors out of %d points" % (len(self.a), n_samples)

        # Intercept
        self.b = 0
        for n in range(len(self.a)):
            self.b += self.sv_y[n]
            self.b -= np.sum(self.a * self.sv_y * K[ind[n],sv])
            self.b /= len(self.a)

        # Weight vector
        if self.kernel == linear_kernel:
            self.w = np.zeros(n_features)
            for n in range(len(self.a)):
                self.w += self.a[n] * self.sv_y[n] * self.sv[n]
        else:
            self.w = None

        print "SVM engine is trained successfully!\n"
        #y_pred = self.predict([[10000,80]])[0]
        cm = confusion_matrix(ML.predict([global_L])[0], global_m)
        #print("New L here", global_L)
        #print("Size of L", global_L.size[0], global_L.size[1])
        print "Confusion matrix is"
        #for row in cm:
        print(cm)
        TP = cm[0][0]
        FP = cm[0][1]
        FN = cm[1][0]
        TN = cm[1][1]
        print "\nCount for True positive, TP is", TP
        print "Count for False positive, FP is", FP
        print "Count for False negative, FN is", FN
        print "Count for True negative, TN is", TN
        #accuracy = (sum(TP,TN)/sum(TP,FP,FN.TN))
        sum1 = TP + FP
        sum2 = TP + TN + FP + FN
        sum3 = TN + FP
        #print "SUMS ARE", sum1, sum2

        #plt.subplot(111)
        #plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
        #plt.title('X_train')
        #plt.subplot(112)
        plt.scatter(global_L[:, 0], global_L[:, 1], c=global_m, s=50, cmap='autumn')
        plt.title('X_test')
        plt.show()

        #print '\n'
        precision = TP / sum1
        #precision_score(global_L, global_m, average='weighted')
        print "\nPrecision of the SVM classifier is:", precision

        accuracy = (sum1 / sum2)*100
        #accuracy_score(global_L, global_m)
        print "Accuracy of the SVM classifier is:", accuracy

        detection_rate = (TP / sum2)*100
        print "Detection Rate of the SVM classifier is:", detection_rate

        FAR = (FP / sum3)*100
        print "False Alarm Rate of the SVM classifier is:", FAR


    def project(self, X):
        if self.w is not None:
            return np.dot(X, self.w) + self.b
        else:
            y_predict = np.zeros(len(X))
            for i in range(len(X)):
                s = 0
                for a, sv_y, sv in zip(self.a, self.sv_y, self.sv):
                    s += a * sv_y * self.kernel(X[i], sv)
                y_predict[i] = s
            return y_predict + self.b

    def predict(self, X):
        #print("The value of X", X)
        return np.sign(self.project(X))

    def gen_lin_separable_overlap_data(self):

        with open("newNormal.txt") as textFile:
            lines1 = [line.split() for line in textFile]

        with open("newabNormal.txt") as textFile:
            lines2 = [line.split() for line in textFile]

        X1 = []
        X2 = []
        y1 = []
        y2 = []
#print(lines)

        a1 = np.array(lines1)
        c1 = a1.astype(np.float)
        a2 = np.array(lines2)
        c2 = a2.astype(np.float)

        for i in range (0,1001):
            X1.append(c1[i][0])
            y1.append(c1[i][1])
            X2.append(c2[i][0])
            y2.append(c2[i][1])

        return X1, y1, X2, y2

    def split_train(self, X1, y1, X2, y2):
        #Training data set
        X1_train = X1[:700]
        y1_train = y1[:700]
        X2_train = X2[:700]
        y2_train = y2[:700]
        X_train = np.vstack((X1_train, X2_train))
        y_train = np.hstack((y1_train, y2_train))
        print("The X_train starts here..", X_train)
        #plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, s=50, cmap='autumn')
        #plt.title('X_train')
        #plt.show()
        return X_train, y_train

    def split_test(self, X1, y1, X2, y2):
        #Test data set
        X1_test = X1[701:1001]
        y1_test = y1[701:1001]
        X2_test = X2[701:1001]
        y2_test = y2[701:1001]
        X_test = np.vstack((X1_test, X2_test))
        y_test = np.hstack((y1_test, y2_test))
        #print("The X1_test starts here..", X1_test)
        #print("Size of X1", len(X1_test))
        #y_pred = self.predict([[10000,80]])[0]
        #print("y_pred is", y_pred)
        #plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, s=50, cmap='autumn')
        #plt.title('X_test')
        #plt.show()
        return X_test, y_test
    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

    #def plot_data(global_L, global_m):
    #    figure = np.figure(global_m)
    #    for i in range (len(y)):
    #        x_figure = global_L[global_L == figure[i]]
    #        plt.scatter(x_figure[:, 0], x_figure[:, 1], c=COLORS[i])
    #    plt.show()

#---------------------------------------------------------------------#

class StatisticCollector(threading.Thread):
    global rx_packets, rx_bytes, t_observation, PortStatsURL
    def __init__(self, threadID, dpid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.dpid = dpid  #Datapath id of the switch
    def run(self):
        global rx_packets, rx_bytes, t_observation, PortStatsURL
        #file_save = open("data_set.txt", "a")

        while True:
            try:
                #Send a request to RYU controller and get a response
                response = requests.get(PortStatsURL).json()
                data = response[self.dpid][0]
                print data

                delta_rx_packets = 0
                delta_rx_bytes = 0
                if rx_packets <= int(data['rx_packets']):
                    delta_rx_packets = int(data['rx_packets'])-rx_packets
                    rx_packets = int(data['rx_packets'])
                else:
                    rx_packets = int(data['rx_packets'])
                if rx_bytes <= int(data['rx_bytes']):
                    delta_rx_bytes = int(data['rx_bytes'])-rx_bytes
                    rx_bytes = int(data['rx_bytes'])
                else:
                    rx_bytes = int(data['rx_bytes'])

                print 'Delta RX_Packets:  ',delta_rx_packets
                print 'Delta RX_Bytes: ',delta_rx_bytes
                print '\n'

                # SVM Checking
                #				trigger = 0
                if ML.predict([[delta_rx_bytes/100.0, delta_rx_packets/10.0]])[0] == 1.0:
                    # Point is in Safezone
                    print('Kind is good traffic behavior')
                else:
                    print('Kind is bad traffic behavior')
            #					if trigger == 0:
            #					    subprocess.call(["bash","trigger_pb.sh"])
            #					    trigger = 1

            # file_save = open("data_set.txt", "a")
            # data_set = str(delta_rx_packets)+'\t'+str(delta_rx_bytes)+'\n'
            # file_save.write(data_set)
            # file_save.close()

            except:
                print 'StatisticCollector | There is an error... Exited on switch ',self.dpid
                #file_save.close()
                break

            time.sleep(t_observation)

ML = SVM(C=0.1)
ML.start()
time.sleep(30)

#y_new = ML.predict([[10000,80]])[0]
#print("y_pred is", y_new)

#y1 = ML.predict([[100,3.3]])[0]

#Start StatisticCollector agent for the switch
Collector = StatisticCollector(1000, '1')
Collector.start()

#average_precision = average_precision_score(y_test, y_score)
#print('Average precision-recall score: {0:0.2f}'.format(average_precision))
