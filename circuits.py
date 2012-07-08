import matplotlib.pyplot as plt
import subprocess
import math

def bode_plot(v,phase=None,**kwargs):
    plt.figure()
    for i,k in enumerate(v.keys(),1):
        freq=v[k][0]
        gain=v[k][1]
        if phase!=None:
            plt.subplot(211)

        plt.subplot(str(i)+'11')
        # plot it as a log-scaled graph
        plt.plot(freq,gain,label=k)
        #plt.semilogx(freq,gain,basex=10,**kwargs)

        # update axis ranges
        ax = []
        ax[0:4] = plt.axis()
        # check if we were given a frequency range for the plot
        plt.axis(ax)

        plt.grid(True)
        # turn on the minor gridlines for log-scaled look
        plt.grid(True,which='minor')
        plt.ylabel("Gain (dB)")

        if phase!=None:
            plt.subplot(212)
            plt.semilogx(freq, phase,basex=10,**kwargs)

            # update axis ranges, we know the phase is between -pi and pi
            ax = plt.axis()
            plt.axis([ax[0],ax[1],-math.pi,math.pi])

            plt.grid(True)
            plt.grid(True,which='minor')
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Phase (rads)")

            # nice LaTeX pi scale for the phase part of the plot
            plt.yticks((-math.pi,-math.pi/2,0,math.pi/2,math.pi),
                       (r"$-\pi$",r"$-\frac{\pi}{2}$","0",r"$\frac{\pi}{2}$",r"$\pi$"))
    plt.legend(v.keys())
    plt.show()

def parse_output(output):
    value={}
    output=output.split('\n')
    index=1
    current = ()
    for line in xrange(len(output)):
        temp=output[line].replace(',','').split()
        if len(temp)>0:
            if temp[0]=='Index':
                temp2=output[line+2].replace(',','').split()
                if float(temp2[0])<index:
                    current = temp[2]
                    value[temp[2]]=([],[])
                    index=0

        if len(temp)>2:
            try:
                float(temp[1]),float(temp[2])
            except:
                continue
            index+=1
            for i in xrange(2):
                value[current][0].append(float(temp[1]))
                value[current][1].append(float(temp[2]))
    return value

def parse_output_old(output,values,start=1):
    value=[[] for i in xrange(values)]
    output=output.split('\n')
    n=0
    for line in xrange(n,len(output)):
        temp=output[line].replace(',','').split()
        if len(temp)>2:
            try:
                #time.append(float(temp[1]))
                #value.append(float(temp[2]))
                for i in xrange(values):
                    value[i].append(float(temp[start+i]))
            except ValueError:
                continue
    return value

def parse_output2(output,values,columns):
    value=[[] for i in xrange(len(columns))]
    output=output.split('\n')
    n=0
    start=False
    for line in xrange(n,len(output)):
        temp=output[line].replace(',','').split()
        if start==True and len(temp)>2:
            try:
                for i in xrange(values):
                    value[i].append(float(temp[start+i]))
            except ValueError:
                continue
        else:
            try:
                if output[line][:80]=='-'*80:
                    start=True
            except:
                pass
    return value

class Timeout(Exception):
    pass

def simulate(file,timeout):
    spice = subprocess.Popen(['timeout','2','ngspice', '-s'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = spice.communicate(file)[0]
    #f = open('spice_out','w')
    #f.write(output)
    #f.close()
    return parse_output(output)

q = """* simulation de RC2
.control
tran 10n 1000n
print v(n1)
.endc
* Spice netlister for gnetlist
R5 n4 n5 1k
V1 n0 0 dc 1 ac 2 pulse 0 1 10n 10n 100n 1u 2u
R4 n3 n4 1k
R3 n2 n3 5k
C5 n5 0 1n
R2 n1 n2 1K
C4 n4 0 1n
R1 n0 n1 1k
C3 n3 0 1n
C2 n2 0 1n
C1 n1 0 1n
I1 n5 0 DC 0.01mA
R6 0 n5 10k
.END"""

w = """*test
.control
ac dec 1000 1 250kHz
write
print v(n2)
.endc
V1 n1 0 dc 0 ac 1
R1 n1 n2 1k
C1 n2 0 100nF
.end"""

#output = simulate(w)
#bode_plot(output[0],output[1])
