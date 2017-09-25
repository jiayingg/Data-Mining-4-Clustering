from math import pow
import Jiaying_Gu_kmeans
import sys
import json

# |c(v)-c(2v)|/(c(v)*v)
# |c(z)-c(y)|/(c(z)*|z-y|)
def get_change_rate(data_points,a,b):
    return abs(Jiaying_Gu_kmeans.kmeans(data_points,a)[1]-Jiaying_Gu_kmeans.kmeans(data_points,b)[1])/(Jiaying_Gu_kmeans.kmeans(data_points,a)[1]*abs(a-b))

# Step 1
def stop_at_2v(data_points,theta):
    v=1
    m=0
    # Stop at k=2v where r < theta
    while get_change_rate(data_points,v,v*2) >= theta:
        m+=1
        v=int(pow(2,m))
        # If 2v > n, output k* = n
        if 2*v>len(data_points):
            return len(data_points)
    return v

# Step 2
def binary_search(data_points,theta,v):
    y=v
    x=v/2

    while x!=y-1:
        z=(x+y)/2
        # If there is little change, search [x,z]
        if get_change_rate(data_points,z,y)<theta:
            y=z
        # Else search [z,y]
        else:
            x=z

    # Smaller average diameter means higher cohesion
    if Jiaying_Gu_kmeans.kmeans(data_points,x)[1]<Jiaying_Gu_kmeans.kmeans(data_points,y)[1]:
        return x
    else:
        return y

def find_kstar(data_points,theta):
    v=stop_at_2v(data_points,theta)
    return binary_search(data_points,theta,v)

if __name__ == '__main__':
    input_lines = open(sys.argv[1])
    theta = float(sys.argv[2])
    data_points=[]

    for line in input_lines:
        record = json.loads(line)
        data_points.append(tuple(record))

    print find_kstar(data_points,theta)