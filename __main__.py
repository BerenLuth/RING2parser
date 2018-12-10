from src.graphs import GraphMatrix

# It's exatcly the same file just to try read from multiple files
x = GraphMatrix("../assets/6a90_network.xml", "../assets/6a90_network.xml")


for el in x.get_element(0, 3):
    print(el)
