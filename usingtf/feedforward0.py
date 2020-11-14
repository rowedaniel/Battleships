import tensorflow as tf

def trainnew():

    x = tf.placeholder(tf.float32, [None,200])
    # input layer        batch size ^    ^ input size
    W = tf.Variable(    tf.zeros((200,100)))
    # weight layer 0   input size ^ ^ output size
    b = tf.Variable(    tf.zeros([100]))
    # bias layer 0    output size ^
    y = tf.matmul(x, W) + b
    # output layer  shape = (batch size, output size)


    y_ = tf.placeholder(tf.float32, [None,100])


    #cross_entropy = tf.losses.sigmoid_cross_entropy(y_, y)
    loss_func = tf.sqrt(tf.reduce_mean(tf.square(y_-y)))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss_func)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    
    # Train
    data=tf.data.Dataset.from_generator(loaddata, tf.float32,
                                 tf.TensorShape([300])
                                 )
    batch_size = 100
    gen_size = 5000
    for i in range(gen_size):        
        batch_data = sess.run(data.shuffle(batch_size).batch(batch_size).\
                            make_one_shot_iterator().get_next())
        batch_xs = batch_data[:,:200]
        batch_ys = batch_data[:,200:]
        
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
        print('gen: %i' % i)


    # Test trained model
    correct_prediction = tf.square(y-y_)
    accuracy = tf.reduce_mean(correct_prediction)
    test_data = sess.run(data.skip(3999).shuffle(100).\
                         batch(100).make_one_shot_iterator().get_next())
    test_xs = test_data[:,:200]
    test_ys = test_data[:,200:]
    a=sess.run(accuracy, feed_dict={x: test_xs,
                                       y_: test_ys})
    b=sess.run(loss_func, feed_dict={x: test_xs,
                                       y_: test_ys})
    print(a,1/(1+a))
    print(b)

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

    result = sess.run(y, feed_dict={x: test_xs,
                                    y_: test_ys})
    for i in range(0,100,10):
        print(result[0][i:i+10])
    print()

    
    drawthing(a,-2)
    drawthing([a[0][100:]], -1)
    drawthing(b,0)
    drawthing(result,1)
    
    
    return W, b


    
    
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
    W, b = trainnew()
