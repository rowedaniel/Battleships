import tensorflow as tf
import statistics
import time


class NNet:
    def __init__(self, layershape):
        self.x = tf.placeholder(tf.float32, [None,layershape[0]])
        self.W = [0 for i in range(1,len(layershape))]
        self.b = [0 for i in range(1,len(layershape))]
        self.l = [0 for i in range(len(layershape))]; self.l[0] = self.x
        for i in range(1,len(layershape)):
            self.W[i-1] = tf.Variable(
                tf.random_normal((layershape[i-1],layershape[i]),
                                 mean=0.0, stddev=0.01)
                )
            self.b[i-1] = tf.Variable(
                tf.random_normal((layershape[i],),
                                 mean=0.0, stddev=0.01)
                )
            self.l[i] = tf.matmul(self.l[i-1], self.W[i-1]) + self.b[i-1]
        self.y = self.l[-1]
        self.y_ = tf.placeholder(tf.float32, [None,100])
        self.loss_func = tf.sqrt(tf.reduce_mean(tf.square(self.y_-self.y)))
    def calculate(self, x, sess=None):
        if sess == None: sess = tf.InteractiveSession()
        return sess.run(self.y, feed_dict={self.x:x})



def trainnew():


    gen_size = 100
    batch_size = 100
    n_gen = 99

    nets = [NNet((200,100)) for i in range(gen_size)]

    


##    cross_entropy = tf.losses.sigmoid_cross_entropy(y_, y)
##    loss_func = tf.sqrt(tf.reduce_mean(tf.square(y_-y)))
##    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss_func)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    
    # Train
    data=tf.data.Dataset.from_generator(loaddata, tf.float32,
                                 tf.TensorShape([300])
                                 )
    
    for i in range(n_gen):        
        batch_data = sess.run(data.shuffle(batch_size).batch(batch_size).\
                            make_one_shot_iterator().get_next())
        batch_xs = batch_data[:,:200]
        batch_ys = batch_data[:,200:]

        fitness = \
            [sess.run(n.loss_func,feed_dict={n.x:batch_xs,
                                             n.y_:batch_ys}) \
             for n in nets]

        # breeding
##        print('start breeding')

        bestfitness = min(fitness)
        worstfitness = max(fitness)
        medianfitness = statistics.median(fitness)
        survive = [f>medianfitness for f in fitness]
        survivors = filter(lambda x: survive[x], range(gen_size))
        dead = filter(lambda x: not survive[x], range(gen_size))

##        print('done with initialization')
        for _ in range(gen_size//2):
            n1 = nets[dead.__next__()]
            n2 = nets[survivors.__next__()]
            t1 = time.time()
            
            for w in range(len(n1.W)):
               n1.W[w].assign(n2.W[w])
               n1.W[w].assign_add(tf.random_normal(n2.W[w].shape,
                                                         stddev=0.001))
               n1.b[w].assign(n2.b[w])
               n1.b[w].assign_add(tf.random_normal(n2.b[w].shape,
                                                         stddev=0.001))
        
        
        print('gen: %i' % i)


    # Test trained model
##    correct_prediction = nets[0].loss_func#tf.square(y-y_)
    accuracy = nets[0].loss_func#tf.reduce_mean(correct_prediction)
    test_data = sess.run(data.skip(3000).shuffle(100).\
                         batch(100).make_one_shot_iterator().get_next())
    test_xs = test_data[:,:200]
    test_ys = test_data[:,200:]
    a=sess.run(accuracy, feed_dict={nets[0].x: test_xs,
                                       nets[0].y_: test_ys})
##    b=sess.run(loss_func, feed_dict={nets[0].x: test_xs,
##                                       nets[0].y_: test_ys})
    print(a,1/(1+a))
##    print(b)

    # visual test

##    test_data = sess.run(data.skip(3999).shuffle(100).\
##                         batch(100).make_one_shot_iterator().get_next())
##    test_xs = test_data[:,:200]
##    test_ys = test_data[:,200:]

    a=test_xs
    b=test_ys

    for i in range(0,100,10):
        print(a[0][i:i+10])
    print()
    for i in range(0,100,10):
        print(a[0][i+100:i+110])
    print()
    for i in range(0,100,10):
        print(b[0][i:i+10])
    print()

    result = nets[0].calculate(test_xs, sess)
    for i in range(0,100,10):
        print(result[0][i:i+10])
    print()

    
    drawthing(a,-2)
    drawthing([a[0][100:]], -1)
    drawthing(b,0)
    drawthing(result,1)
    

    
    
def drawthing(thing,n):
    import turtle
    t=turtle.Pen()
    t.speed(0)
    unit = 10
    t.forward(unit*11*n)
    a = float(min(thing[0]))
    b = float(max(thing[0]))
    
    for i in range(0,100,10):
        for j in thing[0][i:i+10]:
            c=float(j)
            if c < 0:
                c = (c-a)/(b-a)
            t.color(c, c, c)
            t.begin_fill()
            for i in range(4):
                t.forward(unit)
                t.right(90)
            t.end_fill()
            t.forward(unit)
        t.color(0.5,0.5,0.5)
        t.backward(unit*10)
        t.right(90)
        t.forward(unit)
        t.left(90)
        

def loadlabeldata():
    f=open('trainingdata0.txt','r')
    for l in f:
        i=l.index('inputs')
        yield eval(l[6:i])
    f.close()

def loadinputdata():
    f=open('trainingdata0.txt','r')
    for l in f:
        i=l.index('inputs')
        yield eval(l[i+6:-1])
    f.close()

def loaddata():
    f=open('trainingdata0.txt','r')
    for l in f:
        i=l.index('inputs')
        yield eval(l[i+6:])+eval(l[6:i])
    f.close()
    
    
if __name__ == '__main__':
    trainnew()
