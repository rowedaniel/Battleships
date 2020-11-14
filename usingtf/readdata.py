import tensorflow as tf



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


d1=tf.data.Dataset.from_generator(loadlabeldata, tf.int64,
                                 tf.TensorShape([100])
                                 )
d2=tf.data.Dataset.from_generator(loadinputdata, tf.int64,
                                 tf.TensorShape([200]))

for i in range(1):
    valuelabel = d1.skip(i).batch(10).make_one_shot_iterator()#.get_next()
    valueinput = d2.skip(i).batch(10).make_one_shot_iterator()#.get_next()
    with tf.Session() as sess:
        a=sess.run(valuelabel.get_next())
        print(a)
        print(sess.run(valueinput.get_next()))
        print()
