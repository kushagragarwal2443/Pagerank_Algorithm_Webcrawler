import sqlite3

datahandle=sqlite3.connect('SanityPageRankDB.sqlite')
cur=datahandle.cursor()

totalpages=4
#print(totalpages)

iter=input("How many iterations: ")

fromdict=[[None] for i in range(totalpages+1)]
cur.execute('SELECT * FROM Links')
for data in cur:
    if data is None:
        continue
    fid=data[0]
    tid=data[1]
    #print(fid,tid)
    fromdict[fid].append(tid)

todict=[[None] for i in range(totalpages+1)]
cur.execute('SELECT * FROM Links')
for data in cur:
    if data is None:
        continue
    fid=data[0]
    tid=data[1]
    # print(fid,tid)
    todict[tid].append(fid)

total=1.0/totalpages
old_rankval=[total]*(totalpages+10)
new_rankval=[0]*(totalpages+10)

for i in range(totalpages+1):
    print(i,fromdict[i],todict[i])

for iterations in range(int(iter)):
    print("\n\n\n****************************** ITERATION NUMBER",(iterations+1),"***************************\n")
    sanitycheck=0
    for i in range(len(todict)):
        if len(todict[i])==1:
            new_rankval[i]=0
            continue
        pr=0
        for j in range(len(todict[i])):
            if j==0:
                continue
            a=len(fromdict[todict[i][j]])
            a=a-1
            b=float(old_rankval[todict[i][j]])
            pr=pr+(b/a)

        new_rankval[i]=pr
        sanitycheck=sanitycheck+pr

    for i in range(totalpages+1):
        print(i,old_rankval[i],new_rankval[i])

    for i in range(totalpages+1):
        old_rankval[i]=new_rankval[i]

    print("\nTOTAL VALUE:",sanitycheck)
#print(fromdict,todict)
cur.close()
