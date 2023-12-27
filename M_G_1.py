import pandas as pd
import math

#Defining the Bernoulli service distribution
G_values = [(64*8/(25*10**9)), (1464*8/(25*10**9))]

df_prob = pd.read_csv("Distribution_details(Bern)_wholetrace.csv")
df_expparam = pd.read_csv("Distribution_details_wholetrace.csv")

df3 = pd.DataFrame(columns = ["filename", "rho", "Wait time in queue(sec)", "Wait time(sec)", "Length in queue(sec)"])

num_prob =  df_prob.shape[0]
num_expparam = df_expparam.shape[0]

#Calculate E[S]

def calcS(G_values, G_probs) :
    ES = G_values[0]*G_probs[0] + G_values[1]*G_probs[1]
    #print("*",ES)
    return ES

#Calculate E[S^2]

def calcS2(G_values, G_probs) :
    ES2 = (G_values[0]**2)*G_probs[0] + (G_values[1]**2)*G_probs[1]
    #print("**",ES2)
    return ES2


                
if num_prob == num_expparam :
    
    G_probs = [0, 0]
    
    for num in range(num_prob) :
        
        #filename = str(df_prob.file.str.split(".")[0]) + "_nonBDP.csv"
        filename = str(df_prob.iloc[num][1])
        #print(filename)
        
        G_probs[0] = df_prob.iloc[num][4]
        G_probs[1] = df_prob.iloc[num][5]
        
        print(G_probs)
        
        lam = df_expparam.iloc[num][2]
        print(lam)
        lam = 1/(lam*math.pow(10,-9))
        
        rho = lam * calcS(G_values, G_probs)

        #calculate wait time in queue Wq
        calc_variance = calcS2(G_values, G_probs) - calcS(G_values, G_probs)**2

        Wq = (lam * calcS2(G_values, G_probs)) / 2 * (1 - rho)
        W = Wq + calcS(G_values, G_probs)

        Lq = lam * Wq
        
        dict_row = {'filename':[filename],
               'rho':[rho],
               'Wait time in queue(sec)':[Wq],
               'Wait time(sec)':[W],
               'Length in queue(sec)': [Lq]
               } 
        df4 = pd.DataFrame(dict_row)
        df3 = df3.append(df4, ignore_index = True)
     
        print(df3)
        
df3.to_csv('Wait_time_wholetrace.csv', index= False)


        
