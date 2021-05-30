import networkx as nx
import matplotlib.pyplot as plt

plt.figtext(0.08, 0.6, "Stock price = $10")
plt.figtext(0.75, 0.91, "Stock price = $11.5")
plt.figtext(0.75, 0.87, "call payoff = $0.5")
plt.figtext(0.75, 0.28, "Stock price = $9")
plt.figtext(0.75, 0.24, "call payoff = $0")

n=1

def binomial_grid(n):

    G=nx.Graph()
    for i in range(0,n+1):
        for j in range(1,i+2):
            if i<n:
                G.add_edge((i,j),(i+1,j))
                G.add_edge((i,j),(i+1,j+1))
    
    posG={}

    for node in G.nodes():
        posG[node]=(node[0], n+2+node[0] - 2 * node[1])
    
    nx.draw(G, pos=posG)

binomial_grid(n)
plt.show()