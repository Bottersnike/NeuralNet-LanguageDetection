from NeuralNetwork import NeuralNetwork
from GUI import GUI


def main():
    def network_loop(network):
        while True:
            if network.training:
                network.train()

    import thread

    network = NeuralNetwork()
    network.setup()

    gui = GUI()
    gui.bind(network)

    thread.start_new_thread(network_loop, (network,))

    gui.mainloop()


if __name__ == "__main__":
    main()
