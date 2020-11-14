import random
#import tensorflow as tf





def makelabel(ships,sidelength):

    H=1
    V=sidelength
    board_size = sidelength*sidelength


    label = [0 for i in range(board_size)]

    for s in ships:

        done = False
        while not done:
            start = random.randint(0,board_size-1)
            direction = random.randint(0,3)
            pos=start
            done = True
            for segment in range(s):
                if pos > board_size-1 or \
                   pos < 0 or \
                   ((direction == 0 or direction == 2) and \
                   (pos >= start//V*V+V or \
                   pos < start//V*V)) or \
                   label[pos]:
                    done = False
                    break
                if direction == 0:
                    # check if it's overflowing to prevent loop errors
                    pos -= H
                if direction == 1:
                    pos -= V
                if direction == 2:
                    # check if it's overflowing to prevent loop errors
                    pos += H
                if direction == 3:
                    pos += V
        
        pos = start
        for segment in range(s):
            label[pos] = 1
            if direction == 0:
                pos -= H
            if direction == 1:
                pos -= V
            if direction == 2:
                pos += H
            if direction == 3:
                pos += V

    return label

def makeinput(label, sidelength,chance):
    board_size=sidelength*sidelength
    return \
    [1 if label[i] and random.randint(0,1) == 0 else 0 \
            for i in range(board_size)]+\
    [0 if label[i] or random.randint(0,1) != 0 else 1 \
            for i in range(board_size)]


ships = (2,3,3,4,5)

H=1
V=10
board_size = V*V

chance = 5

batch_size = 50000-4100




f=open('trainingdata0.txt','a')
for b in range(batch_size):
    ls = makelabel(ships,V)
    ins = makeinput(ls, V, chance)
    f.write('labels'+str(ls)+'inputs'+str(ins)+'\n')
f.close()

#labels = tf.constant(labels_cons, tf.float32, [batch_size,board_size])
#inputs = tf.constant(inputs_cons, tf.float32, [batch_size,board_size*2])

#d = tf.data.Dataset.from_tensor_slices((labels,inputs))

##for i in range(batch_size):
##    
##
##i=d.make_one_shot_iterator()
##x,y=i.get_next()




##labels = tf.placeholder(tf.int16,[None, board_size])
##inputs = tf.placeholder(tf.int16,[None, board_size*2])


##with tf.Session() as sess:
##    print(sess.run(x))
##    print(sess.run(y))
