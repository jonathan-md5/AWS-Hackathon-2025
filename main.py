import matplotlib.pyplot as plt

import graphs

def main() -> None:
    graphs.heatmaps()
    graphs.games_played()
    graphs.matchups()
    graphs.age_to_weight()
    plt.show()

if __name__ == "__main__":
    main()
